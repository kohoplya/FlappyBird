import pygame as pg
import sys,time

from menu import Menu
from bird import Bird
from pipe import Pipe
from record import Record
from colores import *

pg.init()

class Game:
    def __init__(self):
        self.width = 800
        self.heigh = 600
        self.scaleFactor = 1.5
        self.clock=pg.time.Clock()
        self.bird = Bird(self.scaleFactor)
        self.isEnter = False

        self.pipes = []
        self.pipeGenerateCounter = 71
        self.moveSpeed = 250
        
        self.font = pg.font.Font("./assets/font.ttf", 30)

        self.isStartMonitoring = False
        self.score = 0
        self.scoreText = self.font.render("Score: 0", True, WHITE)
        self.scoreTextRect = self.scoreText.get_rect(center = (120, 30))

        self.coinImg = pg.transform.scale_by(pg.image.load("./assets/coin.png").convert_alpha(), 1.1)
        self.coinRect = self.coinImg.get_rect(center = (50, 75))
        self.coinCounter = 0
        self.coinCounterText = self.font.render("0", True, WHITE)
        self.coinCounterRect = self.coinCounterText.get_rect(center = (100, 75))

        self.bges = []

        self.isGameOver = False
        self.isGameStarted = True

        self.record = Record()
        self.isMouseEnabled = False

        self.createWin()
        self.gameloop()

    def createWin(self):
        self.win = pg.display.set_mode((self.width, self.heigh))
        self.bgImg = pg.transform.scale(pg.image.load("./assets/bg.png").convert(), (400, 800))

    def gameloop(self):
        self.bges.append(pg.Rect(0, -150, 400, 711))
        last_time=time.time()
        while True:
            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN and self.isGameStarted:
                        self.isEnter = True
                        self.bird.isUpdateOn = True
                    if (event.key == pg.K_SPACE or event.type == pg.MOUSEBUTTONUP) and self.isEnter:
                        self.bird.flap(dt)
                else:
                    if event.type == pg.MOUSEBUTTONUP and self.isEnter:
                        self.bird.flap(dt)

                if event.type == pg.MOUSEBUTTONUP and self.isGameOver == True:
                    if self.restartImgRect.collidepoint(pg.mouse.get_pos()):
                        self.record.updateMaxScore(self.score)
                        self.record.updateCoins(self.coinCounter)
                        self.bird.updateImg()
                        self.restartGame()
                if event.type == pg.MOUSEBUTTONUP and self.isGameOver == True:
                    if self.goMenuImgRect.collidepoint(pg.mouse.get_pos()):
                        self.record.updateMaxScore(self.score)
                        self.record.updateCoins(self.coinCounter)
                        self.bird.updateImg()
                        self.menu = Menu()
                        self.menu.menuloop()
            
            self.updateEverything(dt)
            self.moveBg()
            self.drawEverything()
            self.checkScore()
            pg.display.update()
            self.clock.tick(59)
            self.checkCollisions()

    def createElement(self, nameImg, filePath, width, height, centerX, centerY, isBlit):
        setattr(self, nameImg, pg.transform.scale(pg.image.load(filePath).convert_alpha(), (width, height)))
        setattr(self, nameImg + 'Rect', getattr(self, nameImg).get_rect(center=(centerX, centerY)))
        if isBlit:
            self.win.blit(getattr(self, nameImg), getattr(self, nameImg + 'Rect'))

    def createText(self, nameText, text, color, centerX, centerY, size, isBlit):
        font = pg.font.Font("./assets/font.ttf", size)
        setattr(self, nameText, font.render(text, True, color))
        setattr(self, nameText + 'Rect', getattr(self, nameText).get_rect(center=(centerX, centerY)))
        if isBlit:
            self.win.blit(getattr(self, nameText), getattr(self, nameText + 'Rect'))

    def checkScore(self):
        if len(self.pipes) > 0:
            if (self.bird.rect.left > self.pipes[0].rectDown.left and 
            self.bird.rect.right < self.pipes[0].rectDown.right and not self.isStartMonitoring):
                self.isStartMonitoring = True
            if self.bird.rect.left > self.pipes[0].rectDown.right and self.isStartMonitoring:
                self.isStartMonitoring = False
                self.score += 1
                self.scoreText = self.font.render(f"Score: {self.score}", True, WHITE)

    def checkCollisions(self):
        if len(self.pipes):
            if self.bird.rect.bottom > self.heigh:
                self.bird.isUpdateOn = False
                self.isEnter = False
                self.isGameStarted = False
                self.isGameOver = True
            if(self.bird.rect.colliderect(self.pipes[0].rectDown) or
            self.bird.rect.colliderect(self.pipes[0].rectUp)):
                self.isEnter = False
                self.isGameOver = True
            if self.pipes[0].hasCoin and self.bird.rect.colliderect(self.pipes[0].coinRect):
                self.coinCounter += 1
                self.coinCounterText = self.font.render(f"{self.coinCounter}", True, WHITE)
                self.pipes[0].hasCoin = False

    def moveBg(self):
        for i in range (len(self.bges)-1, -1, -1):
            bg = self.bges[i]
            if self.isEnter:
                bg.x -= 1

            if bg.right < 0:
                self.bges.remove(bg)

            if self.bges[len(self.bges) - 1].right <= self.width:
                self.bges.append(pg.Rect(self.bges[len(self.bges) - 1].right, -150, 400, 711))


        for bg in self.bges:
            self.win.blit(self.bgImg, bg)

    def updateEverything(self, dt):
        if self.isEnter:
            if self.pipeGenerateCounter > 70:
                self.pipes.append(Pipe(self.scaleFactor, self.moveSpeed))
                self.pipeGenerateCounter = 0
            self.pipeGenerateCounter += 1

            for pipe in self.pipes:
                pipe.update(dt)

            if len(self.pipes)!= 0:
                if self.pipes[0].rectUp.right < 0:
                    self.pipes.pop(0)

        self.bird.update(dt)

    def restartMenu(self):
        self.createElement("gameOverImg", "./assets/GameOver.png", 564, 114, 400, 300, 1)
        self.createElement("restartImg", "./assets/startButton.png", 160, 56, 200, 400, 1)
        self.createElement("goMenuImg", "./assets/menuButton.png", 160, 56, 600, 400, 1)

        self.scoreText = self.font.render(f"Score: {self.score}", True, BLACK)
        self.coinCounterText = self.font.render(f"{self.coinCounter}", True, BLACK)

        self.win.blit(self.scoreText, self.scoreTextRect)

    def restartGame(self):
        self.bird.updateImg()
        self.score = 0
        self.scoreText = self.font.render("Score: 0", True, WHITE)
        self.coinCounter = 0
        self.coinCounterText = self.font.render("0", True, WHITE)
        self.isEnter = False
        self.isGameStarted = True
        self.bird.resetPosition()
        self.bird.isUpdateOn = False
        self.pipes.clear()
        self.pipeGenerateCounter = 71
        self.isGameOver = False
        self.bird.yVelocity = 0

    
    def drawEverything(self):
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.bird.img, self.bird.rect)
        self.win.blit(self.scoreText, self.scoreTextRect)
        self.win.blit(self.coinImg, self.coinRect)
        self.win.blit(self.coinCounterText, self.coinCounterRect)
        if self.isGameOver == True:
            self.restartMenu()
        if self.isEnter == False and not self.isGameOver:
            self.createText("tutorial", "Press enter to start and space or lmb to flip", WHITE, 400, 300, 20, 1)

menu = Menu()
menu.menuloop()