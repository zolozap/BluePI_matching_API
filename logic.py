# import modules
from random import *
from turtle import *

# set the screen
screen = Screen()

#choose background color
screen.bgcolor("yellow")

# define the function
# for creating a square section
# for the game
def Square(x, y):
    up()
    goto(x, y)
    down()
    color('white', 'green')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()

# define functionn to
# keep a check of index number
def Numbering(x, y):
    return int((x + 100) // 50 + ((y + 100) // 50) * 4)

# define function
def Coordinates(count):
    return (count % 4) * 50 - 100, (count // 4) * 50 - 100

# define function
# to make it interactive
# user click
def click(x, y):
    spot = Numbering(x, y) 
    print(spot)
    mark = state['mark']

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None

def draw():
    clear()
    goto(0, 0)
    stamp()

    for count in range(12):
        if hide[count]:
            x, y = Coordinates(count)
            Square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = Coordinates(mark)
        up()
        goto(x + 2, y)
        color('black')
        write(tiles[mark], font=('Arial', 30, 'normal'))

    update()
    ontimer(draw, 10)

tiles = list(range(6)) * 2
state = {'mark': None}
hide = [True] * 12

# for shuffling the
# numbers placed inside
# the square tiles
print(tiles)
print(click)
shuffle(tiles)
tracer(False)
onscreenclick(click)
draw()
done()

