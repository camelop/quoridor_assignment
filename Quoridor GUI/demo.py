import pygame
pygame.init()

# Define some colors
BLACK = (0,   0,   0)
DARK = (100, 100, 100)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
BLUE = (0,   0, 255)

screen_h = 900
screen_w = 900
edge = 50
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Quoridor Demo v1.1 by littleRound")

block_h = (screen_h - 2 * edge) // 9
block_w = (screen_w - 2 * edge) // 9

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


def DrawBoard():
    # Draw on the screen a green line from (0, 0) to (100, 100)
    # that is 5 pixels wide.
    def BoardLine(y1, x1, y2, x2):
        pygame.draw.line(screen, GRAY, [x1, y1], [x2, y2], 2)

    for i in range(edge, edge + 9 * block_h, block_h):
        for j in range(edge, edge + 9 * block_w, block_w):
            BoardLine(i, j, i + block_h, j)
            BoardLine(i, j, i, j + block_w)

    for i in range(edge, edge + 9 * block_h, block_h):
        BoardLine(i, edge + 9 * block_w, i + block_h, edge + 9 * block_w)

    for j in range(edge, edge + 9 * block_w, block_w):
        BoardLine(edge + 9 * block_h, j, edge + 9 * block_h, j + block_w)


def DrawWall(wall):
    joint = 10

    def WallLine(y1, x1, y2, x2):
        pygame.draw.line(screen, BLACK, [x1, y1], [x2, y2], joint * 2 - 4)
    assert 0 <= wall[0] < 16
    assert 0 <= wall[1] < 8
    if wall[0] % 2 == 0:
        # it is a -
        x = edge + wall[0] // 2 * block_h
        y = edge + wall[1] * block_w + block_w
        WallLine(x + joint, y, x + block_h * 2 - joint, y)
    else:
        # it is a |
        x = edge + (wall[0] + 1) // 2 * block_h
        y = edge + wall[1] * block_w
        WallLine(x, y + joint, x, y + block_w * 2 - joint)


def DrawPlayer(location, color):
    joint = 30

    def Square(y, x, color):
        pygame.draw.rect(screen, color, [
                         x + joint + 2, y + joint + 2, block_w - 2 * joint, block_h - 2 * joint])
    Square(edge + location[0] * block_h, edge + location[1] * block_w, color)


walls = []
redLocation = (0, 4)
blueLocation = (8, 4)
init = (walls.copy(), redLocation, blueLocation, "Red goes first")

history = [init]
nwState = 0


record = open('record.txt', 'w')


def LastMove():
    global nwState
    if nwState <= 0:
        return
    nwState -= 1


def NextMove():
    global nwState
    if nwState + 1 >= len(history):
        return
    nwState += 1


nw_side = 0

# create wall_zone
wall_zone = {}

for i in range(16):
    for j in range(8):
        joint = 10

        def MapWallLine(y1, x1, y2, x2, des):
            wall_zone[(x1, y1, x2, y2)] = des
        if i % 2 == 0:
            # it is a -
            x = edge + i // 2 * block_h
            y = edge + j * block_w + block_w
            MapWallLine(x + joint, y, x + block_h - joint, y, (i, j))
        else:
            # it is a |
            x = edge + (i + 1) // 2 * block_h
            y = edge + j * block_w
            MapWallLine(x, y + joint, x, y + block_w - joint, (i, j))


def handlePress(pos):
    global nw_side
    global redLocation
    global blueLocation
    line = "Meaningless\n"
    x, y = pos
    for conditions, id in wall_zone.items():
        if id[0] % 2 == 0:
            if conditions[0] - 8 <= x <= conditions[2] + 8:
                if conditions[1] <= y <= conditions[3]:
                    line = "wall " + str(id[0]) + ' ' + str(id[1]) + '\n'
                    break
        else:
            if conditions[0] <= x <= conditions[2]:
                if conditions[1] - 8 <= y <= conditions[3] + 8:
                    line = "wall " + str(id[0]) + ' ' + str(id[1]) + '\n'
                    break
    if line == "Meaningless\n":
        x = (x - edge) // block_w
        y = (y - edge) // block_h
        if (0 <= x <= 8) and (0 <= y <= 8):
            if nw_side == 0:
                line = "red " + str(y) + ' ' + str(x) + '\n'
            else:
                line = "blue " + str(y) + ' ' + str(x) + '\n'

    tokens = line.split()
    # assert len(tokens) == 3
    if tokens[0] == 'wall':
        walls.append((int(tokens[1]), int(tokens[2])))
        nw_side = 1 - nw_side
    elif tokens[0] == 'red':
        redLocation = (int(tokens[1]), int(tokens[2]))
        nw_side = 1 - nw_side
    elif tokens[0] == 'blue':
        blueLocation = (int(tokens[1]), int(tokens[2]))
        nw_side = 1 - nw_side
    else:
        return
    record.write(line)
    history.append((walls.copy(), redLocation, blueLocation, line[:-1]))
    NextMove()


# Bold: True, Italics: False
font = pygame.font.SysFont('Calibri', 20, True, False)

text = "Good morning"
import sys
# -------- Main Program Loop -----------
playing = -1
speed = 40
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                LastMove()
            elif event.key == pygame.K_RIGHT:
                NextMove()
            elif event.key == pygame.K_SPACE:
                if playing == -1:
                    playing = speed
                else:
                    playing = -1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                handlePress(pos)
    screen.fill(WHITE)
    # --- Game logic should go here
    walls, redLocation, blueLocation, text = history[nwState]
    if playing > 0:
        playing -= 1
    elif playing == 0:
        NextMove()
        playing = speed

    # show the rectangle if cover
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    for conditions, id in wall_zone.items():
        x, y = mouse_pos
        joint = 10
        if id[0] % 2 == 0:
            if conditions[0] - 8 <= x <= conditions[2] + 8:
                if conditions[1] <= y <= conditions[3]:
                    x = edge + id[0] // 2 * block_h
                    y = edge + id[1] * block_w + block_w
                    pygame.draw.line(
                        screen, DARK, [y, x + joint], [y,  x + block_h * 2 - joint], joint * 2 - 4)
                    break
        else:
            if conditions[0] <= x <= conditions[2]:
                if conditions[1] - 8 <= y <= conditions[3] + 8:
                    x = edge + (id[0] + 1) // 2 * block_h
                    y = edge + id[1] * block_w
                    pygame.draw.line(
                        screen, DARK, [y + joint, x], [y + block_w * 2 - joint, x], joint * 2 - 4)
                    break

    # change mouse
    if nw_side == 0:
        nw_color = RED
    else:
        nw_color = BLUE
    pygame.draw.rect(screen, nw_color, [mouse_x, mouse_y, 30, 30], 5)

    # --- Drawing code should go here
    DrawBoard()
    for wall in walls:
        DrawWall(wall)
    DrawPlayer(redLocation, RED)
    DrawPlayer(blueLocation, BLUE)
    text_f = font.render(text, True, BLACK)
    screen.blit(text_f, [10, 10])
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

record.close()
