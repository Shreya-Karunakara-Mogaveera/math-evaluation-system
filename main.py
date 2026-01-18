import turtle
import random
import time

# ---------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------
level = None
score = 0
question_count = 0
max_questions = 5
timer_value = 10
timer_running = False
quiz_start_time = None
progress = {"Easy": [], "Medium": [], "Hard": []}

screen = turtle.Screen()
screen.setup(800, 520)
screen.bgcolor("lightyellow")
screen.title("MATH EVALUATION SYSTEM")

writer = turtle.Turtle()
writer.penup()
writer.hideturtle()

timer_writer = turtle.Turtle()
timer_writer.penup()
timer_writer.hideturtle()

btn_writer = turtle.Turtle()
btn_writer.penup()
btn_writer.hideturtle()

feedback_writer = turtle.Turtle()
feedback_writer.penup()
feedback_writer.hideturtle()

options_boxes = []
option_turtles = []
circle_turtles = []

LETTER_COLORS = {"A": "blue", "B": "forestgreen", "C": "orange", "D": "purple"}

# ---------------------------------------------
# UTILITY FUNCTIONS
# ---------------------------------------------
def draw_circle_label(x, y, letter):
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.goto(x, y - 10)
    t.pendown()
    t.fillcolor(LETTER_COLORS.get(letter, "gray"))
    t.pencolor(LETTER_COLORS.get(letter, "gray"))
    t.begin_fill()
    t.circle(20)
    t.end_fill()
    t.penup()
    t.goto(x, y - 5)
    t.color("white")
    t.write(letter, align="center", font=("Arial", 16, "bold"))
    circle_turtles.append(t)
    return t

def draw_option_button(x, y, text):
    btn = turtle.Turtle()
    btn.penup()
    btn.shape("square")
    btn.shapesize(2, 14)
    btn.color("white", "darkblue")
    btn.goto(x, y)
    btn.showturtle()

    btn_writer.goto(x, y - 10)
    btn_writer.color("white")
    btn_writer.write(text, align="center", font=("Arial", 18, "bold"))

    option_turtles.append(btn)

    x1, y1 = x - 140, y - 30
    x2, y2 = x + 140, y + 30
    return (x1, y1, x2, y2)

def clear_buttons():
    for t in option_turtles:
        t.clear()
        t.hideturtle()
    option_turtles.clear()
    btn_writer.clear()

def clear_circles():
    for t in circle_turtles:
        t.clear()
        t.hideturtle()
    circle_turtles.clear()

def clear_feedback():
    feedback_writer.clear()

def highlight_option(btn, color):
    btn.color("white", color)

# ---------------------------------------------
# WELCOME SCREEN
# ---------------------------------------------
def welcome_screen():
    writer.clear()
    clear_buttons()
    clear_circles()
    timer_writer.clear()
    feedback_writer.clear()

    writer.goto(0, 100)
    writer.write("MATH EVALUATION SYSTEM", align="center", font=("Arial", 36, "bold"))
    writer.goto(0, -50)
    writer.write("Press ENTER to Start", align="center", font=("Arial", 24, "normal"))

    screen.listen()
    screen.onkey(get_ready_countdown, "Return")

# ---------------------------------------------
# COUNTDOWN
# ---------------------------------------------
def get_ready_countdown():
    writer.clear()
    clear_buttons()
    clear_circles()
    clear_feedback()
    timer_writer.clear()
    screen.onkey(None, "Return")

    for i in range(3, 0, -1):
        writer.goto(0, 0)
        writer.write(f"Get Ready! {i}", align="center", font=("Arial", 36, "bold"))
        time.sleep(1)
        writer.clear()

    writer.goto(0, 0)
    writer.write("GO!", align="center", font=("Arial", 36, "bold"))
    time.sleep(1)
    writer.clear()

    choose_level_screen()

# ---------------------------------------------
# LEVEL SELECTION
# ---------------------------------------------
def choose_level_screen():
    writer.clear()
    clear_buttons()
    clear_circles()
    timer_writer.clear()

    writer.goto(0, 190)
    writer.write("CHOOSE LEVEL", align="center", font=("Arial", 28, "bold"))

    global btn_easy, btn_med, btn_hard
    btn_easy = draw_option_button(0, 90, "Easy")
    btn_med = draw_option_button(0, 10, "Medium")
    btn_hard = draw_option_button(0, -70, "Hard")

    screen.onclick(click_level)

