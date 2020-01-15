# Project of COMP7084 - Artificial Intelligence in Games



<h4><strong> Team Member </strong></h4>
<ul> 
	<li> 2101664624 -  Anindhito Irmandharu </li>
	<li> 2101664624 -  Anindhito Irmandharu </li>
	<li> 2101664624 -  Anindhito Irmandharu </li>
	<li> 2101664624 -  Anindhito Irmandharu </li>
	<li> 2101664624 -  Anindhito Irmandharu </li>

</ul>


[LinkedID Anindhito Irmandharu](https://www.google.com) <br>
[LinkedID I Gusti Sadhu  ](https://www.google.com) <br>
[LinkedID Braja   ](https://www.google.com) <br>
[LinkedID Gerry Gelvianlo  ](https://www.google.com) <br>
[LinkedID Erik Godianto  ](https://www.google.com) <br>


  <br/>
<h4><strong>  Requirement </strong></h4>

<pre>
  <code>
  1. PyGame 1.6 or newer
  2. Python 3.6 or newer
  </code>
</pre>


### AI Algorithm that are used 
In this code we would like to make a comparison between two different algorithm , The first algorithm are A-Star algorithm which can be found in #COLOR Snake. For the second algorithm we use Dijkstra Algorithm's and can be found on the #COLOR Snake

### AI version 1 - Based on A-Star Algorithm
A perfect strategy, ensuring filling the screen, but the speed is slow.
``` python
while len(queue1) != 0:
head = queue1[0]
visited1.append(head)
up_grid = head[0], head[1] - 1
down_grid = head[0], head[1] + 1
left_grid = head[0] - 1, head[1]
right_grid = head[0] + 1, head[1]

for grid in [up_grid, down_grid, left_grid, right_grid]:
    if into_queue(grid, queue1, visited1,worm1, worm2):
	queue1.append(grid)
	if distance1[grid[1]][grid[0]] != 99999:
	    distance1[grid[1]][grid[0]] = distance1[head[1]][head[0]] + 1 + abs(grid[0] - apple['x']) + abs(grid[1] - apple['y'])
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
To visualize the clash of two different algorithm our team decide to use PyGame as a method for visualizing. We choose PyGame since it is one of the popular libraries and understandable to use.


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


### Initialize Apple at a random location
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


