import pygame as pg
from random import randint

class Pipe:
    def __init__(self, scaleFactor, moveSpeed):
        self.imgUp = pg.transform.scale_by(pg.image.load("./assets/pipeup.png").convert_alpha(), scaleFactor)
        self.imgDown = pg.transform.scale_by(pg.image.load("./assets/pipedown.png").convert_alpha(), scaleFactor)
        self.rectUp = self.imgUp.get_rect()
        self.rectDown = self.imgDown.get_rect()
        self.pipeDistance = 200
        self.rectUp.y = randint(200, 500)
        self.rectUp.x = 800
        self.rectDown.y = self.rectUp.y - self.pipeDistance - self.rectUp.height
        self.rectDown.x = 800
        self.moveSpeed  = moveSpeed

        self.hasCoin = randint(1, 5) == 1
        self.coinImg = pg.transform.scale_by(pg.image.load("./assets/coin.png").convert_alpha(), 1.3)
        coin_width, coin_height = self.coinImg.get_size()
        self.coinRect = self.coinImg.get_rect()

        self.coinRect.x = self.rectUp.x + self.rectUp.width // 2
        self.coinRect.y = randint(self.rectDown.bottom + coin_height, self.rectUp.top - coin_height)

        self.coinRect.center = (self.coinRect.x, self.coinRect.y)

    def drawPipe(self, win):
        win.blit(self.imgUp, self.rectUp)
        win.blit(self.imgDown, self.rectDown)
        if self.hasCoin:
            win.blit(self.coinImg, self.coinRect)

    def update(self, dt):
        self.rectUp.x -= int(self.moveSpeed*dt)
        self.rectDown.x -= int(self.moveSpeed*dt)
        self.coinRect. x -= int(self.moveSpeed*dt)

