# -*- coding: iso-8859-1 -*-

from beastlib.core import Engine, Actor
from time import time
import stackless

engine = Engine({
    "debug": True
})

print "test"

# Loads the character movement images
spritesheet = []
spritesheet = engine.create_spritesheet([
    ['assets/amg1_bk1.png', 'assets/amg1_bk2.png'],
    ['assets/amg1_fr1.png', 'assets/amg1_fr2.png'],
    ['assets/amg1_lf1.png', 'assets/amg1_lf2.png'],
    ['assets/amg1_rt1.png', 'assets/amg1_rt2.png'],
])

class Player(Actor):
    def __init__(self, props):
        Actor.__init__(self, props)
        self.boolSprite = False
        self.direction = 1
        self.speed = 3
        self.lastPad = time()
        self.sprite = spritesheet[self.direction][int(self.boolSprite)]
        self.screenshot = 1

    def on_tick(self):
        self.sprite = spritesheet[self.direction][int(self.boolSprite)]
        pad = engine.Controller()
        if pad.cross:
            
            engine.die()
        elif pad.triangle:
            engine.screen.saveToFile("ms0:/PSP/PHOTO/screenshot%s.png" % self.screenshot)
            self.screenshot += 1
        elif pad.down and (not self.lastPad or time() - self.lastPad >= 0.05):
            #Draw the player facing south:
            self.lastPad = time()
            self.direction = 1
            if self.posY + self.sprite.height + self.speed < 272:
                self.posY += self.speed
                self.boolSprite = not self.boolSprite
        elif pad.up and (not self.lastPad or time() - self.lastPad >= 0.05):
            engine.log("up")
            #Draw the player facing north:
            self.lastPad = time()
            self.direction = 0
            if self.posY - self.speed >= 0:
                self.posY -= self.speed
                self.boolSprite = not self.boolSprite
        elif pad.left and (not self.lastPad or time() - self.lastPad >= 0.05):
            #Draw the player facing west:
            self.lastPad = time()
            self.direction = 2
            if self.posX - self.speed >= 0:
                self.posX -= self.speed
                self.boolSprite = not self.boolSprite
        elif pad.right and (not self.lastPad or time() - self.lastPad >= 0.05):
            #Draw the player facing east:
            self.lastPad = time()
            self.direction = 3
            if self.posX + self.sprite.width + self.speed < 480:
                self.posX += self.speed
                self.boolSprite = not self.boolSprite
    def draw(self, screen):
        screen.blit(self.sprite, 0, 0, self.sprite.width ,
            self.sprite.height, self.posX, self.posY, True)

class NPC(Actor):
    def __init__(self, props):
        Actor.__init__(self, props)
        self.boolSprite = False
        self.direction = 0
        self.speed = 5
        self.lastPad = time()
        self.sprite = spritesheet[self.direction][int(self.boolSprite)]
        self.count = 20

    def on_tick(self):
        # This NPC runs around the screen changing its direction
        # when touches the border.
        self.sprite = spritesheet[self.direction][int(self.boolSprite)]
        if self.direction == 0 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.posY - self.speed >= 20:
                self.posY -= self.speed
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 2
        if self.direction == 2 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.posX - self.speed > 0:
                self.posX -= self.speed
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 1
        if self.direction == 1 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.posY + self.sprite.height + self.speed < 252:
                self.posY += self.speed
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 3
        if self.direction == 3 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.posX + self.sprite.width + self.speed < 450:
                self.posX += self.speed
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 0

    def draw(self, screen):
        screen.blit(self.sprite, 0, 0, self.sprite.width,
            self.sprite.height, self.posX, self.posY, True)


# print "Real memory: ",pspos.realmem()

#Loads background music
# pspmp3.init(1)
#pspmp3.load("MP3Sample.mp3")        # Uncomment this to add a MP3 in backgound
# pspmp3.play()

#Loads background music in ogg
#pspogg.init(2)
#pspogg.load('Oggsample.ogg')
#pspogg.play()

# Creates the renderer object

# Creates a player Agent
play = Player({ "rend": engine.rend })
# Creates one NPC that runs around the screen
NPC1 = NPC({ "rend": engine.rend })

# Starts the game loop
stackless.run()
#pspogg.end()
# pspmp3.end()
