from ursina import *
from ursina.shaders import lit_with_shadows_shader
from typing import Tuple

MAX_SCORE = 5
VELOCITY = 5.0

paused = True
p1_score = 0
p2_score = 0
hit_sound = None
point_sound = None
background_music = None

top_paddle = None
bottom_paddle = None
ball = None
left_wall = None
right_wall = None
top_wall = None
bottom_wall = None

main_panel = None
game_over_panel = None
pause_menu = None
score_text = None


def setup_window():
    window.color = color.azure
    camera.position = (0, 15, -26)
    camera.rotation_x = 30


def create_audio():
    global point_sound, hit_sound, background_music
    hit_sound = Audio("assets/audio/hit.wav", volume=.1, autoplay=False)
    point_sound = Audio("assets/audio/point.wav", volume=.1, autoplay=False)
    background_music = Audio("assets/audio/romantic.wav", loop=True, autoplay=False)


def create_entities():
    global top_paddle, bottom_paddle, ball, left_wall, right_wall, top_wall, bottom_wall
    ball_mesh = load_model("assets/mesh/ball.obj")
    
    Entity(model="cube", shader=lit_with_shadows_shader, color=color.blue, scale=(10, .2, 14), position=(0, 0, 0), texture="white_cube")
    Entity(model="cube", color=color.blue, scale=(10, .2, .1), position=(0, 0))
    top_paddle = create_paddle(position=(0, .4, 7), color=color.red)
    bottom_paddle = create_paddle(position=(0, .5, -7), color=color.red)
    ball = Entity(direction=Vec3(1, 0, 1), model=ball_mesh, color=color.white, scale=.2, position=(0, .4, 0), collider="box")

    left_wall = create_wall(position=(5, .5, 0), rotation=(0, 90, 0))
    right_wall = create_wall(position=(-5, .5, 0), rotation=(0, 90, 0))
    top_wall = create_wall(position=(0, .5, 7), rotation=(0, 0, 0), visible=False)
    bottom_wall = create_wall(position=(0, .5, -7), rotation=(0, 0, 0), visible=False)


def create_paddle(position, color):
    return Entity(color=color,
                  shader=lit_with_shadows_shader,
                  model="cube",
                  scale=(3, .5, .5),
                  position=position,
                  collider="box",
                  texture="white_cube")


def create_wall(position, rotation, visible=True):
    return Entity(model="cube",
                  shader=lit_with_shadows_shader,
                  color=color.white10,
                  scale=(14, 1, .1),
                  position=position,
                  rotation=rotation,
                  collider="box",
                  visible=visible)


def create_lighting():
    light = Entity()
    DirectionalLight(parent=light,
                     y=2, z=3,
                     shadows=True,
                     rotation=(45, -45, 45))


def create_ui():
    global score_text, main_panel, game_over_panel, pause_menu

    Text.default_font = "assets/font/PlusJakartaSans-ExtraBold.ttf"

    main_panel = WindowPanel(
        title="Pong3D",
        content=(
            Button(text="Play", color=color.blue, on_click=start_game),
            Button(text="Quit", color=color.red, on_click=application.quit),
        ),
        popup=True,
    )
    main_panel.y = main_panel.panel.scale_y / 2 * main_panel.scale_y
    main_panel.layout()
    
    game_over_panel = WindowPanel(
        title="Game Over",
        content=(
            Button(text="Restart Game", color=color.orange, scale=(.2, .1), position=(0, -.05), on_click=restart_game),
            Button(text="Quit", color=color.red, on_click=application.quit),
        ),
        popup=True,
        enabled=False,
    )
    game_over_panel.y = game_over_panel.panel.scale_y / 2 * game_over_panel.scale_y
    game_over_panel.layout()
    
    pause_menu = WindowPanel(
        title="Paused",
        content=(
            Button(text="Resume", color=color.blue, scale=(.2, .1), position=(0, -.05), on_click=resume_game),
            Button(text="Restart Game", color=color.orange, scale=(.2, .1), position=(0, -.05), on_click=restart_game),
            Button(text="Quit", color=color.red, on_click=application.quit),
        ),
        popup=True,
        enabled=False,
    )
    pause_menu.y = pause_menu.panel.scale_y / 2 * pause_menu.scale_y
    pause_menu.layout()

    score_text = Text(text=f"P1 {p1_score}x{p2_score} P2",
                      color=color.white,
                      position=(0, .45),
                      origin=(0, 0),
                      enabled=False,
                      scale=2)


def update():
    if paused:
        return

    update_paddles()
    update_ball()


def update_paddles():
    top_paddle.x += (held_keys['d'] - held_keys['a']) * time.dt * 4
    bottom_paddle.x += (held_keys['right arrow'] - held_keys['left arrow']) * time.dt * 4


def update_ball():
    global p1_score, p2_score

    ball.position += ball.direction * VELOCITY * time.dt
    collision = ball.intersects()

    if collision.hit:
        if collision.entity in (top_paddle, bottom_paddle):
            hit_sound.play()
            ball.direction.z *= -1
        elif collision.entity in (right_wall, left_wall):
            hit_sound.play()
            ball.direction.x *= -1

        check_score(collision.entity)


def check_score(entity):
    global p1_score, p2_score

    if entity == top_wall:
        p1_score += 1
        point_sound.play()
        reset_ball()
    elif entity == bottom_wall:
        p2_score += 1
        point_sound.play()
        reset_ball()

    update_score_text()

    if MAX_SCORE in (p1_score, p2_score):
        game_over()


def reset_ball():
    ball.position = (0, .4, 0)
    ball.direction = Vec3(1, 0, 1)


def update_score_text():
    score_text.text = f"P1 {p1_score}x{p2_score} P2"


def game_over():
    global paused, p1_score, p2_score
    paused = True
    p1_score = 0
    p2_score = 0
    game_over_panel.enable()


def start_game():
    global paused
    paused = False
    score_text.enable()
    main_panel.disable()


def restart_game():
    global paused, p1_score, p2_score
    p1_score = 0
    p2_score = 0
    paused = False
    game_over_panel.disable()
    pause_menu.disable()
    reset_ball()
    update_score_text()


def resume_game():
    global paused
    paused = False
    pause_menu.disable()


def input(key):
    global paused
    if key == "escape":
        if not main_panel.enabled and not game_over_panel.enabled:
            paused = not paused
            pause_menu.enabled = not pause_menu.enabled


def main(title: str, size: Tuple[int, int]):
    app = Ursina(title=title,
                 borderless=False,
                 icon="assets/icon.ico",
                 size=size,
                 development_mode=False)

    setup_window()
    create_lighting()
    create_entities()
    create_audio()
    create_ui()
    
    main_panel.enable()
    background_music.play()

    app.run()


if __name__ == "__main__":
    main(title="Pong3D", size=(800, 600))