def click_level(x, y):
    global level
    if btn_easy[0] < x < btn_easy[2] and btn_easy[1] < y < btn_easy[3]:
        level = "Easy"
    elif btn_med[0] < x < btn_med[2] and btn_med[1] < y < btn_med[3]:
        level = "Medium"
    elif btn_hard[0] < x < btn_hard[2] and btn_hard[1] < y < btn_hard[3]:
        level = "Hard"
    else:
        return

    screen.onclick(None)
    start_quiz()

# ---------------------------------------------
# QUESTION GENERATOR
# ---------------------------------------------
def generate_question(level):
    if level == "Easy":
        ops = ["+", "-"]
        a, b = random.randint(1, 10), random.randint(1, 10)
    elif level == "Medium":
        ops = ["+", "-", "*"]
        a, b = random.randint(10, 20), random.randint(10, 20)
    else:
        ops = ["*", "/"]
        a = random.randint(20, 50)
        b = random.randint(20, 50)
        c = a * b

    op = random.choice(ops)

    if op == "/":
        question = f"{a} / {b} = ?"
        answer = a // b
    else:
        question = f"{a} {op} {b} = ?"
        answer = int(eval(f"{a}{op}{b}"))

    wrongs = set()
    while len(wrongs) < 3:
        w = answer + random.randint(-12, 12)
        if w != answer:
            wrongs.add(w)

    return question, answer, list(wrongs)

# ---------------------------------------------
# TIMER
# ---------------------------------------------
def update_timer():
    global timer_value, timer_running

    if not timer_running:
        return

    timer_writer.clear()
    timer_writer.goto(340, 220)
    timer_writer.color("red")
    timer_writer.write(f"Time: {timer_value}", align="center", font=("Arial", 20, "bold"))

    if timer_value > 0:
        timer_value -= 1
        screen.ontimer(update_timer, 1000)
    else:
        timer_running = False

        # highlight correct answer
        for (box, value, letter), btn in zip(options_boxes, option_turtles):
            if value == current_answer:
                highlight_option(btn, "green")
                break

        feedback_writer.goto(0, -260)
        feedback_writer.color("red")
        feedback_writer.write("⏳ Time's up!", align="center", font=("Arial", 20, "bold"))

        screen.ontimer(next_step, 1500)

# ---------------------------------------------
# ASK QUESTION
# ---------------------------------------------
def ask_question():
    global current_answer, options_boxes, question_count, timer_value, timer_running

    writer.clear()
    clear_buttons()
    clear_circles()
    clear_feedback()
    timer_writer.clear()

    q, correct, wrong_list = generate_question(level)
    current_answer = correct
    question_count += 1

    writer.goto(0, 180)
    writer.write(f"{level} Level - Question {question_count}/{max_questions}", align="center", font=("Arial", 20, "bold"))

    writer.goto(0, 120)
    writer.write(q, align="center", font=("Arial", 26, "bold"))

    answers = wrong_list + [correct]
    random.shuffle(answers)
    letters = ["A", "B", "C", "D"]

    options_boxes.clear()
    circle_x = -240
    button_x = 160
    y_positions = [40, -40, -120, -200]

    for i in range(4):
        draw_circle_label(circle_x, y_positions[i], letters[i])
        hitbox = draw_option_button(button_x, y_positions[i], str(answers[i]))
        options_boxes.append((hitbox, answers[i], letters[i]))

    timer_value = 10
    timer_running = True
    update_timer()

    screen.onclick(click_answer)

