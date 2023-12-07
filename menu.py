import pygame as pg
import sys, time
from random import randint

from colores import *
from bird import Bird
from record import Record

class Menu:
    def __init__(self):
        self.width = 500
        self.heigh = 500
        self.win = pg.display.set_mode((self.width, self.heigh))
        self.clock=pg.time.Clock()
        self.isShop = False
        self.font = pg.font.Font("./assets/font.ttf", 20)
        self.bird = Bird(1.8)
        self.bird.rect.center = (80, 200)
        self.record = Record()

        self.price = 10

    def menuloop(self):
        last_time=time.time()
        while True:
            if not self.isShop:
                self.drawMenu()
            else:
                self.Shop()

            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if not self.isShop: 
                    if self.restartImgRect.collidepoint(pg.mouse.get_pos()):
                        self.bird.rect.center = (80, 200)
                        if event.type == pg.MOUSEBUTTONUP:
                            self.bird.rect.center = (80, 200)
                            from game import Game
                            self.game = Game()

                    if self.shopImgRect.collidepoint(pg.mouse.get_pos()):
                        self.bird.rect.center = (80, 300)
                        if event.type == pg.MOUSEBUTTONUP:
                            self.bird.rect.center = (80, 300)
                            self.isShop = True 

                elif self.backImgRect.collidepoint(pg.mouse.get_pos()) and event.type == pg.MOUSEBUTTONUP:
                    self.isShop = False

            self.bird.playAnimation()
            pg.display.update()
            self.clock.tick(30)

    def drawElement(self, nameImg, filePath, width, height, centerX, centerY):
        setattr(self, nameImg, pg.transform.scale(pg.image.load(filePath).convert_alpha(), (width, height)))
        setattr(self, nameImg + 'Rect', getattr(self, nameImg).get_rect(center=(centerX, centerY)))
        self.win.blit(getattr(self, nameImg), getattr(self, nameImg + 'Rect'))

    def drawText(self, nameText, text, color, centerX, centerY):
        setattr(self, nameText, self.font.render(text, True, color))
        setattr(self, nameText + 'Rect', getattr(self, nameText).get_rect(center=(centerX, centerY)))
        self.win.blit(getattr(self, nameText), getattr(self, nameText + 'Rect'))

    def drawMenu(self):
        self.drawElement("bgImg", "./assets/bg.png", 520, 924, 250, 250)
        self.drawElement("flappyBirdImg", "./assets/FlappyBird.png", 384, 88, 250, 80)
        self.drawElement("restartImg", "./assets/startButton.png", 160*1.2, 56*1.2, 250, 200)
        self.drawElement("shopImg", "./assets/shopButton.png", 160*1.2, 56*1.2, 250, 300)
        self.drawElement("recordImg", "./assets/record.png", 140*1.4, 28*1.4, 120, 450)
        self.drawElement("coinsImg", "./assets/coins.png", 140*1.4, 28*1.4, 380, 450)
        
        self.drawText("maxScoreText", f"{self.record.getMaxScore()}", WHITE, 165, 450)
        self.drawText("coinsText", f"{self.record.getCoins()}", WHITE, 420, 450)
        
        self.win.blit(self.bird.img, self.bird.rect)

    def Shop(self):
        self.drawElement("bgImg", "./assets/bg.png", 520, 924, 250, 250)
        self.drawElement("backImg", "./assets/back.png", 26*1.4, 28*1.4, 30, 35)
        self.drawElement("coinsImg", "./assets/coins.png", 140*1.4, 28*1.4, 372, 35)   
        self.drawElement("buyImg", "./assets/buyButton.png", 160*2, 56*2, 250, 250)
        self.drawElement("cheatImg", "./assets/cheat.png", 80*1.4, 28*1.4, 414, 76)

        self.drawText("coinsText", f"{self.record.getCoins()}", WHITE, 412, 35)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if self.backImgRect.collidepoint(pg.mouse.get_pos()):
                if event.type == pg.MOUSEBUTTONUP:
                    self.bird.updateImg()
                    self.isShop = False
            if self.cheatImgRect.collidepoint(pg.mouse.get_pos()):
                if event.type == pg.MOUSEBUTTONUP:
                    self.record.updateCoins(50)
                    
            if self.buyImgRect.collidepoint(pg.mouse.get_pos()):
                if event.type == pg.MOUSEBUTTONUP:
                    if self.record.getCoins() >= self.price:
                        self.randNum = randint(0, len(self.bird.birdList) // 2 - 1) * 2
                        self.record.updateRandNum(self.randNum)
                        self.bird.updateImg()

                        self.currentCoins = self.record.getCoins() - self.price
                        self.record.setCoins(self.currentCoins)
                        self.drawText("successText", f"Success", WHITE, 250, 320)
                        self.coinsText = self.font.render(f"{self.record.getCoins()}",True, WHITE)
                    else:
                        self.drawText("unSuccessText", f"Not enough coins!!!", WHITE, 250, 320)
