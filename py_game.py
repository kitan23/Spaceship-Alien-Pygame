import pygame
import random
import math
from pygame import mixer
#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#set background
background = pygame.image.load('space.png')

#Music
mixer.music.load('background.wav')
mixer.music.play(-1)


#change Title and Icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('book.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(30)

# Bullet
#Ready - Can't see the bullet on the screen
#Fire - Bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

#Score
score_value = 0

textX = 10
textY = 10

font = pygame.font.Font('freesansbold.ttf',32)
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (230, 250))

#WINNN
win_font = pygame.font.Font('freesansbold.ttf',64)
def win_text():
    win_text = win_font.render("YOU WIN", True, (255,255,255))
    screen.blit(win_text, (250,250))


#Show spaceship
def player(x,y):
    screen.blit(playerImg,(x,y))

#Show image
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX- bulletX,2) + math.pow(enemyY- bulletY,2))
    if distance < 27:
        return True
    return False


#Game Loop
running = True
while running:

    screen.fill((0,0,0))

    #backgound image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #interrupt the program when click close
            running = False

        if event.type == pygame.KEYDOWN:#if keystroke is pressed check the direction
            if event.key == pygame.K_LEFT:
                #print('Left arrow is pressed')
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                #print('Right key is pressed')
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #print('A keystroke is released')
                playerX_change=0


    #Spaceship Movement
    playerX += playerX_change

    #Create boundaries for spaceship
    if playerX <=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy Movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] >= 415:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        #Create boundaries for alien
        if enemyX[i] <=0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        enemy(enemyX[i],enemyY[i],i)

        #Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_Sound = mixer.Sound('explosion.wav')
            collision_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(0,150)


        if score_value == 5:
            for j in range(num_of_enemies):
                enemyY[j] = -2000
            win_text()
            break


    #Bullet movement&boundary
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    show_score(textX,textY)
    player(playerX,playerY)

    pygame.display.update()




