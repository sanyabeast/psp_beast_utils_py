# -*- coding: iso-8859-1 -*-


from beastlib.core import GLOBAL
from beastlib.tools import random_bool, random_choice, random_int
from beastlib.framework import Engine, Pawn, Actor, Tickable, TaskManager, Game
from time import time
import stackless

class Player(Pawn):
    def __init__(self, props):
        Pawn.__init__(self, props)
        self.boolSprite = False
        self.direction = 1
        self.speed = 3
        self.sprint = 0
        self.sprint_speed = 4
        self.lastPad = time()
        self.spritesheet = self.get(props, "spritesheet")
        self.sprite = self.spritesheet[self.direction][int(self.boolSprite)]

    def on_tick(self, delta=1):
        Pawn.on_tick(self, delta)
        self.sprite = self.spritesheet[self.direction][int(self.boolSprite)]
    def draw(self):
        GLOBAL.SCREEN.blit(self.sprite, 0, 0, self.sprite.width ,
            self.sprite.height, int(self.position.x), int(self.position.y), True)
    def on_pad_triangle(self, pad):
        from beastlib.tools import get_random_string
        def dojob(f):
            self.log(get_random_string("test"))
            f()
        engine.task_manager.add_task(dojob)
    def on_pad_cross(self, pad):
        self.log("cross")
        engine.destroy()
    def on_pad_circle(self, pad):
        self.log("circle")
    def on_pad_square(self, pad):
        def dojob(f):
            engine.log("1")
            engine.log("2")
            engine.log("3")
            if self.find_object_by_type("Fire")!=None:
                self.find_object_by_type("Fire").destroy()
            f()
        engine.task_manager.add_task(dojob)
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
            
