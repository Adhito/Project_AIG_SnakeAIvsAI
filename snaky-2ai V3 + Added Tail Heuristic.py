import random, pygame, sys
from pygame.locals import *
from random import randint
import math

FPS = 60
##WINDOWWIDTH = 640
#WINDOWHEIGHT = 480
WINDOWWIDTH =  960
WINDOWHEIGHT = 960
CELLSIZE = 40
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK


apple = {'x':0,'y':0}

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

DIRECTION = [UP,DOWN,LEFT,RIGHT]

HEAD = 0 # syntactic sugar: index of the worm's head

distance1 = [] #inisialisasi distance
distance2 = []

#initialize distance array
for y in range(CELLHEIGHT):
    distance1.append([])
    distance2.append([])
    for x in range(CELLWIDTH):
        distance1[y].append(8888)
        distance2[y].append(8888)

def into_queue(coor, queue, visited, worm1, worm2):
    if coor == (apple['x'],apple['y']): #if coordinate is the apple
        return False
    elif coor[0] < 0 or coor[0] >= CELLWIDTH: #if x coordinate in the border or outside of the screen
        return False
    elif coor[1]< 0 or coor[1]>= CELLHEIGHT: #if y coordinate in the border or outside of the screen
        return False
    elif coor  in queue: #if coordinate already in queue
        return False
    elif coor  in visited: #if coordinate already visited
        return False
    elif is_snake(coor[0], coor[1], worm1, worm2): #if the coordinate is the snake1 or snake2 body
        return False
    else:
        return True
    

def is_snake(x,y,worm1, worm2):
    #the code can still be refactored welp
    #this code check if the x,y coordinate belongs to worm boy
    temp1 = False
    temp2 = False

    for body in worm1:
        if body['x'] == x and body['y'] == y:
            temp1 =  True
    
    for body in worm2:
        if body['x'] == x and body['y'] == y:
            temp2 =  True
    
    if temp1 == True or temp2 == True:
        return True
    else:
        return False


def cal_distance(worm1, worm2):
    #worm 1 with A* (with tail distance to tile as heuristic)
    #worm 2 with dijkstra
    queue1 = [(apple['x'],apple['y'])]
    queue2 = [(apple['x'],apple['y'])]

    visited1 = []
    visited2 = []

    for y in range(CELLHEIGHT):
        for x in range(CELLWIDTH):
            distance1[y][x] = 9999
            distance2[y][x] = 9999

    distance1[apple['y']][apple['x']] = 0
    distance2[apple['y']][apple['x']] = 0


    while len(queue1) != 0 :
        head = queue1[0]
        visited1.append(head)
        up_grid = head[0], head[1] - 1
        down_grid = head[0], head[1] + 1
        left_grid = head[0] - 1, head[1]
        right_grid = head[0] + 1, head[1]

        for grid in [up_grid, down_grid, left_grid, right_grid]:
            if into_queue(grid, queue1, visited1,worm1, worm2):
                queue1.append(grid)
                distance1[grid[1]][grid[0]] = distance1[head[1]][head[0]] + 1 + abs(grid[0] - worm1[-1]['x']) + abs(grid[1] - worm1[-1]['y']) #heuristic part


        queue1.pop(0)
    
    while len(queue2) != 0:
        head = queue2[0]
        visited2.append(head)
        up_grid = head[0], head[1] - 1
        down_grid = head[0], head[1] + 1
        left_grid = head[0] - 1, head[1]
        right_grid = head[0] + 1, head[1]

        for grid in [up_grid, down_grid, left_grid, right_grid]:
            if into_queue(grid, queue2, visited2,worm1, worm2):
                queue2.append(grid)
                distance2[grid[1]][grid[0]] = distance2[head[1]][head[0]] + 1 #normal dijkstra
        queue2.pop(0)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init() #ini kyk frame set visible 
    FPSCLOCK = pygame.time.Clock() #ini kyk thread
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #ini kek set size di java
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18) #ngeset font 
    pygame.display.set_caption('Danke Game')#nge set title game 

    showStartScreen() #nampilin gambar muter ga jelas
    while True: #loop untuk frame nya
        runGame() #jalanin game nya 
        showGameOverScreen() #ini kalo dh lese 


