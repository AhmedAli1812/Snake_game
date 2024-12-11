import tkinter as tk
import random

# إعداد نافذة اللعبة
window = tk.Tk()
window.title("Snake Game")
window.geometry("600x550")
window.configure(bg="#282C34")
window.resizable(False, False)

# إعداد القماش للرسم
canvas = tk.Canvas(window, width=600, height=400, bg="#1E1E1E", highlightthickness=0)
canvas.pack(pady=10)

# إعداد اللعبة
SNAKE_COLOR = "#98C379"
FOOD_COLOR = "#E06C75"
CELL_SIZE = 20
DIRECTIONS = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}

# بدء اللعبة
snake = [(5, 5), (4, 5), (3, 5)]
snake_dir = "Right"
food_pos = (10, 10)
game_running = True

# رسم الشبكة الأولية

def draw_cell(position, color):
    x, y = position
    x1, y1 = x * CELL_SIZE, y * CELL_SIZE
    x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

# تحديث اللعبة

def update_game():
    global snake, food_pos, game_running

    if not game_running:
        return

    # حساب الرأس الجديد
    head_x, head_y = snake[0]
    dir_x, dir_y = DIRECTIONS[snake_dir]
    new_head = (head_x + dir_x, head_y + dir_y)

    # تحقق من التصادم
    if (
        new_head in snake or
        new_head[0] < 0 or new_head[1] < 0 or
        new_head[0] * CELL_SIZE >= 600 or new_head[1] * CELL_SIZE >= 400
    ):
        game_running = False
        canvas.create_text(300, 200, text="Game Over!", fill="white", font=("Arial", 24, "bold"))
        return

    # تحديث الثعبان
    snake.insert(0, new_head)
    if new_head == food_pos:
        place_food()
    else:
        tail = snake.pop()
        draw_cell(tail, "#1E1E1E")

    draw_cell(new_head, SNAKE_COLOR)
    window.after(100, update_game)

# وضع الطعام الجديد

def place_food():
    global food_pos
    while True:
        x = random.randint(0, 29)
        y = random.randint(0, 19)
        if (x, y) not in snake:
            food_pos = (x, y)
            draw_cell(food_pos, FOOD_COLOR)
            break

# تغيير الاتجاه

def change_direction(event):
    global snake_dir
    if event.keysym in DIRECTIONS:
        new_dir = event.keysym
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_dir != opposite[snake_dir]:
            snake_dir = new_dir

# إعادة تشغيل اللعبة

def restart_game():
    global snake, snake_dir, food_pos, game_running
    canvas.delete("all")
    snake = [(5, 5), (4, 5), (3, 5)]
    snake_dir = "Right"
    food_pos = (10, 10)
    game_running = True
    place_food()
    update_game()

# إنهاء اللعبة

def exit_game():
    window.destroy()

# إعداد الأزرار مع تحسين التصميم
button_frame = tk.Frame(window, bg="#282C34")
button_frame.pack(pady=10)

restart_button = tk.Button(button_frame, text="Restart", command=restart_game, font=("Arial", 14, "bold"), bg="#61AFEF", fg="white", width=12, height=1)
restart_button.pack(side="left", padx=15)

exit_button = tk.Button(button_frame, text="Exit", command=exit_game, font=("Arial", 14, "bold"), bg="#E06C75", fg="white", width=12, height=1)
exit_button.pack(side="right", padx=15)

# ربط لوحة المفاتيح وتحديث اللعبة
window.bind("<Key>", change_direction)
place_food()
update_game()

window.mainloop()

