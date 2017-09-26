import sys
import time
import threading
import locale
import random
import json
from board import Board
from queue import Empty
from pprint import pprint
from stdio_ipc import ChildProcess


def action(ai, content):
    try:
        ai.send(content)
        message = ai.recv(timeout=1)
        nx, ny = map(int, message.strip().split)
    except Empty as e:
        return {'err': 'timeout'}
    except:
        return {'err': 'wrong format. your output: %s' % repr(message)}
    return {'nx': nx, 'ny': ny}


should_reverse = 0


def get_init(ai0, ai1, side=random.randint(0, 1)):
    global turn, record_json, should_reverse
    turn = side
    should_reverse = side
    names = ["", ""]
    try:
        ai0.send(side)
        names[0] = ai0.recv(timeout=2)
    #     record_json['init-board'] = ""
    except Empty as e:
        finish(1, "timeout", "")
    except Exception as e:
        print(e)
        finish(2, str(e), str(e))

    try:
        ai1.send(1 - side)
        names[1] = ai1.recv(timeout=2)
    except Empty as e:
        finish(0, "", "timeout")
    except Exception as e:
        print(e)
        finish(2, str(e), str(e))

    record_json['id'] = [side, 1 - side]
    return tuple(names)


def finish(winner2, err0="", err1=""):
    global running, name0, name1, first_sit, steps, winner, ai0, ai1, record_json, should_reverse
    winner = winner2
    record_json['total'] = steps
    if winner2 < 2 and should_reverse == 1:
        winner2 = 1 - winner2
    record_json['result'] = winner2
    record_json['err'] = [err0, err1]
    # kill ai and write stdio log
    if type(ai0) is not dict:
        ai0.exit()
    if type(ai1) is not dict:
        ai1.exit()

    if not p2dv:
        print(record_json)
    json_out = open('result.json', 'w')
    json.dump(record_json, json_out)
    json_out.close()

    running = False
    sys.exit(0)


def spawnAI(args, save_stdin_path, save_stdout_path, save_stderr_path):
    try:
        ai = ChildProcess(args, save_stdin_path,
                          save_stdout_path, save_stderr_path)
        return ai
    except:
        return {'err': 'fail to spawn the program.' + str(sys.exc_info()[1])}


def judge():
    global steps, ai0, ai1, turn, record_json
    nw = Board(record_json)
    ai0 = spawnAI(sys.argv[1], 'ai0_stdin.log',
                  'ai0_stdout.log', 'ai0_stderr.log')
    ai1 = spawnAI(sys.argv[2], 'ai1_stdin.log',
                  'ai1_stdout.log', 'ai1_stderr.log')
    t = get_init(ai0, ai1)
    print(t)
    name0, name1 = t
    if name0 == "":
        name0 = "Unknown_0"
    if name1 == "":
        name1 = "Unknown_1"
    record_json['user'] = [name0, name1]
    record_json['step'] = []
    while (True):
        print(steps)
        x = ""
        if turn == 0:
            try:
                if x != "":
                    ai0.send(x)
                ai0.send("Action")
                x = ai0.recv(timeout=1)
                loc = list(map(int, x.split()))
                rec = nw.update(loc)
                if rec != True:
                    finish(1)
                    break
                if nw.result() < 2:
                    finish(nw.result())
                    break
            except Exception as e:
                print(e)
                finish(1)
                break
            steps += 1
        turn = 0
        if steps > 99:
            print("DRAW!")
            finish(2)
            break
        # send to 1
        try:
            if x != "":
                ai1.send(x)
            ai1.send("Action")
            x = ai1.recv(timeout=1)
            loc = list(map(int, x.split()))
            rec = nw.update(loc)
            if rec != True:
                finish(0)
                break
            if nw.result() < 2:
                finish(nw.result())
                break
        except Exception as e:
            print(e)
            finish(0)
            break
        steps += 1
        # send to 0
        if steps > 99:
            print("DRAW!")
            finish(2)
            break


def p2dv():
    t = threading.Thread(target=judge)
    t.start()

    while True:
        line = sys.stdin.readline()
        if not running:
            sys.stderr.write('finished\n')
            sys.stderr.flush()
            break

        if line == 'get steps\n':
            sys.stderr.write('%d\n' % steps)

        sys.stderr.flush()


def main():
    global running, p2dv

    if (not len(sys.argv) in [3, 4]):
        print('usage:   ./main.py ai0Path ai1Path')
        print('example: ./main.py ./sample_ai ./sample_ai')
        print('')
        sys.exit(1)

    running = True
    if len(sys.argv) == 4 and sys.argv[3] == 'p2dv':
        is_p2dv = True
        p2dv()
    else:
        is_p2dv = False
        judge()


# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
steps = 0
turn = 0
ai0 = 0
ai1 = 0
name0 = 'Unknown'
name1 = 'Unknown'
winner = -1
record_json = {}
main()

if type(ai0) is not dict:
    ai0.exit()
if type(ai1) is not dict:
    ai1.exit()
