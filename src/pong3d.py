from ursina import *
from ursina.shaders import lit_with_shadows_shader

DIRECTION = Vec3(3.5, 0, 3.5)

game = Ursina(title="Pong3D", borderless=False,
              size=(800, 600), development_mode=False)

window.color = color.white
camera.position = (0, 15, -26)
camera.rotation_x = 30

paused = True

table = Entity(model="cube", shader=lit_with_shadows_shader,
               color=color.blue, scale=(10, .2, 14),
               position=(0, 0, 0), texture="white_cube")

top_paddle = Entity(color=color.red, shader=lit_with_shadows_shader,
                    model="cube", scale=(3, .5, .5),
                    position=(0, .4, 7), collider="box",
                    texture="white_cube")

left_wall = duplicate(table, color=color.white10,
                      rotation=(0, 90, 0), scale=(14, 1, .1),
                      position=(5, .5, 0), collider="box")

right_wall = duplicate(left_wall, position=(-5, .5, 0))

top_wall = duplicate(left_wall, visible=False, rotation=(0, 0, 0),
                     scale=(10, 1, .1), position=(0, .5, 7))

bottom_wall = duplicate(top_wall, position=(0, .5, -7))

bottom_paddle = duplicate(top_paddle, position=(0, .5, -7))

ball = Entity(direction=DIRECTION, model="sphere",
              color=color.white, scale=.5, position=(0, .4, 0),
              collider="box")

light = Entity()
DirectionalLight(parent=light, y=2, z=3, shadows=True, rotation=(45, -45, 45))

p1 = 0
p2 = 0
MAX_SCORE = 5

score_text = Text(text=f"P1 {p1}x{p2} P2", color=color.black, position=(
    0, .4), origin=(0, 0), scale=2)

hit = Audio("assets/hit.wav", autoplay=False)
point = Audio("assets/point.wav", autoplay=False)
gameover = Audio("assets/gameover.wav", autoplay=False)


def update():
    if paused:
        return
    global p1, p2
    top_paddle.x += (held_keys['d'] - held_keys['a']) * time.dt * 4
    bottom_paddle.x += (held_keys['right arrow'] -
                        held_keys['left arrow']) * time.dt * 4
    ball.position += ball.direction * time.dt

    collision = ball.intersects()
    if collision.hit:
        if collision.entity in (top_paddle, bottom_paddle):
            hit.play()
            ball.direction.z *= -1
            ball.direction *= 1.1
        elif collision.entity in (right_wall, left_wall):
            hit.play()
            ball.direction.x *= -1

        if collision.entity == top_wall:
            p1 += 1
            reset()
        elif collision.entity == bottom_wall:
            p2 += 1
            reset()

        score_text.text = f"P1 {p1}x{p2} P2"

        if MAX_SCORE in (p1, p2):
            gameover.play()
            game_over()


def reset():
    global paused
    point.play()
    paused = False
    ball.position = (0, .4, 0)
    ball.direction = DIRECTION
    score_text.text = f"P1 {p1}x{p2} P2"


def game_over():
    global p1, p2, paused
    paused = True
    p1 = 0
    p2 = 0
    invoke(reset, delay=3)


def input(key):
    global paused
    if key == "space":
        paused = not paused
    if key == "escape":
        game.destroy()


def main() -> None:
    game.run()


if __name__ == "__main__":
    main()
