from turtle import update
import pygame
import random
import math
from pygame import mixer

# Initialising pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1530,810))

# Title and Icon
pygame.display.set_caption("Space Intruders")
icon = pygame.image.load("UFO.png")
icon = pygame.transform.scale(icon, (1530, 810)).convert_alpha()
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("Background.png")
background = pygame.transform.scale(background, (1530, 810)).convert_alpha()

# Background Music
pygame.mixer.music.load("Background.mp3")
pygame.mixer.music.play(-1)

# Player
player = pygame.image.load("Spaceship.png")
playerX = 685
playerY = 620
playerX_change = 0

# Enemy
enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8
num_of_enemies1 = 4
num_of_enemies2 = 4

for i in range(num_of_enemies1):
    enemy.append(pygame.image.load("Enemy1.png"))
    enemyX.append(random.randint(0, 1380))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3.5)
    enemyY_change.append(50)

for i in range(num_of_enemies2):
    enemy.append(pygame.image.load("Enemy2.png"))
    enemyX.append(random.randint(0, 1380))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3.5)
    enemyY_change.append(50)

# Bullet
bullet = pygame.image.load("Bullet.png")
bulletX = 0
bulletY = 620
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"                            # At ready state bullet is not visible & at fire state bullet is moving on the screen

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY= 10

# Game over text
gameover_font = pygame.font.Font("Italia.ttf", 95)

# Dealing with Hi_score
with open ("Hi_score.txt", "r") as f:
    hiscore = f.read()

def show_score(x, y):
    score = font.render("SCORE : " + str(score_value) + "  HI-SCORE : " + str(hiscore), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = gameover_font.render(" GAME OVER! ", True, (255, 255, 255))
    screen.blit(over_text, (480, 320))

def Spaceship(x, y):
    screen.blit(player,(x, y))

def Ghost(x, y, i):
    screen.blit(enemy[i],(x, y))   

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet,(x+40, y+15))

def iscollison(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0,0,0))

    # Background Image Loading
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # Check if any key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = +5
            if event.key == pygame.K_r:
                score_value += 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("Laserbeam.wav")
                    bullet_sound.play()
                    # Get the current x coordinate of the sppaceship                   
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # Checking for Boundaries of Spaceship            
    playerX += playerX_change

    if playerX <=0:
        playerX = 0
    elif playerX >= 1380:
        playerX = 1380

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 550:
            with open ("Hi_score.txt", "w") as f:
                f.write(str(hiscore))
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 3.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1430:
            enemyX_change[i] = -3.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collison = iscollison(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            collison_sound = mixer.Sound("Explosion.wav")
            collison_sound.play()
            bulletY = 620
            bullet_state = "ready"
            score_value += 10
            if score_value > int(hiscore):
                hiscore = score_value
            enemyX[i] = random.randint(0, 1380)
            enemyY[i] = random.randint(50, 150)
        Ghost(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <=0 :
        bulletY = 620
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    

    Spaceship(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
