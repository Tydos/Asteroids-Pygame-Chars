""" AI Asteroids """
import pygame
import math
import time as t
import random


game_timer = 60
game_fps = 60
sw = 1920
sh = 1080
exitflag = 0
count = 0
difficulty = []
timetaken = []
lives = 3
score = 0
hits = 0
highScore = 0
difficultylvl = 1
starsactive = False
run = True
gameover = False
asteroids = []
stars = []
result = ''
word = ''
start_time = t.time()


EasyWords = ['ACBC', 'CBAC', 'CCBA', 'ACAB']
MediumWords = ['ACBA', 'ACBAC', 'CABBC', 'CBCA']
HardWords = ['CAACBCBBCA', 'BCACBCAC', 'CACBBACAC', 'ABBBACAAAAACA']


pygame.init()
bg = pygame.image.load('spacee.jpg')
playerRocket = pygame.image.load('alienship.png')
star = pygame.image.load('star.png')
word_c = pygame.image.load('c.png')
word_a = pygame.image.load('a.png')
word_b = pygame.image.load('b.png')
pygame.display.set_caption('Asteroids')
win = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 30)


def dynamicdifficulty():
    getcurrentstate()
    checkprogress()   
   
def getcurrentstate():
    global difficulty,timetaken
    curr_time = t.time()
    difficulty.append(difficultylvl)
    timetaken.append(int(curr_time-start_time))

def checkprogress():
    global difficultylvl
    len = 0
    for x in difficulty:
        print(x)
        len += 1
    for y in timetaken:
        print(y) 

    lastdifficulty = difficulty[len-1]
    lasttimetaken = timetaken[len-1]       

    if lasttimetaken > timetaken[-1]:
        if difficultylvl != 1:
            difficultylvl -= 1
    else:
        if difficultylvl != 3:
            difficultylvl += 1


class Player(object):
    def __init__(self):
        self.img = playerRocket
        self.w = 50
        self.h = 50
        self.x = sw//2
        self.y = sh//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2,
                     self.y - self.sine * self.h//2)

    def draw(self, win):
        win.blit(self.rotatedSurf, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2,
                     self.y - self.sine * self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2,
                     self.y - self.sine * self.h//2)

    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2,
                     self.y - self.sine * self.h // 2)

    def updateLocation(self):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0


class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank

        if self.rank == 1:
            self.image = word_a
        elif self.rank == 2:
            self.image = word_b
        else:
            self.image = word_c

        self.w = 50
        self.h = 50
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice(
            [-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1, 3)
        self.yv = self.ydir * random.randrange(1, 3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Star(object):
    def __init__(self):
        self.img = star
        self.w = 50
        self.h = 50
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

def initialize():
    global word,starsactive
    ran = random.randrange(0, 3)
    if difficultylvl == 3:
        word = HardWords[ran]
        starsactive = True
    elif difficultylvl == 2:
        word = MediumWords[ran]
        starsactive = True
    else:
        word = EasyWords[ran]
        starsactive = False

def updateresult():
    global result, score, word, hits , curr_time

    currentresult = font.render('RESULT: ' + result, 1, (255, 255, 255))
    win.blit(currentresult, (920, 150))

    if result.lower() == word.lower():
        result = ''
        score += 100
        hits += 1
        dynamicdifficulty()
        initialize()
        

def checktime():
    global exitflag
    curr_time = t.time()
    currenttime = font.render('TIME: ' + str(int(curr_time-start_time)) + ' Sec', 1, (255, 255, 255))
    win.blit(currenttime, (1400, 200))
    if curr_time - start_time >= game_timer:
        exitflag = 1
        resetgame()


def resetgame():
    global lives, result, asteroids, stars, score, highScore
    font = pygame.font.SysFont('arial', 70)
    message = font.render( 'GAME OVER',1,(120,50,250) )
    win.blit(message, (1000, 600))
   
    asteroids.clear()
    stars.clear()
    if score > highScore:
        highScore = score
    score = 0


def redrawGameWindow():
    if exitflag == 1:
        return
    
    win.blit(bg, (0, 0))
   
    currentword = font.render('WORD: ' + word, 1, (255, 255, 255))
    win.blit(currentword, (210, 150))

    updateresult()
    checktime()

    livesText = font.render('LIVES: ' + str(lives), 1, (255, 255, 255))
    difficultylvlText = font.render( 'LEVEL: ' + str(difficultylvl), 1, (255, 255, 255))
    playAgainText = font.render('Press Tab to Play Again', 1, (255, 255, 255))
    scoreText = font.render('SCORE: ' + str(score), 1, (255, 255, 255))
    highScoreText = font.render('HIGH SCORE: ' + str(highScore), 1, (255, 255, 255))
    win.blit(scoreText, (1200, 150))
    win.blit(livesText, (210, 200))
    win.blit(difficultylvlText, (600, 150))
    win.blit(highScoreText, (1400, 150))

    player.draw(win)
    for a in asteroids:
        a.draw(win)

    for s in stars:
        s.draw(win)

    if gameover:
        win.blit(playAgainText, (sw//2-playAgainText.get_width() //
                 2, sh//2 - playAgainText.get_height()//2))

   
    pygame.display.update()



player = Player()
initialize()

while run:
    clock.tick(game_fps)
    count += 1
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1,2,3])
            asteroids.append(Asteroid(ran))
        if count % 100 == 0:
            if starsactive:
                stars.append(Star())

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            # if spaceship hits a asterioid ig
            if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y + a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    # lives -= 1
                    score += 50
                    asteroids.pop(asteroids.index(a))

                    # if letter a was hit
                    if a.rank == 1:
                        score += 10
                        result = result + 'A'

                    if a.rank == 2:
                        score += 10
                        result = result + 'B'

                    if a.rank == 3:
                        score += 10
                        result = result + 'C'

                   
                    updateresult()

        for s in stars:
            s.x += s.xv
            s.y += s.yv

            # remove stars when they go offscreen
            if s.x < -100 - s.w or s.x > sw + 100 or s.y > sh + 100 or s.y < -100 - s.h:
                stars.pop(stars.index(s))
                break

            # if spaceship hits a star
            if (s.x >= player.x - player.w//2 and s.x <= player.x + player.w//2) or (s.x + s.w <= player.x + player.w//2 and s.x + s.w >= player.x - player.w//2):
                if(s.y >= player.y - player.h//2 and s.y <= player.y + player.h//2) or (s.y + s.h >= player.y - player.h//2 and s.y + s.h <= player.y + player.h//2):
                    lives -= 1
                    score -= 50
                    stars.pop(stars.index(s))
                    break

        if lives <= 0:
            gameover = True


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.moveForward()
        if keys[pygame.K_SPACE]:
            exit(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if gameover:
                    gameover = False
                    lives = 3
                    result = ''
                    asteroids.clear()
                    stars.clear()
                    if score > highScore:
                        highScore = score
                    score = 0
                else:
                    lives = 3
                    result = ''
                    score = 0

    redrawGameWindow()

pygame.quit()