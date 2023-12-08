import pygame as pg
from random import randint
from record import Record

class Bird(pg.sprite.Sprite):
    def __init__(self, scaleFactor):
        super(Bird, self).__init__()

        self.birdList = [pg.transform.scale_by(pg.image.load("./assets/birds/cummonBirdDown.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/cummonBirdUp.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/greenBirdDown.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/greenBirdUp.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/pinkBirdDown.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/pinkBirdUp.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/ukBirdDown.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/ukBirdUp.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/upaBirdDown.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/upaBirdUp.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/yellowBirdDown.png").convert_alpha(), scaleFactor),
                        pg.transform.scale_by(pg.image.load("./assets/birds/yellowBirdUp.png").convert_alpha(), scaleFactor),
                        ]
        self.record = Record()
        self.randNum = self.record.getBirdImgIndex()
        self.imgIndex = self.randNum
        
        self.img = self.birdList[self.imgIndex]
        self.rect = self.img.get_rect(center = (100, 200))
        self.yVelocity = 0
        self.gravity = 10
        self.flapSpeed= 250
        self.animCounter = 0
        self.isUpdateOn = False

    def updateImg(self):
        self.randNum = self.record.getBirdImgIndex()
        self.imgIndex = self.randNum

    def update(self, dt):
        if self.isUpdateOn == True:
            self.playAnimation()
            self.appleGravity(dt)

            if self.rect.y <= 0 and self.flapSpeed == 250:
                self.rect.y = 0
                self.flapSpeed = 0
                self.yVelocity = 0
            elif self.rect.y > 0 and self.flapSpeed == 0:
                self.flapSpeed = 250

    def appleGravity(self, dt):
        self.yVelocity += self.gravity*dt
        self.rect.y += self.yVelocity

    def flap(self, dt):
        self.yVelocity =- self.flapSpeed*dt 

    def playAnimation(self):
        if self.animCounter == 5:
            self.img = self.birdList[self.imgIndex]
            if self.imgIndex == self.randNum: self.imgIndex = self.randNum + 1
            else: self.imgIndex = self.randNum
            self.animCounter = 0

        self.animCounter += 1

    def resetPosition(self):
        self.rect.center = (100, 200)

