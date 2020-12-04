# -*- coding: iso-8859-1 -*-


from beastlib.framework import Engine, Actor, Renderable, Tickable, SCREEN_W, SCREEN_H
from time import time
import stackless
import simplejson as json
import random
import threading

class Player(Actor):
    def __init__(self, props):
        Actor.__init__(self, props)
        self.boolSprite = False
        self.direction = 1
        self.speed = 3
        self.sprint = 0
        self.sprint_speed = 4
        self.lastPad = time()
        self.spritesheet = self.get(props, "spritesheet")
        self.sprite = self.spritesheet[self.direction][int(self.boolSprite)]
        self.screenshot = 1

    def on_tick(self, delta=1):
        Actor.on_tick(self, delta)
        self.sprite = self.spritesheet[self.direction][int(self.boolSprite)]
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
        if self.position.x - (self.speed*self.tick_delta) >= 0:
            self.position.x -= (self.speed*self.tick_delta)
            self.boolSprite = not self.boolSprite
    def on_pad_right(self, pad):
        self.direction = 3
        self.log("right")
        if self.position.x + self.sprite.width + (self.speed*self.tick_delta) < 480:
            self.position.x += (self.speed*self.tick_delta)
            self.boolSprite = not self.boolSprite
    def on_pad_up(self, pad):
        self.direction = 0
        self.log("up")
        if self.position.y - (self.speed*self.tick_delta) >= 0:
            self.position.y -= (self.speed*self.tick_delta)
            self.boolSprite = not self.boolSprite
    def on_pad_down(self, pad):
        self.direction = 1
        self.log("down")
        if self.position.y + self.sprite.height + (self.speed*self.tick_delta) < 272:
            self.position.y += (self.speed*self.tick_delta)
            self.boolSprite = not self.boolSprite
            
class NPC(Actor):
    def __init__(self, props):
        Actor.__init__(self, props)
        self.boolSprite = False
        self.direction = 0
        self.speed = 2
        self.lastPad = time()
        self.spritesheet = self.get(props, "spritesheet")
        self.sprite = self.spritesheet[self.direction][int(self.boolSprite)]
        self.count = 20

    def on_tick(self, delta=1):
        Actor.on_tick(self, delta)
        self.sprite = self.spritesheet[self.direction][int(self.boolSprite)]
        if self.random_bool(0.05) or self.direction == 0 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.y - (self.speed*self.tick_delta) >= 20:
                self.position.y -= (self.speed*self.tick_delta)
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 2
        if self.random_bool(0.05) or self.direction == 2 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.x - (self.speed*self.tick_delta) > 0:
                self.position.x -= (self.speed*self.tick_delta)
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 1
        if self.random_bool(0.05) or self.direction == 1 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.y + self.sprite.height + (self.speed*self.tick_delta) < 252:
                self.position.y += (self.speed*self.tick_delta)
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 3
        if self.random_bool(0.05) or self.direction == 3 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.x + self.sprite.width + (self.speed*self.tick_delta) < 450:
                self.position.x += (self.speed*self.tick_delta)
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 0

    def draw(self, screen):
        screen.blit(self.sprite, 0, 0, self.sprite.width,
            self.sprite.height, self.position.x, self.position.y, True)

class Fire(Renderable):
    def __init__(self, props):
        Renderable.__init__(self, props)
        self.sprite_index = self.get(props, "sprite_index", 0)
        self.direction = 0
        self.speed = 2
        self.lastPad = time()
        self.spritesheet = self.get(props, "spritesheet")
        self.sprite = self.spritesheet[0][int(self.sprite_index)]
        self.count = 20

    def on_tick(self, delta=1):
        Renderable.on_tick(self, delta)
        self.sprite = self.spritesheet[0][self.sprite_index]
        self.sprite_index = (self.sprite_index+1)%4

    def draw(self, screen):
        screen.blit(self.sprite, 0, 0, self.sprite.width,
            self.sprite.height, self.position.x, self.position.y, True)