def can_move(coor, worm1, worm2):
    if coor[0]< 0 or coor[0] >= CELLWIDTH: #check if next move is outside the screen for x axis
        return False
    elif coor[1]< 0 or coor[1] >= CELLHEIGHT: #check if next move is outside the screen for x axis
        return False
    elif is_snake(coor[0], coor[1],worm1, worm2): #check if next move is the snake body
        return False
    elif coor == (worm1[HEAD]['x'], worm1[HEAD]['y']) or coor == (worm2[HEAD]['x'], worm2[HEAD]['y']): #check if the next move is the head of the snake
        return False
    else:
        return True

def test_not_ok(temp, worm):
    #ngecek kalo corrdinate nya di badan satu uler 
    for body in worm:
        if temp['x'] == body['x'] and temp['y'] == body['y']:
            return True
    return False

def update_dirc(now, direc):
    #buat ngupdate direction yang akan di ambil
    loc = {'x':0,'y':0}
    if direc == UP:
        loc = {'x':now['x'],'y':now['y']-1}
    elif direc == DOWN:
        loc = {'x':now['x'],'y':now['y']+1}
    elif direc == RIGHT:
        loc = {'x':now['x']+1,'y':now['y']}
    elif direc == LEFT:
        loc = {'x':now['x']-1,'y':now['y']}
    return loc


