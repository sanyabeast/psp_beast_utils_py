# -*- coding: iso-8859-1 -*-


from beastlib.framework import Engine, Actor
from time import time
import stackless
import simplejson as json


engine = Engine({
    "debug": True
})

engine.log(json.dumps([1, 3, 4]))

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
        self.sprint = 0
        self.sprint_speed = 4
        self.lastPad = time()
        self.sprite = spritesheet[self.direction][int(self.boolSprite)]
        self.screenshot = 1

    def on_tick(self):
        Actor.on_tick(self)
        self.sprite = spritesheet[self.direction][int(self.boolSprite)]
    def draw(self, screen):
        screen.blit(self.sprite, 0, 0, self.sprite.width ,
            self.sprite.height, self.position.x, self.position.y, True)
    def on_pad_triangle(self, pad):
        engine.screen.saveToFile("ms0:/PSP/PHOTO/screenshot%s.png" % self.screenshot)
        self.screenshot += 1
    def on_pad_cross(self, pad):
        self.log("cross")
        engine.die()
    def on_pad_left(self, pad):
        self.direction = 2
        self.log("left")
        if self.position.x - (self.speed+self.sprint*self.sprint_speed) >= 0:
            self.position.x -= (self.speed+self.sprint*self.sprint_speed)
            self.boolSprite = not self.boolSprite
    def on_pad_right(self, pad):
        self.direction = 3
        self.log("right")
        if self.position.x + self.sprite.width + (self.speed+self.sprint*self.sprint_speed) < 480:
            self.position.x += (self.speed+self.sprint*self.sprint_speed)
            self.boolSprite = not self.boolSprite
    def on_pad_up(self, pad):
        self.direction = 0
        self.log("up")
        if self.position.y - (self.speed+self.sprint*self.sprint_speed) >= 0:
            self.position.y -= (self.speed+self.sprint*self.sprint_speed)
            self.boolSprite = not self.boolSprite
    def on_pad_down(self, pad):
        self.direction = 1
        self.log("down")
        if self.position.y + self.sprite.height + (self.speed+self.sprint*self.sprint_speed) < 272:
            self.position.y += (self.speed+self.sprint*self.sprint_speed)
            self.boolSprite = not self.boolSprite
            

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
        self.sprite = spritesheet[self.direction][int(self.boolSprite)]
        if self.direction == 0 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.y - self.speed >= 20:
                self.position.y -= self.speed
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 2
        if self.direction == 2 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.x - self.speed > 0:
                self.position.x -= self.speed
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 1
        if self.direction == 1 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.y + self.sprite.height + self.speed < 252:
                self.position.y += self.speed
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 3
        if self.direction == 3 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.x + self.sprite.width + self.speed < 450:
                self.position.x += self.speed
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 0

    def draw(self, screen):
        screen.blit(self.sprite, 0, 0, self.sprite.width,
            self.sprite.height, self.position.x, self.position.y, True)


play = Player({ 
    "rend": engine.rend,
    "is_pawn": True
})

NPC1 = NPC({ "rend": engine.rend })


stackless.run()