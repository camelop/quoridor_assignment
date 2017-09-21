import numpy as np


class Board(object):
    def __init__(self):
        self.board = np.zeros((20, 20), dtype=bool)
        self.loc = []
        self.loc.append([2, 10])
        self.loc.append([18, 10])
        self.side = 0
        self.near = [[0, 2], [0, -2], [2, 0], [-2, 0]]
        self.walls = []
        self.walls.append(10)
        self.walls.append(10)
        self.recordColor = 0

    def positionType(self, loc):
        if 2 <= loc[0] <= 18 and 2 <= loc[1] <= 18 and loc[0] % 2 == 0 and loc[1] % 2 == 0:
            return 0
        if 2 <= loc[0] <= 17:
            if loc[0] % 2 == 0:
                if 3 <= loc[1] <= 17 and loc[1] % 2 == 1:
                    return 1
            else:
                if 2 <= loc[1] <= 16 and loc[1] % 2 == 0:
                    return 2
        return 3

    def record(self, loc):
        file = open("record.txt", "a")
        type = self.positionType(loc)
        if type == 0:
            if self.recordColor == 0:
                file.write("red")
            else:
                file.write("blue")
            file.write(" " + str(loc[0] // 2 - 1) +
                       " " + str(loc[1] // 2 - 1) + "\n")
        elif type in (1, 2):
            file.write("wall " + str(loc[0] - 2) + " " + str(loc[1] // 2 - 1))
        file.close()
        self.recordColor = 1 - self.recordColor

    def update(self, loc):
        case = self.positionType(loc)
        otherside = 1 - self.side
        nw_loc = self.loc[self.side]
        if case == 0:
            v = [loc[0] - nw_loc[0], loc[1] - nw_loc[1]]
            if v in self.near:
                v_d2 = (v[0] // 2, v[1] // 2)
                wall = (nw_loc[0] + v_d2[0], nw_loc[1] + v_d2[1])
                if loc != self.loc[otherside] and not self.board[wall[0]][wall[1]]:
                    self.loc[self.side] = loc
                    self.side = 1 - self.side
                    self.record(loc)
                    return True
            else:
                for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    if self.board[nw_loc[0] + d[0]][nw_loc[1] + d[1]]:
                        continue
                    if [nw_loc[0] + 2 * d[0], nw_loc[1] + 2 * d[1]] != self.loc[otherside]:
                        continue
                    if self.board[nw_loc[0] + 3 * d[0]][nw_loc[1] + 3 * d[1]]:
                        for dt in [(d[1], d[0]), (-d[1], d[0]), (d[1], -d[0]), (-d[1], -d[0])]:
                            if nw_loc[0] + 2 * d[0] + 2 * dt[0] != loc[0] or\
                                    nw_loc[1] + 2 * d[1] + 2 * dt[1] != loc[1]:
                                continue
                            if not self.board[nw_loc[0] + 2 * d[0] + dt[0]][nw_loc[1] + 2 * d[1] + dt[1]]:
                                self.loc[self.side] = loc
                                self.side = 1 - self.side
                                self.record(loc)
                                return True
                    else:
                        if nw_loc[0] + 4 * d[0] == loc[0] and nw_loc[1] + 4 * d[1] == loc[1]:
                            self.loc[self.side] = loc
                            self.side = 1 - self.side
                            self.record(loc)
                            return True
            return "Invalid Move"
        elif case == 1:
            if self.board[loc[0]][loc[1]] or\
                    self.board[loc[0] + 1][loc[1]] or\
                    self.board[loc[0] + 2][loc[1]] or\
                    self.walls[self.side] <= 0:
                return "Invalid Move"
            self.board[loc[0]][loc[1]] = True
            self.board[loc[0] + 1][loc[1]] = True
            self.board[loc[0] + 2][loc[1]] = True
            self.side = 1 - self.side
            self.walls[self.side] -= 1
            self.record(loc)
            return True
        elif case == 2:
            if self.board[loc[0]][loc[1]] or\
                    self.board[loc[0]][loc[1] + 1] or\
                    self.board[loc[0]][loc[1] + 2] or\
                    self.walls[self.side] <= 0:
                return "Invalid Move"
            self.board[loc[0]][loc[1]] = True
            self.board[loc[0]][loc[1] + 1] = True
            self.board[loc[0]][loc[1] + 2] = True
            self.side = 1 - self.side
            self.walls[self.side] -= 1
            self.record(loc)
            return True
        else:
            return "Invalid Move"

    def result(self):
        if self.loc[0][0] == 18:
            return 0
        elif self.loc[1][0] == 2:
            return 1
        else:
            return 2


"""
# Test
b = Board()
np.set_printoptions(threshold=np.nan)
while (True):
    print(b.loc, b.side)
    print(b.board.astype(int))
    temp = input()
    temp = temp.split()
    temp = list(map(int, temp))
    b.update(temp)
"""