def runGame():
    global running_,apple,DIRECTION
    # Set a random start point.
    startx = random.randint(0, CELLWIDTH -1)
    starty = random.randint(0, CELLHEIGHT -1)
    wormCoords1 = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    #di atas buat snake 1 di bawah ni buat snake 2 (dapetin kordinat random)
    startx = random.randint(0, CELLWIDTH -1)
    starty = random.randint(0, CELLHEIGHT -1)

    wormCoords2 = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    #direction awal aj ini 
    direction1 = RIGHT
    direction2 = RIGHT
    running_ = True


    # Start the apple in a random place.
    apple = getRandomLocation(wormCoords1, wormCoords2)

    #buat ngitung distance array
    cal_distance(wormCoords1, wormCoords2)

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()

        #ini kek nampung distance dari 4 macam gerakan ke apple vroh
        four_dis1 = [99999, 99999, 99999, 99999] 
        four_dis2 = [99999, 99999, 99999, 99999]
        

        #ini buat nampung cost dari 4 macam gerakan
        #snake1
        if can_move((wormCoords1[HEAD]['x'], wormCoords1[HEAD]['y'] - 1), wormCoords1, wormCoords2):
            four_dis1[0] = distance1[wormCoords1[HEAD]['y'] - 1][wormCoords1[HEAD]['x']]

        if can_move((wormCoords1[HEAD]['x'] + 1, wormCoords1[HEAD]['y']), wormCoords1, wormCoords2):
            four_dis1[1] = distance1[wormCoords1[HEAD]['y']][wormCoords1[HEAD]['x'] + 1]

        if can_move((wormCoords1[HEAD]['x'], wormCoords1[HEAD]['y'] + 1), wormCoords1, wormCoords2):
            four_dis1[2] = distance1[wormCoords1[HEAD]['y'] + 1][wormCoords1[HEAD]['x']]

        if can_move((wormCoords1[HEAD]['x'] - 1, wormCoords1[HEAD]['y']), wormCoords1, wormCoords2):
            four_dis1[3] = distance1[wormCoords1[HEAD]['y']][wormCoords1[HEAD]['x'] - 1]
        
        #snake2
        if can_move((wormCoords2[HEAD]['x'], wormCoords2[HEAD]['y'] - 1), wormCoords2, wormCoords1):
            four_dis2[0] = distance2[wormCoords2[HEAD]['y'] - 1][wormCoords2[HEAD]['x']]

        if can_move((wormCoords2[HEAD]['x'] + 1, wormCoords2[HEAD]['y']), wormCoords2, wormCoords1):
            four_dis2[1] = distance2[wormCoords2[HEAD]['y']][wormCoords2[HEAD]['x'] + 1]

        if can_move((wormCoords2[HEAD]['x'], wormCoords2[HEAD]['y'] + 1), wormCoords2, wormCoords1):
            four_dis2[2] = distance2[wormCoords2[HEAD]['y'] + 1][wormCoords2[HEAD]['x']]

        if can_move((wormCoords2[HEAD]['x'] - 1, wormCoords2[HEAD]['y']), wormCoords2, wormCoords1):
            four_dis2[3] = distance2[wormCoords2[HEAD]['y']][wormCoords2[HEAD]['x'] - 1]

        #sini buat milih yang paling kecil costnya
        min_num1 = min(four_dis1)
        min_num2 = min(four_dis2)

        
        #yang di sini buat milih direksi yang mana cost nya kecil 
        #snake 1
        if four_dis1[0] < 99999 and distance1[wormCoords1[HEAD]['y'] - 1][wormCoords1[HEAD]['x']] == min_num1 and direction1 != DOWN:
            direction1 = UP

        elif four_dis1[1] < 99999 and distance1[wormCoords1[HEAD]['y']][wormCoords1[HEAD]['x'] + 1] == min_num1 and direction1 != LEFT:
            direction1 = RIGHT

        elif four_dis1[2] < 99999 and distance1[wormCoords1[HEAD]['y'] + 1][wormCoords1[HEAD]['x']] == min_num1 and direction1 != UP:
            direction1 = DOWN

        elif four_dis1[3] < 99999 and distance1[wormCoords1[HEAD]['y']][wormCoords1[HEAD]['x'] - 1] == min_num1 and direction1 != RIGHT:
            direction1 = LEFT
        else:
            #snake 1
            print('alt move 1')
            index_ = 0
            for i in range(4):
                temp = update_dirc(wormCoords1[HEAD],DIRECTION[i])
                temp = (temp['x'], temp['y'])
                if can_move(temp,wormCoords1, wormCoords2):
                    index_ = i
                    break
            direction_new = DIRECTION[index_]
            if direction1 == UP:
                if direction_new != DOWN:
                    direction1 = direction_new
            elif direction1 == DOWN:
                if direction_new != UP:
                    direction1 = direction_new
            elif direction1 == RIGHT:
                if direction_new != LEFT:
                    direction1 = direction_new            
            elif direction1 == LEFT:
                if direction_new != RIGHT:
                    direction1 = direction_new
        
        #snake 2
        if four_dis2[0] < 99999 and distance2[wormCoords2[HEAD]['y'] - 1][wormCoords2[HEAD]['x']] == min_num2 and direction2 != DOWN:
            direction2 = UP

        elif four_dis2[1] < 99999 and distance2[wormCoords2[HEAD]['y']][wormCoords2[HEAD]['x'] + 1] == min_num2 and direction2 != LEFT:
            direction2 = RIGHT

        elif four_dis2[2] < 99999 and distance2[wormCoords2[HEAD]['y'] + 1][wormCoords2[HEAD]['x']] == min_num2 and direction2 != UP:
            direction2 = DOWN

        elif four_dis2[3] < 99999 and distance2[wormCoords2[HEAD]['y']][wormCoords2[HEAD]['x'] - 1] == min_num2 and direction2 != RIGHT:
            direction2 = LEFT

        else:
            #snake 2
            print('alt move 2')
            index_ = 0
            for i in range(4):
                temp = update_dirc(wormCoords2[HEAD],DIRECTION[i])
                temp = (temp['x'], temp['y'])
                if can_move(temp,wormCoords2, wormCoords1):
                    index_ = i
                    break
            direction_new = DIRECTION[index_]
            if direction2 == UP:
                if direction_new != DOWN:
                    direction2 = direction_new
            elif direction2 == DOWN:
                if direction_new != UP:
                    direction2 = direction_new
            elif direction2 == RIGHT:
                if direction_new != LEFT:
                    direction2 = direction_new            
            elif direction2 == LEFT:
                if direction_new != RIGHT:
                    direction2 = direction_new
        

        #check if the worm 1 or worm 2 has hit one the the another worm head or  the edge
        if wormCoords1[HEAD]['x'] == -1 or wormCoords1[HEAD]['x'] == CELLWIDTH or wormCoords1[HEAD]['y'] == -1 or wormCoords1[HEAD]['y'] == CELLHEIGHT \
            or wormCoords2[HEAD]['x'] == -1 or wormCoords2[HEAD]['x'] == CELLWIDTH or wormCoords2[HEAD]['y'] == -1 or wormCoords2[HEAD]['y'] == CELLHEIGHT \
            or (wormCoords2[HEAD]['x'] == wormCoords1[HEAD]['x'] and wormCoords2[HEAD]['y'] == wormCoords1[HEAD]['y']) :
            return # game over


        test = [*wormCoords1[1:],*wormCoords2[1:]] #combine snake1 and snake2 coordinate

        #check if worm 1 or worm 2 head hit their own body or another worm body
        for wormBody in test:
            if (wormBody['x'] == wormCoords1[HEAD]['x'] and wormBody['y'] == wormCoords1[HEAD]['y']) or (wormBody['x'] == wormCoords2[HEAD]['x'] and wormBody['y'] == wormCoords2[HEAD]['y']):
                return # game over
        

        # check if worm1 or 2 has eaten an apple
        if wormCoords1[HEAD]['x'] == apple['x'] and wormCoords1[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation(wormCoords1, wormCoords2) # set a new apple somewhere
        else:
            del wormCoords1[-1] # remove worm's tail segment

        if wormCoords2[HEAD]['x'] == apple['x'] and wormCoords2[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation(wormCoords1, wormCoords2) # set a new apple somewhere
        else:
            del wormCoords2[-1] # remove worm's tail segment

        # move the worm1 and 2 by adding a segment in the direction it is moving (also add new head to snake)
        if direction1 == UP:
            newHead1 = {'x': wormCoords1[HEAD]['x'], 'y': wormCoords1[HEAD]['y'] - 1}
        elif direction1 == DOWN:
            newHead1 = {'x': wormCoords1[HEAD]['x'], 'y': wormCoords1[HEAD]['y'] + 1}
        elif direction1 == LEFT:
            newHead1 = {'x': wormCoords1[HEAD]['x'] - 1, 'y': wormCoords1[HEAD]['y']}
        elif direction1 == RIGHT:
            newHead1 = {'x': wormCoords1[HEAD]['x'] + 1, 'y': wormCoords1[HEAD]['y']}
        
        if direction2 == UP:
            newHead2 = {'x': wormCoords2[HEAD]['x'], 'y': wormCoords2[HEAD]['y'] - 1}
        elif direction2 == DOWN:
            newHead2 = {'x': wormCoords2[HEAD]['x'], 'y': wormCoords2[HEAD]['y'] + 1}
        elif direction2 == LEFT:
            newHead2 = {'x': wormCoords2[HEAD]['x'] - 1, 'y': wormCoords2[HEAD]['y']}
        elif direction2 == RIGHT:
            newHead2 = {'x': wormCoords2[HEAD]['x'] + 1, 'y': wormCoords2[HEAD]['y']}
        
        #insert new head to worm coordinate
        wormCoords1.insert(0, newHead1)
        wormCoords2.insert(0, newHead2)

        # #calculate tile distance from apple
        cal_distance(wormCoords1, wormCoords2)

        #draw background
        DISPLAYSURF.fill(BGCOLOR)

        #draw grid
        drawGrid()

        #draw worm
        drawWorm1(wormCoords1)
        drawWorm2(wormCoords2)

        #draw apple
        drawApple(apple)

        #draw score
        drawScore(len(wormCoords1) - 3, len(wormCoords2) - 3)
        pygame.display.update() #update current screen (like repaint)
        FPSCLOCK.tick(FPS) #set game frame

def drawPressKeyMsg():
    #function to draw message in the bottom right corner
    pressKeySurf = BASICFONT.render('Press c to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.bottomright = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    #check if key is pressed and return the key number
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    #show the title menu
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Dijktra', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('A*', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress() == 99:
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        # #FPSCLOCK.tick(FPS)
        # degrees1 += 3 # rotate by 3 degrees each frame
        # degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    #quit the window and the game
    pygame.quit()
    sys.exit()

def getRandomLocation(worm1, worm2):
    temp = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    while test_not_ok(temp, worm1) or test_not_ok(temp, worm2):
        temp = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    return temp


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress() == 99: #if key pressed is 'c'
            pygame.event.get() # clear event queue
            return

def drawScore(score1, score2):
    #method for drawing score
    scoreSurf = BASICFONT.render('Score1: %s , Score2: %s' % (score1, score2), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 200, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm1(wormCoords):
    #method for drawing the worm
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

def drawWorm2(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

running_ = True

if __name__ == '__main__':
    main()