import tkinter
from tkinter import *
import tk
from tkextrafont import Font
from pathlib import Path
import random

# TODO LIST
# Pause button, sound effects, high score, levels


# GAME SETTINGS
GAME_RUNNING = None
GAME_PAUSED = False
GAME_OVER = False
GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 300
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = '#ebe134'
FOOD_COLOR = '#eb4034'
BACKGROUND_COLOR = '#000000'

# CLASSES
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tags="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH//SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT//SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOR, tags="food")

# FUNCTIONS
def next_turn():
    global GAME_RUNNING, score, food

    if GAME_PAUSED:
        return

    global GAME_RUNNING
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text = f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        GAME_RUNNING = window.after(SPEED, next_turn)

def change_direction(new_direction):
    if GAME_PAUSED:
        return

    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    global GAME_OVER

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=custom_font, text="GAME OVER", fill="white")
    GAME_OVER = True

def restart_game(event=None):
    global snake, food, score, direction, GAME_RUNNING, GAME_PAUSED, GAME_OVER

    GAME_OVER = False
    GAME_PAUSED = False

    if GAME_RUNNING is not None:
        window.after_cancel(GAME_RUNNING)

    canvas.delete(ALL)

    score = 0
    direction = 'right'
    label.config(text = f"Score: {score}")

    snake = Snake()
    food = Food()

    next_turn()


def pause_game(event=None):
    global GAME_PAUSED, GAME_RUNNING, GAME_OVER

    if not GAME_OVER:
        if not GAME_PAUSED:
            GAME_PAUSED = True
            if GAME_RUNNING is not None:
                window.after_cancel(GAME_RUNNING)
            canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, font=custom_font, text="PAUSED", fill="white", tags="pause_text")
        else:
            GAME_PAUSED = False
            canvas.delete("pause_text")
            next_turn()


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'right'

font_path = Path(__file__).parent / 'RetroGaming.ttf'
custom_font = Font(file = str(font_path), family = "Retro Gaming", weight = 'bold', size = 30)

label  = Label(window, text = f"Score: {score}", font = custom_font)
label.grid(row = 0, column = 0)
restart = Button(window, text = "Restart", command = restart_game, font = custom_font, pady = 0)
restart.grid(row = 0, column = 1, pady = 10)

canvas = Canvas(window, bg = BACKGROUND_COLOR, width = GAME_WIDTH, height = GAME_HEIGHT)
canvas.grid(row = 1, columnspan = 2)

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# ARROW KEY movement binds
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# RESTART binds
window.bind('<Key-R>', restart_game)
window.bind('<Key-r>', restart_game)

# PAUSE binds
window.bind('<Key-P>', pause_game)
window.bind('<Key-p>', pause_game)

# WASD movement binds
window.bind('<Key-A>', lambda event: change_direction('left'))
window.bind('<Key-D>', lambda event: change_direction('right'))
window.bind('<Key-W>', lambda event: change_direction('up'))
window.bind('<Key-S>', lambda event: change_direction('down'))
window.bind('<Key-a>', lambda event: change_direction('left'))
window.bind('<Key-d>', lambda event: change_direction('right'))
window.bind('<Key-w>', lambda event: change_direction('up'))
window.bind('<Key-s>', lambda event: change_direction('down'))


restart_game()

window.mainloop()
