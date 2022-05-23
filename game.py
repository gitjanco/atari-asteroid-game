# Janco Megerssa
# Computing ID: jam6nnu
"""Source of help:
   I sought help from office hours so that I could have my asteroids randomly spawn better. I also sought help for
   successfully creating a timer/clock.
"""

"""
This program uses gamebox and pygame to create a game based off of Atari's Asteroids. It is a space themed shooter 
arcade game. The user controls a ship that shoots projectiles. These projectiles will be used to shoot at incoming 
asteroids. The user will need to avoid colliding with these asteroids and make sure they can beat the clock
"""
import gamebox
import pygame
import random

# initialize outside of tick
width = 800
height = 600
score = 0
countdown = 30
true_countdown = 30
ship_xspeed = 11
ship_yspeed = 12
width_health = 300
x_health = 400
start = False
won = False
game_over = False

# camera
camera = gamebox.Camera(width, height)
# Start Screen
start_screen = gamebox.from_image(400, 300, 'Ast-start.jpg')
start_screen.scale_by(1.35)
# background
background = gamebox.from_image(300, 100, 'purple_background.jpg')
# game over background
game_over_background = gamebox.from_image(400, 200, 'GameOver.png')
# You win background
win_screen = gamebox.from_image(380, 200, 'YouWon.jpg')
# borders
top_border = gamebox.from_color(400, 0, "black", 800, 30)
bottom_border = gamebox.from_color(400, 600, "black", 800, 30)
right_border = gamebox.from_color(800, 400, "black", 30, 800)
left_border = gamebox.from_color(0, 200, "black", 30, 8000)
# ship player
ship_sprite = gamebox.load_sprite_sheet("ship_sprite.png", 2, 4)
ship = gamebox.from_image(width / 2, height / 2, ship_sprite[0])
ship.scale_by(0.6)

# ship projectiles
projectile_left_1 = gamebox.from_image(1600, 1600, 'projectile.png')
projectile_left_1.scale_by(0.030)
projectile_left_1.speedx = -20 # projectile speed
projectile_left_2 = gamebox.from_image(1600, 1600, 'projectile.png')
projectile_left_2.scale_by(0.030)
projectile_left_2.speedx = -15 # projectile speed
projectile_left_3 = gamebox.from_image(1600, 1600, 'projectile.png')
projectile_left_3.scale_by(0.030)
projectile_left_3.speedx = -10 # projectile speed
projectile_right_1 = gamebox.from_image(1600, 1600, 'projectile.png')
projectile_right_1.scale_by(0.030)
projectile_right_1.speedx = 10 # projectile speed
projectile_right_2 = gamebox.from_image(1600, 1600, 'projectile.png')
projectile_right_2.scale_by(0.030)
projectile_right_2.speedx = 15 # projectile speed
projectile_right_3 = gamebox.from_image(1600, 1600, 'projectile.png')
projectile_right_3.scale_by(0.030)
projectile_right_3.speedx = 20 # projectile speed
projectile_up_1 = gamebox.from_image(1600, 1600, 'projectile.png')
projectile_up_1.scale_by(0.030)
projectile_up_1.speedy = -20 # projectile speed
projectile_up_2 = gamebox.from_image(1600, 1600, 'projectile.png')
projectile_up_2.scale_by(0.030)
projectile_up_2.speedy = -15 # projectile speed
projectile_up_3 = gamebox.from_image(1600, 1600, 'projectile.png')
projectile_up_3.scale_by(0.030)
projectile_up_3.speedy = -10 # projectile speed

# asteroids
asteroid_1 = gamebox.from_image(50, 50, 'asteroid-transparent-2.png')
asteroid_1.scale_by(0.08)
asteroid_2 = gamebox.from_image(500, 200, 'asteroid-transparent-2.png')
asteroid_2.scale_by(0.08)
asteroid_3 = gamebox.from_image(200, 500, 'asteroid-transparent-2.png')
asteroid_3.scale_by(0.08)

# intro
asteroids_title = gamebox.from_text(400, 150, "WELCOME TO", 100, "white")
start_instructions = gamebox.from_text(400, 570, "Hit S to Start!", 50, "white")
movement_instructions = gamebox.from_text(400, 410, "Use the Up, Down, Right, and Left keys to navigate ship.", 40, "white")
shooting_instructions = gamebox.from_text(400, 440, "Use the W, A, and D keys to shoot projectiles.", 40, "white")
scoring_instructions = gamebox.from_text(400, 470, "Shoot the asteroids to get points!", 40, "green")
lose_health = gamebox.from_text(400, 500, "Avoid getting hit or you'll lose health!", 40, "green")
win_if = gamebox.from_text(400, 535, "Last 30 seconds and you win!!", 40, "white")


