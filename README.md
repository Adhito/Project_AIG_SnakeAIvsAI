# Project of COMP7084 - Artificial Intelligence in Games



<h4><strong> Team Member </strong></h4>
<ul> 
	<li> 2101664624 -  Anindhito Irmandharu </li>
	<li> 2101685351 -  Gusti Sadhu Jnanin Werkodara </li>
	<li> 2101655720 -  Gerry Gelvianlo </li>
	<li> 2101649592 -  Braja  </li>
	<li> 2101661175 -  Erik Godianto </li>

</ul>


[LinkedIn Anindhito Irmandharu](http://linkedin.com/in/anindhito-irmandharu) <br>
[LinkedIn Gusti Sadhu  ](https://id.linkedin.com/in/gusti-sadhu-jnanin-werkodara-2b1a01194) <br>
[LinkedIn Gerry Gelvianlo  ](https://www.linkedin.com/in/gerry-gelvianlo-8311b01a0) <br>
[LinkedIn Braja   ](https://www.linkedin.com/in/braja-tannady-86ab80194) <br>
[LinkedIn Erik Godianto  ](https://www.linkedin.com/in/erik-godianto-ba2a4a181) <br>


  <br/>
<h4><strong>  Requirement </strong></h4>

<pre>
  <code>
  1. PyGame 1.6 or newer
  2. Python 3.6 or newer
  </code>
</pre>


### AI Algorithm that are used 
In this code we would like to make a comparison between two different algorithm , The first algorithm are A-Star algorithm which can be found in Green Snake. For the second algorithm we use Dijkstra Algorithm's and can be found on the White Snake

### AI version 1 - Based on A-Star Algorithm
A-Star has similar complexity with Dijkstra but with added heuristic for each distance calculation.Heuristic that are used are longest path by following tail which mean the closer the snake to the tail, the smaller the cost is. This added code make the path taking more longer but makes the snake more agile (less crashing to each other).
``` python
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
```
<br>
  
### AI version 2 - Dijkstra Shortest Path Algorithm
A simple BFS strategy make the snake trapped in local optimal point and not considering future.

``` python
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
	if distance2[grid[1]][grid[0]] != 99999:
	    distance2[grid[1]][grid[0]] = distance2[head[1]][head[0]] + 1 
queue2.pop(0)
```
<br>  

<hr>
To visualize the clash of two different algorithm our team decide to use PyGame as a method for visualizing. We choose PyGame since it is one of the popular libraries and understandable to use. Below are the code that helps us visualize the two algorithm (A-Star and Dijkstra) that are used by Snakes at work.

<br>

The code snippet below are the key function and validation of how our program works but does not explain all function that are found in the source code. For further detail please refer to the python source code file

### Starting the program
Starting the Snake game program. FPSLOCK can be change to make game frame-per-second more faster or lower.
``` python
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init() #ini kyk frame set visible 
    
    # Set FPS 
    FPSCLOCK = pygame.time.Clock() 
    
    # Set display size
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    # Set the font 
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)  
    pygame.display.set_caption('Snaky Game') 

    showStartScreen() 
    while True: 
        runGame() 
        showGameOverScreen() 
```

### Initialize a random point.
Initialize random start point for snake 1 and snake 2.
``` python

    startx = random.randint(0, CELLWIDTH -1)
    starty = random.randint(0, CELLHEIGHT -1)
    wormCoords1 = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]


    startx = random.randint(0, CELLWIDTH -1)
    starty = random.randint(0, CELLHEIGHT -1)

    wormCoords2 = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
```


### Validation and Initialize Apple at a random location
Putting an apple at a random location with validation to ensure the apple does not spawn within the snake body
``` python
def getRandomLocation(worm1, worm2):
    temp = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    while test_not_ok(temp, worm1) or test_not_ok(temp, worm2):
	temp = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    return temp
    
	.
	.
	.
	

apple = getRandomLocation(wormCoords1, wormCoords2)
cal_distance(wormCoords1, wormCoords2)
```

<hr>

### Validation for snake's when eating Apples
When the snake eats an apple the corresponding snake should get longer according to how many Apple they eat.
``` python

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

```


### Validation for snake's body when hitting each other 
We added validation condition when the snake dies, and those are : 
<ul> 
	<li> When the snake has hit one of the other head or body. </li>
	<li> When the snake has hit its own body </li>
	<li> When the snake has hit the edge of the map </li>

</ul>

For the time being we do not add time-limit restriction so the snakes are free to compete without any time limit

``` python

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

```



### Validation for snake's to try avoid other snakes 
In the code snippet below are code for the snake's to try avoid hitting each other. 
``` python
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
```
