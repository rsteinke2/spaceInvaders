import turtle
import time
import random

def create_custom_alien():
    alien_shape_coords = [
        (0.0, 0.0), (-15.0, -10.0), (-10.0, -10.0), (-32.5, -15.0), (-32.5, 0.0),
        (-32.5, 15.0), (-10.0, 10.0), (-15.0, 10.0), (0.0, 0.0)
    ]
    alien_shape_coords = tuple(alien_shape_coords)
    turtle.register_shape("custom_alien", alien_shape_coords)

def create_custom_player():
    player_shape_coords = [
        (0.0, 0.0), (3.75, -7.5), (15.0, -15.0), (15.0, -22.5), (26.25, -30.0),
        (-26.25, -30.0), (-15.0, -22.5), (-15.0, -15.0), (-3.75, -7.5), (0.0, 0.0)
    ]
    player_shape_coords = tuple(player_shape_coords)
    turtle.register_shape("custom_player", player_shape_coords)

#game window
window = turtle.Screen()
window.title("Space Invaders")
window.bgcolor("black")
window.setup(width=1024, height=768)
window.tracer(0)

#custom alien shape
create_custom_alien()
create_custom_player()

# Player's spaceship
player = turtle.Turtle()
player.shape("custom_player")
player.color("white")
player.penup()
player.goto(0, -250)
player.setheading(90)

# Player movement
def move_left():
    x = player.xcor()
    x -= 20
    if x < -380:
        x = -380
    player.setx(x)

def move_right():
    x = player.xcor()
    x += 20
    if x > 380:
        x = 380
    player.setx(x)

window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")

# Aliens
aliens = []
def create_alien_wave():
    global aliens
    aliens.clear()
    for i in range(5):
        for j in range(6):
            alien = turtle.Turtle()
            alien.shape("custom_alien")
            alien.color("purple")
            alien.penup()
            alien.goto(-200 + j * 80, 300 - i * 60)
            aliens.append(alien)

create_alien_wave()

# Barriers
barriers = []

def create_barriers():
    global barriers
    barriers.clear()
    for i in range(6):
        for j in range(2):  # Two rows of barriers
            barrier = turtle.Turtle()
            barrier.shape("square")
            barrier.color("green")
            barrier.penup()
            barrier.shapesize(stretch_wid=1, stretch_len=2)
            barrier.goto(-200 + i * 80, -200 + j * 40)
            barriers.append(barrier)

create_barriers()

# Bullet
bullet = turtle.Turtle()
bullet.shape("triangle")
bullet.color("yellow")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)
bullet.hideturtle()

bullet_speed = 20
bullet_state = "ready"

# Alien Rockets
alien_rockets = []

def create_alien_rocket():
    rocket = turtle.Turtle()
    rocket.shape("square")
    rocket.color("red")
    rocket.penup()
    rocket.speed(0)
    rocket.shapesize(stretch_wid=0.5, stretch_len=1)
    rocket.setheading(270)
    rocket.hideturtle()
    alien_rockets.append(rocket)

for _ in range(5):
    create_alien_rocket()

# Score
score = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(400, 340)
score_display.write(f"Score: {score}", align="right", font=("Courier", 16, "normal"))

def update_score(points):
    global score
    score += points
    score_display.clear()
    score_display.write(f"Score: {score}", align="right", font=("Courier", 16, "normal"))

# Game Over / Win
is_game_over = False

def game_over():
    global is_game_over
    is_game_over = True
    game_over_display = turtle.Turtle()
    game_over_display.speed(0)
    game_over_display.color("red")
    game_over_display.penup()
    game_over_display.hideturtle()
    game_over_display.goto(0, 0)
    game_over_display.write("GAME OVER", align="center", font=("Courier", 24, "bold"))
    window.update()
    time.sleep(2)
    window.bye()

def player_wins():
    global is_game_over
    is_game_over = True
    remaining_barrier_score = len(barriers) * 1000
    update_score(remaining_barrier_score)
    win_display = turtle.Turtle()
    win_display.speed(0)
    win_display.color("green")
    win_display.penup()
    win_display.hideturtle()
    win_display.goto(0, 0)
    win_display.write("YOU WIN!", align="center", font=("Courier", 24, "bold"))
    window.update()
    time.sleep(2)
    window.bye()

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.goto(x, y)
        bullet.showturtle()

def move_bullet():
    global bullet_state
    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)
        if y > 275:
            bullet.hideturtle()
            bullet_state = "ready"

def fire_alien_rocket():
    if aliens and not is_game_over:
        alien = random.choice(aliens)
        for rocket in alien_rockets:
            if not rocket.isvisible():
                rocket.goto(alien.xcor(), alien.ycor())
                rocket.showturtle()
                break
    window.ontimer(fire_alien_rocket, random.randint(2000, 5000))

def move_alien_rockets():
    for rocket in alien_rockets:
        if rocket.isvisible():
            rocket.sety(rocket.ycor() - 10)
            if rocket.ycor() < -300:
                rocket.hideturtle()
            elif is_collision(rocket, player):
                game_over()
            else:
                for barrier in barriers[:]:
                    if is_collision(rocket, barrier):
                        rocket.hideturtle()
                        barrier.hideturtle()
                        barriers.remove(barrier)
                        break

def is_collision(t1, t2):
    distance = t1.distance(t2)
    return distance < 20

def move_aliens():
    global aliens
    if not aliens and not is_game_over:
        player_wins()
        return

    for alien in aliens:
        y = alien.ycor()
        y -= 10
        alien.sety(y)
        if y < -240 or is_collision(alien, player):
            game_over()
            return

    window.ontimer(move_aliens, 1000)

window.onkeypress(fire_bullet, "space")
window.ontimer(move_aliens, 1000)
window.ontimer(fire_alien_rocket, 2000)

# game loop
while not is_game_over:
    window.update()
    move_bullet()
    move_alien_rockets()

    for alien in aliens[:]:
        if is_collision(bullet, alien):
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.goto(0, -400)
            alien.hideturtle()
            aliens.remove(alien)
            update_score(100)

    time.sleep(0.05)