# ---------------------------------------------
# ANSWER CLICK
# ---------------------------------------------
def click_answer(x, y):
    global score, timer_running

    if not timer_running:
        return

    timer_running = False
    screen.onclick(None)

    for (box, value, letter), btn in zip(options_boxes, option_turtles):
        if box[0] < x < box[2] and box[1] < y < box[3]:

            if value == current_answer:
                score += 1
                highlight_option(btn, "green")
                feedback_writer.goto(0, -260)
                feedback_writer.color("green")
                feedback_writer.write(f" Correct! ({letter})", align="center", font=("Arial", 20, "bold"))

            else:
                highlight_option(btn, "red")
                # show correct
                for (b2, v2, l2), btn2 in zip(options_boxes, option_turtles):
                    if v2 == current_answer:
                        highlight_option(btn2, "green")
                        break

                feedback_writer.goto(0, -260)
                feedback_writer.color("red")
                feedback_writer.write(f" Wrong! You chose {letter}", align="center", font=("Arial", 20, "bold"))

            screen.ontimer(next_step, 1500)
            return

# ---------------------------------------------
# NEXT STEP
# ---------------------------------------------
def next_step():
    clear_feedback()
    if question_count < max_questions:
        ask_question()
    else:
        end_quiz()

# ---------------------------------------------
# END QUIZ → SHOW SCORE (NO TOTAL TIME)
# ---------------------------------------------
def ask_another_level():
    writer.clear()
    clear_buttons()
    clear_circles()
    clear_feedback()
    timer_writer.clear()

    writer.goto(0, 120)
    writer.write(f"You scored {score}/{max_questions} in {level} level",
                 align="center", font=("Arial", 24, "bold"))

    #  REMOVED TOTAL TIME BASED ON YOUR REQUEST

    writer.goto(0, 40)
    writer.write("Do you want to try another level?\nPress Y for Yes, N for No",
                 align="center", font=("Arial", 20, "normal"))

    screen.listen()
    screen.onkey(try_another_level_yes, "y")
    screen.onkey(try_another_level_no, "n")

def try_another_level_yes():
    screen.onkey(None, "y")
    screen.onkey(None, "n")
    choose_level_screen()

def try_another_level_no():
    screen.onkey(None, "y")
    screen.onkey(None, "n")

    attempts = sum(len(v) for v in progress.values())

    if attempts <= 1:
        # Only one attempt → DO NOT SHOW GRAPH
        writer.clear()
        writer.goto(0, 0)
        writer.write("Thanks for playing!", align="center", font=("Arial", 26, "bold"))
        return

    else:
        # More than one attempt → show graph
        show_progress_graph_turtle()

# ---------------------------------------------
# BAR GRAPH (TURTLE)
# ---------------------------------------------
def show_progress_graph_turtle():
    clear_buttons()
    clear_circles()
    clear_feedback()
    timer_writer.clear()
    writer.clear()

    writer.goto(0, 220)
    writer.write("Quiz Progress", align="center", font=("Arial", 28, "bold"))

    all_scores = [s for scores in progress.values() for s in scores]
    if not all_scores:
        writer.goto(0, 100)
        writer.write("No attempts yet.", align="center", font=("Arial", 18, "normal"))
        return

    max_score = max(all_scores)
    bar_width = 40
    spacing = 80
    start_x = -150
    base_y = -100

    i = 0
    for lvl, scores in progress.items():
        for attempt, s in enumerate(scores):
            bar_height = (s / max_score) * 200 if max_score > 0 else 0

            t = turtle.Turtle()
            t.hideturtle()
            t.penup()
            t.goto(start_x + i * spacing, base_y)
            t.pendown()

            t.fillcolor("green")
            t.begin_fill()
            t.forward(bar_width)
            t.left(90)
            t.forward(bar_height)
            t.left(90)
            t.forward(bar_width)
            t.left(90)
            t.forward(bar_height)
            t.end_fill()

            t.penup()
            t.goto(start_x + i * spacing + bar_width/2, base_y - 20)
            t.write(f"{lvl}-{attempt+1}", align="center", font=("Arial", 10, "normal"))

            i += 1

# ---------------------------------------------
# STORE SCORE THEN ASK NEXT LEVEL
# ---------------------------------------------
def end_quiz():
    progress[level].append(score)
    ask_another_level()

# ---------------------------------------------
# START QUIZ
# ---------------------------------------------
def start_quiz():
    global score, question_count, quiz_start_time
    score = 0
    question_count = 0
    quiz_start_time = time.time()
    ask_question()

# ---------------------------------------------
# RUN
# ---------------------------------------------
welcome_screen()
screen.mainloop()