class Game(Tickable):
    def on_begin(self):
        engine.log(json.dumps([1, 3, 4]))
        spritesheet_purple = engine.create_spritesheet([
            ['assets/purple_wizard/amg1_bk1.png', 'assets/purple_wizard/amg1_bk2.png'],
            ['assets/purple_wizard/amg1_fr1.png', 'assets/purple_wizard/amg1_fr2.png'],
            ['assets/purple_wizard/amg1_lf1.png', 'assets/purple_wizard/amg1_lf2.png'],
            ['assets/purple_wizard/amg1_rt1.png', 'assets/purple_wizard/amg1_rt2.png'],
        ])
        spritesheet_lime = engine.create_spritesheet([
            ['assets/lime_wizard/amg1_bk1.png', 'assets/lime_wizard/amg1_bk2.png'],
            ['assets/lime_wizard/amg1_fr1.png', 'assets/lime_wizard/amg1_fr2.png'],
            ['assets/lime_wizard/amg1_lf1.png', 'assets/lime_wizard/amg1_lf2.png'],
            ['assets/lime_wizard/amg1_rt1.png', 'assets/lime_wizard/amg1_rt2.png'],
        ])
        spritesheet_blue = engine.create_spritesheet([
            ['assets/blue_wizard/amg1_bk1.png', 'assets/blue_wizard/amg1_bk2.png'],
            ['assets/blue_wizard/amg1_fr1.png', 'assets/blue_wizard/amg1_fr2.png'],
            ['assets/blue_wizard/amg1_lf1.png', 'assets/blue_wizard/amg1_lf2.png'],
            ['assets/blue_wizard/amg1_rt1.png', 'assets/blue_wizard/amg1_rt2.png'],
        ])
        spritesheet_red = engine.create_spritesheet([
            ['assets/red_wizard/amg1_bk1.png', 'assets/red_wizard/amg1_bk2.png'],
            ['assets/red_wizard/amg1_fr1.png', 'assets/red_wizard/amg1_fr2.png'],
            ['assets/red_wizard/amg1_lf1.png', 'assets/red_wizard/amg1_lf2.png'],
            ['assets/red_wizard/amg1_rt1.png', 'assets/red_wizard/amg1_rt2.png'],
        ])
        spritesheet_cyan = engine.create_spritesheet([
            ['assets/cyan_wizard/amg1_bk1.png', 'assets/cyan_wizard/amg1_bk2.png'],
            ['assets/cyan_wizard/amg1_fr1.png', 'assets/cyan_wizard/amg1_fr2.png'],
            ['assets/cyan_wizard/amg1_lf1.png', 'assets/cyan_wizard/amg1_lf2.png'],
            ['assets/cyan_wizard/amg1_rt1.png', 'assets/cyan_wizard/amg1_rt2.png'],
        ])
        spritesheet_fire = engine.create_spritesheet([
            [
                'assets/fire_a/fire_0.png', 
                'assets/fire_a/fire_1.png',
                'assets/fire_a/fire_2.png', 
                'assets/fire_a/fire_3.png'
            ]
        ])

        char_spritesheets = [
            spritesheet_cyan,
            spritesheet_lime,
            spritesheet_blue,
            spritesheet_red
        ]

        fires = 0
        while fires<10:
            fire = Fire({
                "tick_interval": 0.1,
                "position_x": engine.random_int(0, SCREEN_W),
                "position_y": engine.random_int(0, SCREEN_H),  
                "sprite_index": engine.random_int(0, 3),
                "spritesheet": spritesheet_fire
            })
            fires+=1

        player = Player({ 
            "is_pawn": True,
            "tick_interval": 0.0333,
            "spritesheet": spritesheet_purple,
            "position_x": engine.random_int(0, SCREEN_W),
            "position_y": engine.random_int(0, SCREEN_H),
        })

        chars = 0
        while chars<8:
            NPC({ 
                "tick_interval": 0.0333,
                "spritesheet": engine.random_choice(char_spritesheets),
                "position_x": engine.random_int(0, SCREEN_W),
                "position_y": engine.random_int(0, SCREEN_H),
            })
            chars+=1

        engine.set_loading(False)

game = Game({
    "tick_interval": 1
})

engine = Engine({
    "debug": True,
    "is_loading": True
})

stackless.run()