class NPC(Pawn):
    def __init__(self, props):
        Pawn.__init__(self, props)
        self.created_at = time()
        self.lifetime = random_int(10, 60)
        self.boolSprite = False
        self.direction = 0
        self.speed = 2
        self.lastPad = time()
        self.spritesheet = self.get(props, "spritesheet")
        self.sprite = self.spritesheet[self.direction][int(self.boolSprite)]
        self.count = 20

    def on_tick(self, delta=1):
        # now = time()
        # if (now-self.created_at>self.lifetime): 
        #     self.destroy()
        #     return
        Pawn.on_tick(self, delta)
        self.sprite = self.spritesheet[self.direction][int(self.boolSprite)]
        if random_bool(0.05) or self.direction == 0 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.y - (self.speed*self.tick_delta) >= 20:
                self.position.y -= (self.speed*self.tick_delta)
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 2
        if random_bool(0.05) or self.direction == 2 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.x - (self.speed*self.tick_delta) > 0:
                self.position.x -= (self.speed*self.tick_delta)
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 1
        if random_bool(0.05) or self.direction == 1 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.y + self.sprite.height + (self.speed*self.tick_delta) < 252:
                self.position.y += (self.speed*self.tick_delta)
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 3
        if random_bool(0.05) or self.direction == 3 and \
           (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            if self.position.x + self.sprite.width + (self.speed*self.tick_delta) < 450:
                self.position.x += (self.speed*self.tick_delta)
                self.boolSprite = not self.boolSprite
            else:
                self.direction = 0

    def draw(self):
        GLOBAL.SCREEN.blit(self.sprite, 0, 0, self.sprite.width,
            self.sprite.height, int(self.position.x), int(self.position.y), True)

class Fire(Actor):
    def __init__(self, props):
        Actor.__init__(self, props)
        self.sprite_index = self.get(props, "sprite_index", 0)
        self.direction = 0
        self.speed = 2
        self.lastPad = time()
        self.spritesheet = self.get(props, "spritesheet")
        self.sprite = self.spritesheet[0][int(self.sprite_index)]
        self.count = 20

    def on_tick(self, delta=1):
        Actor.on_tick(self, delta)
        self.sprite = self.spritesheet[0][self.sprite_index]
        self.sprite_index = (self.sprite_index+1)%4

    def draw(self):
        GLOBAL.SCREEN.blit(self.sprite, 0, 0, self.sprite.width,
            self.sprite.height, self.position.x, self.position.y, True)
    def on_destroy(self, reason):
        self.log("the fire is out")

class DungeonGame(Game):
    max_fires = 16
    max_npcs = 8
    spritesheets = {}
    def __init__(self, props):
        Game.__init__(self, props)
        
    def on_tick(self, delta):
        if self.count_t("Fire")<self.max_fires:
            def dojob(f):
                fire = Fire({
                    "tick_interval": 0.1,
                    "position_x": random_int(0, GLOBAL.SCREEN_W),
                    "position_y": random_int(0, GLOBAL.SCREEN_H),  
                    "sprite_index": random_int(0, 3),
                    "spritesheet": self.spritesheets["spritesheet_fire"]
                })
                f()
            engine.task_manager.add_task(dojob)

      
    def on_begin(self):
        self.spritesheets["spritesheet_purple"] = engine.create_spritesheet([
            ['assets/purple_wizard/amg1_bk1.png', 'assets/purple_wizard/amg1_bk2.png'],
            ['assets/purple_wizard/amg1_fr1.png', 'assets/purple_wizard/amg1_fr2.png'],
            ['assets/purple_wizard/amg1_lf1.png', 'assets/purple_wizard/amg1_lf2.png'],
            ['assets/purple_wizard/amg1_rt1.png', 'assets/purple_wizard/amg1_rt2.png'],
        ])
        self.spritesheets["spritesheet_lime"] = engine.create_spritesheet([
            ['assets/lime_wizard/amg1_bk1.png', 'assets/lime_wizard/amg1_bk2.png'],
            ['assets/lime_wizard/amg1_fr1.png', 'assets/lime_wizard/amg1_fr2.png'],
            ['assets/lime_wizard/amg1_lf1.png', 'assets/lime_wizard/amg1_lf2.png'],
            ['assets/lime_wizard/amg1_rt1.png', 'assets/lime_wizard/amg1_rt2.png'],
        ])
        self.spritesheets["spritesheet_blue"] = engine.create_spritesheet([
            ['assets/blue_wizard/amg1_bk1.png', 'assets/blue_wizard/amg1_bk2.png'],
            ['assets/blue_wizard/amg1_fr1.png', 'assets/blue_wizard/amg1_fr2.png'],
            ['assets/blue_wizard/amg1_lf1.png', 'assets/blue_wizard/amg1_lf2.png'],
            ['assets/blue_wizard/amg1_rt1.png', 'assets/blue_wizard/amg1_rt2.png'],
        ])
        self.spritesheets["spritesheet_red"] = engine.create_spritesheet([
            ['assets/red_wizard/amg1_bk1.png', 'assets/red_wizard/amg1_bk2.png'],
            ['assets/red_wizard/amg1_fr1.png', 'assets/red_wizard/amg1_fr2.png'],
            ['assets/red_wizard/amg1_lf1.png', 'assets/red_wizard/amg1_lf2.png'],
            ['assets/red_wizard/amg1_rt1.png', 'assets/red_wizard/amg1_rt2.png'],
        ])
        self.spritesheets["spritesheet_cyan"] = engine.create_spritesheet([
            ['assets/cyan_wizard/amg1_bk1.png', 'assets/cyan_wizard/amg1_bk2.png'],
            ['assets/cyan_wizard/amg1_fr1.png', 'assets/cyan_wizard/amg1_fr2.png'],
            ['assets/cyan_wizard/amg1_lf1.png', 'assets/cyan_wizard/amg1_lf2.png'],
            ['assets/cyan_wizard/amg1_rt1.png', 'assets/cyan_wizard/amg1_rt2.png'],
        ])
        self.spritesheets["spritesheet_fire"] = engine.create_spritesheet([
            [
                'assets/fire_a/fire_0.png', 
                'assets/fire_a/fire_1.png',
                'assets/fire_a/fire_2.png', 
                'assets/fire_a/fire_3.png'
            ]
        ])

        from beastlib.tools import stringify_json
        engine.log(stringify_json([1, 3, 4]))

        
        char_spritesheets = [
            self.spritesheets["spritesheet_cyan"],
            self.spritesheets["spritesheet_lime"],
            self.spritesheets["spritesheet_blue"],
            self.spritesheets["spritesheet_red"]
        ]

        player = Player({
            "is_pawn": True,
            "tick_interval": 0.0333,
            "spritesheet": random_choice(char_spritesheets),
            "position_x": random_int(0, GLOBAL.SCREEN_W),
            "position_y": random_int(0, GLOBAL.SCREEN_H),
        })
    
        chars = 0
        while chars<8:
            NPC({ 
                "tick_interval": 0.0333,
                "spritesheet": random_choice(char_spritesheets),
                "position_x": random_int(0, GLOBAL.SCREEN_W),
                "position_y": random_int(0, GLOBAL.SCREEN_H),
            })
            chars+=1


game = DungeonGame({
    "tick_interval": 1
})

engine = Engine({
    "debug": True,
    "is_loading": True,
    "create_renderer": True,
    "create_task_manager": True
})
stackless.run()