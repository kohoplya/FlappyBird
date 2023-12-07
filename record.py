class Record:
    def __init__(self, filename="./data.txt"):
        self.filename = filename
        self.maxScore = 0
        self.coins = 0
        self.birdImgIndex = 0

    def load(self):
        try:
            with open(self.filename, 'r') as file:
                content = file.readlines()
                if content:
                    self.maxScore = int(content[0])
                    self.coins = int(content[1])
                    self.birdImgIndex = int(content[2])
        except FileNotFoundError:
            self.save(0, 0, 0)

    def save(self, currentScore, currentCoins, randNum):
        if currentScore > self.maxScore:
            self.maxScore = currentScore
        self.coins += currentCoins
        self.birdImgIndex = randNum
        with open(self.filename, 'w') as file:
            file.write(f"{self.maxScore}\n{self.coins}\n{self.birdImgIndex}")

    def updateMaxScore(self, currentScore):
        self.load()
        self.save(currentScore, 0, self.birdImgIndex)

    def updateCoins(self, currentCoins):
        self.load()
        self.save(self.maxScore, currentCoins, self.birdImgIndex)

    def setCoins(self, currentCoins):
        self.load()
        with open(self.filename, 'w') as file:
            file.write(f"{self.maxScore}\n{currentCoins}\n{self.birdImgIndex}")

    def updateRandNum(self, num):
        self.load()
        self.save(self.maxScore, 0, num)

    def getMaxScore(self):
        self.load()
        return self.maxScore

    def getCoins(self):
        self.load()
        return self.coins
    
    def getBirdImgIndex(self):
        self.load()
        return self.birdImgIndex

    def resetAll(self):
        self.maxScore = 0
        self.coins = 0
        self.birdImgIndex = 0
        with open(self.filename, 'w') as file:
            file.write('0\n0\n0')

record = Record()
# record.resetAll()
