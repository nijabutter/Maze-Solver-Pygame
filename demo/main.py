'''
Requires pygame:
    From CLI:
    pip install pygame
    python -m pip install pygame

Uses Randomized depth-first search to generate the maze
Then A* Pathfinding to solve it

Press R to make a new maze
Press ENTER / RETURN to solve it

'''

import pygame
import random
import time
import math
from Cell import Cell

# Window size
W_WIDTH = W_HEIGHT = 1000 

# Columns and rows
# Wouldn't recommend > 100
ACROSS = DOWN = 50


FPS = 1000

C_WIDTH, C_HEIGHT = W_WIDTH // ACROSS, W_HEIGHT // DOWN
window = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
pygame.display.set_caption("Maze " + str(ACROSS) + "x" + str(DOWN))
isRunning = True
background = (0, 0, 0)
pygame.init()
fpsdelay = 1000 // FPS
cells = []
stack = []
current = None
unvisited = ACROSS * DOWN
goalX = (ACROSS-1) * C_WIDTH
goalY = (DOWN-1) * C_HEIGHT
startX = 0
startY = 0
solutionFound = False
solving = False
closedSet = []
openSet = []
path = []
def Setup():
    global cells
    global stack
    global current
    global unvisited
    cells = []
    stack = []
    current = None
    unvisited = ACROSS * DOWN
    for y in range(DOWN):
        cells.append([])
        for x in range(ACROSS):
            cells[y].append(Cell(window, x*C_WIDTH, y*C_HEIGHT, C_WIDTH, C_HEIGHT, x, y))
            if x > 0:
                # add to left neighbour
                cells[y][x-1].neighbours.append(cells[y][x])
                cells[y][x].neighbours.append(cells[y][x-1])
            if y > 0:
                # add to top neighbour
                cells[y-1][x].neighbours.append(cells[y][x])
                cells[y][x].neighbours.append(cells[y-1][x])
            
    current = cells[0][0]
    unvisited -= 1
    openSet.append(cells[startY][startX])


        


def Update():
    global current
    global unvisited
    global makingMaze
    global isRunning
    if unvisited == 0:
        makingMaze = False
        return
    current.visited = True
    neighbours = []
    if current.indexX > 0:
        # can have left neighbour
        if cells[current.indexY][current.indexX-1].visited == False:
            neighbours.append(cells[current.indexY][current.indexX-1])

    if current.indexX < ACROSS-1:
        # can have right neighbour
        if cells[current.indexY][current.indexX+1].visited == False:
            neighbours.append(cells[current.indexY][current.indexX+1])
    
    if current.indexY > 0:
        # can have top neighbour
        if cells[current.indexY-1][current.indexX].visited == False:
            neighbours.append(cells[current.indexY-1][current.indexX])

    if current.indexY < DOWN-1:
        # can have bottom neighbour
        if cells[current.indexY+1][current.indexX].visited == False:
            neighbours.append(cells[current.indexY+1][current.indexX])
    
    # current cell has unvisited neighbours
    if len(neighbours) > 0:
        nextCell = neighbours[random.randint(0, len(neighbours)-1)]
        stack.append(current)
        nextCell.visited = True
        unvisited -= 1
        xDiff = current.indexX - nextCell.indexX
        yDiff = current.indexY - nextCell.indexY
        
        if xDiff == 1:
            # neighbour on left
            nextCell.walls[0] = False
        elif xDiff == -1:
            # neighbour on right
            current.walls[0] = False
        if yDiff == 1:
            # neighbour on top
            nextCell.walls[1] = False
        elif yDiff == -1:
            # neighbour on bottom
            current.walls[1] = False
        current = nextCell
    elif len(stack) > 0:
        current = stack.pop()

def heuristic(ax, ay, bx, by):
    return math.sqrt((bx-ax)**2 + (by-ay)**2)

def SolveMaze():
    global solutionFound
    global solving
    if not solutionFound:
        if len(openSet) > 0:
            lowestIndex = 0
            for i in range(len(openSet)):
                if openSet[i].f < openSet[lowestIndex].f:
                    lowestIndex = i
            current = openSet[lowestIndex]
            if current.x == goalX and current.y == goalY:
                path.append(current)
                while current.previous != None:
                    path.append(current.previous)
                    current = current.previous
                solutionFound = True
                solving = False
                print("Solved!")
                return
            openSet.remove(current)
            closedSet.append(current)

            for n in current.neighbours:
                xDiff = current.indexX - n.indexX
                yDiff = current.indexY - n.indexY

                if xDiff == 0:
                    # top or bottm
                    if yDiff == 1:
                        # top
                        if n.walls[1]:
                            continue
                    else:
                        # bottom
                        if current.walls[1]:
                            continue
                elif xDiff == 1:
                    # left
                    if n.walls[0]:
                        continue
                else:
                    # right
                    if current.walls[0]:
                        continue

                if n in closedSet:
                    continue
                tentativeG = current.g + 1
                if n not in openSet:
                    openSet.append(n)
                elif tentativeG > n.g:
                    continue
                n.g = tentativeG
                n.h = heuristic(n.x, n.y, goalX, goalY)
                n.f = n.g + n.h 
                n.previous = current
                #current = n
        else:
            solutionFound = True
            solving = False
            print("No solution!")


def MakeMaze():
    global solutionFound
    global closedSet
    global openSet
    global path
    global makingMaze
    global solving
    solving = False
    makingMaze = True
    solutionFound = False
    closedSet = []
    openSet = []
    path = []
    print("Making maze...")
    start = time.process_time()
    Setup()
    #print("Made maze in:", time.process_time() - start)

def Input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global isRunning
            isRunning = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                global solving
                solving = True
            elif event.key == pygame.K_r:
                MakeMaze()
    
def Draw():
    window.fill(background)
    for y in range(DOWN):
        for x in range(ACROSS):
            cells[y][x].draw()
            if x == 0 and y == 0:
                filled_rect = pygame.Rect(cells[y][x].x, cells[y][x].y, C_WIDTH, C_HEIGHT)
                pygame.draw.rect(window, (0, 100, 0), filled_rect) 
            elif x == ACROSS-1 and y == DOWN-1:
                filled_rect = pygame.Rect(cells[y][x].x, cells[y][x].y, C_WIDTH, C_HEIGHT)
                pygame.draw.rect(window, (100, 0, 0), filled_rect)
            if cells[y][x] in openSet:
                filled_rect = pygame.Rect(cells[y][x].x+C_WIDTH/3, cells[y][x].y+C_HEIGHT/3, C_WIDTH/3, C_HEIGHT/3)
                pygame.draw.rect(window, (0, 0, 100), filled_rect)
            if cells[y][x] in closedSet:
                filled_rect = pygame.Rect(cells[y][x].x+C_WIDTH/3, cells[y][x].y+C_HEIGHT/3, C_WIDTH/3, C_HEIGHT/3)
                pygame.draw.rect(window, (100, 0, 0), filled_rect)
            if cells[y][x] in path:
                filled_rect = pygame.Rect(cells[y][x].x+C_WIDTH/3, cells[y][x].y+C_HEIGHT/3, C_WIDTH/3, C_HEIGHT/3)
                pygame.draw.rect(window, (0, 100, 0), filled_rect)

    pygame.display.flip()
MakeMaze()

while isRunning:
    Input()
    if solving:
        SolveMaze()
    Draw()
    if makingMaze:
        Update()
    pygame.time.delay(fpsdelay) # cap fps