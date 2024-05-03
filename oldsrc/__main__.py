"""
A Simple 3D Pong game made in Ursina Engine / Python
Author: Marcio Dantas
---
Python 3.9
"""

from ursina import *
from time import sleep

def reset_ball():
    ball.x = 0
    ball.z = 0


def update():
    global dx, dz
    global score_A, score_B

    # Paddle B control
    paddle_B.x = paddle_B.x + held_keys['right arrow'] * time.dt
    paddle_B.x = paddle_B.x - held_keys['left arrow'] * time.dt

    # Paddle A control
    paddle_A.x = paddle_A.x + held_keys['d'] * time.dt
    paddle_A.x = paddle_A.x - held_keys['a'] * time.dt

    # Ball control
    ball.x = ball.x + time.dt*2 * dx
    ball.z = ball.z + time.dt*2 * dz

    # Ball collisions
    hit_info = ball.intersects()

    if hit_info.hit:
        if hit_info.entity == paddle_A or hit_info.entity == paddle_B:
            Audio("res/hit.wav")
            dz = -dz

    # Table left and right border check
    if abs(ball.x) > .4:
        dx = -dx

    # Table bottom and top border check
    if ball.z > .25:
        Audio("res/error.wav")
        score_B += 1
        print_on_screen(f"Player A: {score_A}, Player B: {score_B}", position=(-.85, .45), scale=2, duration=1)

        if score_B >= 10:
            sleep(2)
            exit()

        reset_ball()

    if ball.z < -.65:
        Audio("res/error.wav")
        score_A += 1
        print_on_screen(f"Player A: {score_A}, Player B: {score_B}", position=(-.85, .45), scale=2, duration=1)

        if score_A >= 10:
            sleep(2)
            exit()

        reset_ball()

    # Other
    if held_keys['s']:
        Audio("res/start.wav", volume=.3)
        info_press.visible = False
        dx = .1
        dz = .2


app = Ursina()
window.color = color.orange

table = Entity(model="cube", color=color.green, scale=(10, .5, 14), position=(0, 0, 0), texture='white_cube')

paddle_A = Entity(parent=table, color=color.black, model="cube", scale=(.2, .03, .05), position=(0, 3.7, .22), collider="box")
line = Entity(parent=table, color=color.rgba(0, 0, 0, 0), model="quad", scale=(.88, .2, .1), position=(0, 3.5, -.2))
paddle_B = Entity(parent=table, color=color.black, model="cube", scale=(.2, .03, .05), position=(0, 3.7, -.62), collider="box")
ball = Entity(parent=table, model="sphere", color=color.red, scale=.05, position=(0, 3.71, -.2), collider="box")

camera.position = (0, 15, -26)
camera.rotation_x = 30

# UI
Text(text="Player A", scale=2, position=(-.1, .32))
Text(text="Player B", scale=2, position=(-.1, -.4))
info_press = Text(text="Press [S] to start", scale=3, position=(.2, .4))

score_A = 0
score_B = 0
dx = 0
dz = 0

app.run()