def tick(keys):
    """

    :param keys: Input parameter on keyboard for user to hit keys to activate actions in the game such as player movement.
    :return: This function allows for multiple things to be returned. It allows the game "Asteroids" to work. This ranges
    from random asteroids being spawned, movement of spaceship, shooting mechanics and asteroid destruction, menu displays,
    game over screens,timer,health bar, score, and etc.
    """
    # globals
    global start, game_over, countdown, score, width_health, x_health, true_countdown
    camera.clear("black")
    # draw start screen
    camera.draw(start_screen)
    camera.draw(movement_instructions)
    camera.draw(shooting_instructions)
    camera.draw(scoring_instructions)
    camera.draw(lose_health)
    camera.draw(win_if)

    # Start
    if pygame.K_s in keys:
        start = True
    if start:
        countdown -= 1
        true_countdown = int(countdown / 30) + 30
        # draw background
        camera.draw(background)
        # draw borders
        camera.draw(bottom_border)
        camera.draw(top_border)
        camera.draw(left_border)
        camera.draw(right_border)
        # draw asteroids
        asteroid_1.move_speed()
        camera.draw(asteroid_1)
        asteroid_2.move_speed()
        camera.draw(asteroid_2)
        asteroid_3.move_speed()
        camera.draw(asteroid_3)
        # keep ship within borders
        ship.move_to_stop_overlapping(bottom_border)
        ship.move_to_stop_overlapping(top_border)
        ship.move_to_stop_overlapping(left_border)
        ship.move_to_stop_overlapping(right_border)

        # health gameboxes
        full_health = gamebox.from_color(400, 30, "black", 300, 20)
        health = gamebox.from_color(x_health, 30, "green", width_health, 20)

        # Clock gamebox
        clock = gamebox.from_text(100, 30, "TIMER: " + str(true_countdown), 30, "white")
        clock_box = gamebox.from_color(100, 30, "black", 120, 30)

        # ship motion
        if pygame.K_UP in keys:
            ship.y -= ship_yspeed
            ship.image = ship_sprite[4]
        if pygame.K_DOWN in keys:
            ship.y += ship_yspeed
            ship.image = ship_sprite[0]
        if pygame.K_LEFT in keys:
            ship.x -= ship_xspeed
            ship.image = ship_sprite[7]
        if pygame.K_RIGHT in keys:
            ship.x += ship_xspeed
            ship.image = ship_sprite[5]
        # shooting mechanics
        if pygame.K_w in keys:
            projectile_up_1.x = ship.x
            projectile_up_1.y = ship.y
            projectile_up_2.x = ship.x
            projectile_up_2.y = ship.y
            projectile_up_3.x = ship.x
            projectile_up_3.y = ship.y
        if pygame.K_a in keys:
            projectile_left_1.x = ship.x
            projectile_left_1.y = ship.y
            projectile_left_2.x = ship.x
            projectile_left_2.y = ship.y
            projectile_left_3.x = ship.x
            projectile_left_3.y = ship.y
        if pygame.K_d in keys:
            projectile_right_1.x = ship.x
            projectile_right_1.y = ship.y
            projectile_right_2.x = ship.x
            projectile_right_2.y = ship.y
            projectile_right_3.x = ship.x
            projectile_right_3.y = ship.y
        projectile_up_1.move_speed()
        projectile_up_2.move_speed()
        projectile_up_3.move_speed()
        projectile_left_1.move_speed()
        projectile_left_2.move_speed()
        projectile_left_3.move_speed()
        projectile_right_1.move_speed()
        projectile_right_2.move_speed()
        projectile_right_3.move_speed()

        # drawing projectiles after being shot
        camera.draw(projectile_up_1)
        camera.draw(projectile_up_2)
        camera.draw(projectile_up_3)
        camera.draw(projectile_left_1)
        camera.draw(projectile_left_2)
        camera.draw(projectile_left_3)
        camera.draw(projectile_right_1)
        camera.draw(projectile_right_2)
        camera.draw(projectile_right_3)

        # drawing ship
        camera.draw(ship)

        # Asteroid spawning
        if asteroid_1.touches(bottom_border):
            asteroid_1.x = random.randint(0, 800)
            asteroid_1.y = 400
        if asteroid_1.touches(top_border):
            asteroid_1.x = random.randint(0, 800)
            asteroid_1.y = 400
        if asteroid_1.touches(left_border):
            asteroid_1.x = random.randint(0, 800)
            asteroid_1.y = 400
        if asteroid_1.touches(right_border):
            asteroid_1.x = random.randint(0, 800)
            asteroid_1.y = 400
        if asteroid_2.touches(bottom_border):
            asteroid_2.x = random.randint(0, 800)
            asteroid_2.y = 400
        if asteroid_2.touches(top_border):
            asteroid_2.x = random.randint(0, 800)
            asteroid_2.y = 400
        if asteroid_2.touches(left_border):
            asteroid_2.x = random.randint(0, 800)
            asteroid_2.y = 400
        if asteroid_2.touches(right_border):
            asteroid_2.x = random.randint(0, 800)
            asteroid_2.y = 400
        if asteroid_3.touches(bottom_border):
            asteroid_3.x = random.randint(0, 800)
            asteroid_3.y = 400
        if asteroid_3.touches(top_border):
            asteroid_3.x = random.randint(0, 800)
            asteroid_3.y = 400
        if asteroid_3.touches(left_border):
            asteroid_3.x = random.randint(0, 800)
            asteroid_3.y = 400
        if asteroid_3.touches(right_border):
            asteroid_3.x = random.randint(0, 800)
            asteroid_3.y = 400
        asteroid_1.speedx = -1 * 5
        asteroid_1.speedy = -1 * 5
        asteroid_2.speedx = 5
        asteroid_2.speedy = 5
        asteroid_3.speedx = -1 * 5
        asteroid_3.speedy = -1 * 5

        # Collision detection between ship and asteroids
        if ship.touches(asteroid_1):
            asteroid_1.x = 200
            width_health -= 10
            x_health -= 5
        if ship.touches(asteroid_2):
            asteroid_2.x = 600
            width_health -= 10
            x_health -= 5
        if ship.touches(asteroid_3):
            asteroid_3.x = 200
            width_health -= 10
            x_health -= 5
        if width_health == 0:
            game_over = True

        # Collision between projectiles and asteroids
        if asteroid_1.touches(projectile_up_1) or asteroid_1.touches(projectile_up_2) or asteroid_1.touches(
                projectile_up_3) or asteroid_1.touches(projectile_right_1) or asteroid_1.touches(
            projectile_right_2) or asteroid_1.touches(projectile_right_3) or asteroid_1.touches(
            projectile_left_1) or asteroid_1.touches(projectile_left_2) or asteroid_1.touches(projectile_left_3):
            asteroid_1.x = 10
            score += 10
        if asteroid_2.touches(projectile_up_1) or asteroid_2.touches(projectile_up_2) or asteroid_2.touches(
                projectile_up_3) or asteroid_2.touches(projectile_right_1) or asteroid_2.touches(
            projectile_right_2) or asteroid_2.touches(projectile_right_3) or asteroid_2.touches(
            projectile_left_1) or asteroid_2.touches(projectile_left_2) or asteroid_2.touches(projectile_left_3):
            asteroid_2.x = 10
            score += 10
        if asteroid_3.touches(projectile_up_1) or asteroid_3.touches(projectile_up_2) or asteroid_3.touches(
                projectile_up_3) or asteroid_3.touches(projectile_right_1) or asteroid_3.touches(
            projectile_right_2) or asteroid_3.touches(projectile_right_3) or asteroid_3.touches(
            projectile_left_1) or asteroid_3.touches(projectile_left_2) or asteroid_3.touches(projectile_left_3):
            asteroid_3.x = 10
            score += 10

        # score gamebox
        user_score = gamebox.from_text(680, 30, "YOUR SCORE: " + str(score), 30, "white")
        user_score_box = gamebox.from_color(680, 30, "black", 200, 30)
        final_score = gamebox.from_text(400, 300, "YOUR FINAL SCORE IS: " + str(score), 60, "red")
        thanks = gamebox.from_text(400, 400, "THANK YOU FOR PLAYING ", 60, "red")

        # win gameboxes
        you_won = gamebox.from_text(400, 100, "YOU SURVIVED! LETS GO!! ", 60, "green")

        # drawing health
        camera.draw(full_health)
        camera.draw(health)
        # drawing score
        camera.draw(user_score_box)
        camera.draw(user_score)
        # drawing timer
        camera.draw(clock_box)
        camera.draw(clock)
    else:

        camera.draw(asteroids_title)
        camera.draw(start_instructions)

    if true_countdown == 0:
        won = True
        if won:
            camera.clear("black")
            camera.draw(win_screen)
            camera.draw(you_won)
            camera.draw(gamebox.from_text(400, 300, "YOUR FINAL SCORE IS: " + str(score), 60, "green"))
            camera.draw(gamebox.from_text(400, 400, "THANK YOU FOR PLAYING ", 60, "green"))
            gamebox.pause()

    if game_over:
        camera.clear('black')
        camera.draw(game_over_background)
        camera.draw(final_score)
        camera.draw(thanks)
        gamebox.pause()
    camera.display()


ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)