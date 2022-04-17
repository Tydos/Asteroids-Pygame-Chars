import pygame
import math
import time as t
import random


pygame.init()

sw = 1920
sh = 1080


# bg = pygame.image.load('asteroidsPics/starbg.png')
bg = pygame.image.load('spacee.jpg')
playerRocket = pygame.image.load('alienship.png')
# playerRocket = pygame.image.load('asteroidsPics/spaceRocket.png')
star = pygame.image.load('asteroidsPics/star.png')
# # asteroid50 = pygame.image.load('asteroidsPics/asteroid50.png')
# asteroid100 = pygame.image.load('asteroidsPics/asteroid100.png')
# asteroid150 = pygame.image.load('asteroidsPics/asteroid150.png')
# asteroid50 = pygame.image.load('D:/AsteroidsTut-master/a.png')
word_c = pygame.image.load('c.png')
word_a = pygame.image.load('a.png')
word_b = pygame.image.load('b.png')

pygame.display.set_caption('Asteroids')
win = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()

gameover = False
lives = 3
score = 0

highScore = 0
result = ''
word = ''
start_time = t.time()
# EasyWords = ['TCC', 'CTC', 'CCT', 'TCT']
# MediumWords = ['TCCT', 'TCTC', 'CTTC', 'CCCT']
# HardWords = ['CTTCCCT', 'CTCCTC', 'CTCTCTC', 'TTCCTTTTTCT']
EasyWords = ['ACBC', 'CBAC', 'CCBA', 'ACAB']
MediumWords = ['ACBCBA', 'ACBAC', 'CABABC', 'CCBBCA']
HardWords = ['CAACBCBBCA', 'BCACBCAC', 'CACBBBBACAC', 'ABBBACCAAAAACA']

# Words = {
#     'Hard': 'CTCTCT',
#     'Medium': 'CTCCT',
#     'Easy': 'CT'
# }

starsactive = False
difficultylvl = 2
# if difficultylvl == 3:

#     # word = Words['Hard'];
#     starsactive = True
# elif difficultylvl == 2:
#     # word = Words['Medium'];
#     starsactive = True
# else:
#     # word = Words['Easy'];
ran = random.randrange(0, 3)
if difficultylvl == 3:
    word = HardWords[ran]
    starsactive = True

elif difficultylvl == 2:
    word = MediumWords[ran]
    starsactive = True

else:
    word = EasyWords[ran]


class Player(object):
    def __init__(self):
        self.img = playerRocket
        # self.w = self.img.get_width()
        # self.h = self.img.get_height()
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
        #win.blit(self.img, [self.x, self.y, self.w, self.h])
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

        # self.w = 50 * rank
        # self.h = 50 * rank
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
        # self.w = self.img.get_width()
        # self.h = self.img.get_height()
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


def updateresult():
    global result
    global score
    global choice
    global word
    font = pygame.font.SysFont('arial', 30)
    currentresult = font.render('RESULT: ' + result, 1, (255, 255, 255))

    win.blit(currentresult, (920, 150))

    if result.lower() == word.lower():
        result = ''
        score += 100
        ran = random.randrange(0, 3)
        if difficultylvl == 3:
            word = HardWords[ran]

        elif difficultylvl == 2:
            word = MediumWords[ran]

        else:
            word = EasyWords[ran]


def checktime():
    curr_time = t.time()
    font = pygame.font.SysFont('arial', 30)
    currenttime = font.render(
        'TIME: ' + str(int(curr_time-start_time)) + ' Sec', 1, (255, 255, 255))
    win.blit(currenttime, (1400, 200))
    if curr_time - start_time >= 60:
        pass


def redrawGameWindow():
    win.blit(bg, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    currentword = font.render('WORD: ' + word, 1, (255, 255, 255))
    win.blit(currentword, (210, 150))

    # currentresult = font.render('Result: ' + result,1,(255,255,255))
    # win.blit(currentresult,(100,100))

    updateresult()
    checktime()

    livesText = font.render('LIVES: ' + str(lives), 1, (255, 255, 255))
    difficultylvlText = font.render(
        'LEVEL: ' + str(difficultylvl), 1, (255, 255, 255))
    playAgainText = font.render('Press Tab to Play Again', 1, (255, 255, 255))
    scoreText = font.render('SCORE: ' + str(score), 1, (255, 255, 255))
    highScoreText = font.render(
        'HIGH SCORE: ' + str(highScore), 1, (255, 255, 255))

    player.draw(win)
    for a in asteroids:
        a.draw(win)

    for s in stars:
        s.draw(win)

    if gameover:
        win.blit(playAgainText, (sw//2-playAgainText.get_width() //
                 2, sh//2 - playAgainText.get_height()//2))

    # win.blit(scoreText, (sw- scoreText.get_width() - 25, 25))
    win.blit(scoreText, (1200, 150))
    win.blit(livesText, (210, 200))
    win.blit(difficultylvlText, (600, 150))
    # win.blit(highScoreText, (sw - highScoreText.get_width() -25, 35 + scoreText.get_height()))
    win.blit(highScoreText, (1400, 150))
    pygame.display.update()


player = Player()
playerBullets = []
asteroids = []
count = 0
stars = []
run = True


while run:
    clock.tick(60)
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

                    # win.blit(result,(100,100))
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

    # for event in pygame.event.get():

    #     if event.key == pygame.K_LEFT or event.key == ord('a'):
    #         player.turnLeft()
    #     if event.key == pygame.K_RIGHT or event.key == ord('d'):
    #         player.turnRight()
    #     if event.key == pygame.K_UP or event.key == ord('w'):
    #         player.moveForward()
    #     if event.key == pygame.K_SPACE:
    #         exit(0)

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
                    asteroids.clear()
                    stars.clear()
                    if score > highScore:
                        highScore = score
                    score = 0

    redrawGameWindow()
pygame.quit()
