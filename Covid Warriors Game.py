import pygame
import random
from sys import exit
import math
from pygame import mixer

#initialize pygame
pygame.init()

#create the screen
screen=pygame.display.set_mode((800,600))

#background
background= pygame.image.load('bgimg.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Covid Warriors")
icon = pygame.image.load("virus.png")
pygame.display.set_icon(icon)
#player icon
playerimg=pygame.image.load('warrior.png')
playerX=370
playerY=480
playerXchange=0

#enemy icon
enemyimg=[]
enemyX=[]
enemyY=[]
enemyXchange=[]
enemyYchange=[]
num_of_enemies=6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('coronavirus.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyXchange.append(0.2)
    enemyYchange.append(40)

#spray icon
sprayimg=pygame.image.load('drop.png')
sprayX=0
sprayY=480
sprayYchange=0.5
spray_state="ready"

#score
score_value=0
font = pygame.font.Font('lcd.ttf',32)
gameoverfont = pygame.font.Font('Lcd.ttf',64)
textx=10
texty=10
def showscore(x,y):
    score=font.render(("Score : " + str(score_value)),True,(0,0,245))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))
    
def spray(x,y):
    global spray_state
    spray_state="fire"
    screen.blit(sprayimg,(x+60,y+5))

def isCollision(enemyX,enemyY,sprayX,sprayY):
    distance=math.sqrt((math.pow(enemyX-sprayX,2))+(math.pow(enemyY-sprayY,2)))
    if distance < 27:
        return True
    else:
        return False
    
def gameovertext():
    gameover=gameoverfont.render("GAMEOVER!",True,(255,0,0))
    screen.blit(gameover,(255,250))

while True:
    screen.fill((0,128,128))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -0.3
            if event.key == pygame.K_RIGHT:
                playerXchange = 0.3
            if event.key == pygame.K_SPACE:
                if spray_state is "ready":
                    spray_sound=mixer.Sound("laser.wav")
                    spray_sound.play()
                    sprayX=playerX
                    spray(sprayX,sprayY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0
    playerX  += playerXchange
    #spaceship boundary check
    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0
    for i in range(num_of_enemies):
        #gameover
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            gameovertext()
            break
        enemyX[i] += enemyXchange[i]
        #boundary check for enemy
        if enemyX[i] >= 736:
            enemyY[i] += enemyYchange[i]
            enemyXchange[i] = -0.2
        elif enemyX[i] <= 0:
            enemyY[i] += enemyYchange[i]
            enemyXchange[i] = 0.2
         #collision
        collision=isCollision(enemyX[i],enemyY[i],sprayX,sprayY)
        if collision:
            collision_sound=mixer.Sound("explosion.wav")
            collision_sound.play()
            sprayY=480
            spray_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)
    #spray movement
    if sprayY <= 0:
        sprayY=480
        spray_state="ready"
    if spray_state is "fire":
        spray(sprayX,sprayY)
        sprayY -= sprayYchange
        
    player(playerX,playerY)
    showscore(textx,texty)
    pygame.display.update()