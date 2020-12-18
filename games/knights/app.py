
## created by sanyabeast <a.gvrnsk@gmail.com>
## 17 dec 2020

from beast.core import GLOBAL, Launcher, create_spritesheet, LOG
from beast.tools import random_bool, random_choice, random_int
from beast.framework import Engine, Pawn, Actor, Tickable, TaskManager, Game, PlayerController
import math

class SomePawn(Pawn):
    TICK_INTERVAL=0.1
    sprite_move_index = 1
    move_direction_x = 0
    move_direction_y = 0
    speed = 2
    sprite_index = 0
    spritesheet = None

    def set_move_direction(self, move_x=0, move_y=0):
        sprite_move_index = (3 if move_x>0 else 2) if abs(move_x)>abs(move_y) else (1 if move_y>0 else 0)
        self.sprite_move_index=sprite_move_index
        self.move_direction_x = move_x
        self.move_direction_y = move_y
    def set_speed(self, speed=0):
        self.speed=speed
    def ON_TICK(self, DELTA=1):
        Pawn.ON_TICK(self, DELTA)
        self.POSITION_X += self.move_direction_x * self.speed
        self.POSITION_Y += self.move_direction_y * self.speed

class Player(SomePawn):
    def __init__(self, PROPS, INIT_PROPS=True):
        SomePawn.__init__(self, PROPS, False)
        if INIT_PROPS: self.INIT_PROPS(PROPS)
        self.sprite_index = False
        self.sprite_move_index = 1
        self.speed = 3
        self.sprint = 0
        self.sprint_speed = 4
        self.lastPad = self.TIME()
        self.spritesheet = self.GET(PROPS, "spritesheet")
        self.sprite = self.spritesheet[self.sprite_move_index][int(self.sprite_index)]

    def ON_TICK(self, DELTA=1):
        SomePawn.ON_TICK(self, DELTA)
        if self.speed>0:
            if self.move_direction_x!=0: self.sprite_index = math.floor(self.POSITION_X)%3!=0
            if self.move_direction_y!=0:self.sprite_index = math.floor(self.POSITION_Y)%3!=0
        self.sprite = self.spritesheet[self.sprite_move_index][int(self.sprite_index)]
    def DRAW(self):
        GLOBAL.SCREEN.blit(self.sprite, 0.5, 0, self.sprite.width ,
            self.sprite.height, int(self.POSITION_X), int(self.POSITION_Y), True)
               
class NPC(SomePawn):
    def __init__(self, PROPS, INIT_PROPS=True):
        SomePawn.__init__(self, PROPS, False)
        if INIT_PROPS: self.INIT_PROPS(PROPS)
        self.created_at = self.TIME()
        self.lifetime = random_int(10, 60)
        self.sprite_index = False
        self.sprite_move_index = 0
        self.speed = 2
        self.lastPad = self.TIME()
        self.spritesheet = self.GET(PROPS, "spritesheet")
        self.sprite = self.spritesheet[self.sprite_move_index][int(self.sprite_index)]
        self.count = 20

    def ON_TICK(self, DELTA=1):
        # now = self.TIME()
        # if (now-self.created_at>self.lifetime): 
        #     self.DESTROY()
        #     return
        SomePawn.ON_TICK(self, DELTA)
        self.sprite = self.spritesheet[self.sprite_move_index][int(self.sprite_index)]
        if random_bool(0.05) or self.sprite_move_index == 0 and \
           (not self.lastPad or self.TIME() - self.lastPad >= 0.05):
            self.lastPad = self.TIME()
            if self.POSITION_Y - (self.speed*self.TICK_DELTA) >= 20:
                self.POSITION_Y -= (self.speed*self.TICK_DELTA)
                self.sprite_index = not self.sprite_index
            else:
                self.sprite_move_index = 2
        if random_bool(0.05) or self.sprite_move_index == 2 and \
           (not self.lastPad or self.TIME() - self.lastPad >= 0.05):
            self.lastPad = self.TIME()
            if self.POSITION_X - (self.speed*self.TICK_DELTA) > 0:
                self.POSITION_X -= (self.speed*self.TICK_DELTA)
                self.sprite_index = not self.sprite_index
            else:
                self.sprite_move_index = 1
        if random_bool(0.05) or self.sprite_move_index == 1 and \
           (not self.lastPad or self.TIME() - self.lastPad >= 0.05):
            self.lastPad = self.TIME()
            if self.POSITION_Y + self.sprite.height + (self.speed*self.TICK_DELTA) < 252:
                self.POSITION_Y += (self.speed*self.TICK_DELTA)
                self.sprite_index = not self.sprite_index
            else:
                self.sprite_move_index = 3
        if random_bool(0.05) or self.sprite_move_index == 3 and \
           (not self.lastPad or self.TIME() - self.lastPad >= 0.05):
            self.lastPad = self.TIME()
            if self.POSITION_X + self.sprite.width + (self.speed*self.TICK_DELTA) < 450:
                self.POSITION_X += (self.speed*self.TICK_DELTA)
                self.sprite_index = not self.sprite_index
            else:
                self.sprite_move_index = 0

    def DRAW(self):
        GLOBAL.SCREEN.blit(self.sprite, 0, 0, self.sprite.width,
            self.sprite.height, int(self.POSITION_X), int(self.POSITION_Y), True)

class Fire(Actor):
    def __init__(self, PROPS, INIT_PROPS=True):
        Actor.__init__(self, PROPS, False)
        if INIT_PROPS: self.INIT_PROPS(PROPS)
        self.sprite_index = self.GET(PROPS, "sprite_index", 0)
        self.sprite_move_index = 0
        self.speed = 2
        self.lastPad = self.TIME()
        self.spritesheet = self.GET(PROPS, "spritesheet")
        self.sprite = self.spritesheet[0][int(self.sprite_index)]
        self.count = 20

    def ON_TICK(self, DELTA=1):
        Actor.ON_TICK(self, DELTA)
        self.sprite = self.spritesheet[0][self.sprite_index]
        self.sprite_index = (self.sprite_index+1)%4

    def DRAW(self):
        GLOBAL.SCREEN.blit(self.sprite, 0, 0, self.sprite.width,
            self.sprite.height, self.POSITION_X, self.POSITION_Y, True)
    def ON_DESTROY(self, REASON):
        self.LOG("the fire is out")

class SomePlayerController(PlayerController):
    def __init__(self, PROPS, INIT_PROPS=True):
        PlayerController.__init__(self, PROPS, False)
        if INIT_PROPS: self.I(PROPS)
    @property
    def player(self):
        return self.FIND_T("Player")
    # def ON_PAD_TRIANGLE(self, PAD):
    #     from beast.tools import get_random_string
    #     def dojob(f):
    #         self.LOG(get_random_string("test"))
    #         f()
    #     engine.TaskManager.ADD_TASK(dojob)
    # def ON_PAD_CROSS(self, PAD):
    #     self.LOG("cross")
    #     engine.DESTROY()
    # def ON_PAD_CIRCLE(self, PAD):
    #     self.LOG("circle")
    # def ON_PAD_SQUARE(self, PAD):
    #     def dojob(f):
    #         LOG("1")
    #         LOG("2")
    #         LOG("3")
    #         if self.FIND_T("Fire")!=None:
    #             self.FIND_T("Fire").DESTROY()
    #         f()
    #     engine.TaskManager.ADD_TASK(dojob)
    # def ON_PAD_LEFT(self, PAD):
    #     self.player.set_sprite_move_index(2)
    # def ON_PAD_RIGHT(self, PAD):
    #     self.player.set_sprite_move_index(3)
    # def ON_PAD_UP(self, PAD):
    #     self.player.set_sprite_move_index(0)
    # def ON_PAD_DOWN(self, PAD):
    #     self.player.set_sprite_move_index(1)
    def ON_PAD_PRESSED(self, NAME, PAD, DPAD, ANALOG):
        self.LOG(str(DPAD["length"]))
        self.player.set_speed(DPAD["length_c"])
        if NAME=="left":
            self.player.set_move_direction(DPAD["x"], DPAD["y"])
        elif NAME=="right":
            self.player.set_move_direction(DPAD["x"], DPAD["y"])
        elif NAME=="up":
            self.player.set_move_direction(DPAD["x"], DPAD["y"])
        elif NAME=="down":
            self.player.set_move_direction(DPAD["x"], DPAD["y"])
        elif NAME=="cross":
            self.LOG("cross")
            self.GET_ENGINE().DESTROY()
        elif NAME=="square":
            self.LOG("cross")
            def dojob(f):
                LOG("1")
                LOG("2")
                LOG("3")
                if self.FIND_T("Fire")!=None:
                    self.FIND_T("Fire").DESTROY()
                f()
            self.GET_ENGINE().TaskManager.ADD_TASK(dojob)
        elif NAME=="triangle":
            from beast.tools import get_random_string
            def dojob(f):
                self.LOG(get_random_string("test"))
                f()
            self.GET_ENGINE().TaskManager.ADD_TASK(dojob)
    def ON_PAD_RELEASED(self, NAME, PAD, DPAD, ANALOG):
        self.LOG(NAME)
        self.player.set_speed(DPAD["length_c"])
        if NAME=="left":
            self.player.set_move_direction(DPAD["x"], DPAD["y"])
        elif NAME=="right":
            self.player.set_move_direction(DPAD["x"], DPAD["y"])
        elif NAME=="up":
            self.player.set_move_direction(DPAD["x"], DPAD["y"])
        elif NAME=="down":
            self.player.set_move_direction(DPAD["x"], DPAD["y"])
            
class App(Game):
    max_fires = 16
    max_npcs = 8
    spritesheets = {}
    def __init__(self, PROPS, INIT_PROPS=True):
        Game.__init__(self, PROPS, False)
        if INIT_PROPS: self.INIT_PROPS(PROPS)
        
    def ON_TICK(self, DELTA):
        if self.COUNT_T("Fire")<self.max_fires:
            pass
            def dojob(f):
                fire = Fire({
                    "TICK_INTERVAL": 0.2,
                    "POSITION_X": random_int(0, GLOBAL.SCREEN_W),
                    "POSITION_Y": random_int(0, GLOBAL.SCREEN_H),  
                    "sprite_index": random_int(0, 3),
                    "spritesheet": self.spritesheets["spritesheet_fire"]
                })
                f()
            self.GET_ENGINE().TaskManager.ADD_TASK(dojob)

      
    def ON_BEGIN(self):
        self.spritesheets["spritesheet_purple"] = create_spritesheet([
            ['assets/purple_wizard/amg1_bk1.png', 'assets/purple_wizard/amg1_bk2.png'],
            ['assets/purple_wizard/amg1_fr1.png', 'assets/purple_wizard/amg1_fr2.png'],
            ['assets/purple_wizard/amg1_lf1.png', 'assets/purple_wizard/amg1_lf2.png'],
            ['assets/purple_wizard/amg1_rt1.png', 'assets/purple_wizard/amg1_rt2.png'],
        ])
        self.spritesheets["spritesheet_lime"] = create_spritesheet([
            ['assets/lime_wizard/amg1_bk1.png', 'assets/lime_wizard/amg1_bk2.png'],
            ['assets/lime_wizard/amg1_fr1.png', 'assets/lime_wizard/amg1_fr2.png'],
            ['assets/lime_wizard/amg1_lf1.png', 'assets/lime_wizard/amg1_lf2.png'],
            ['assets/lime_wizard/amg1_rt1.png', 'assets/lime_wizard/amg1_rt2.png'],
        ])
        self.spritesheets["spritesheet_blue"] = create_spritesheet([
            ['assets/blue_wizard/amg1_bk1.png', 'assets/blue_wizard/amg1_bk2.png'],
            ['assets/blue_wizard/amg1_fr1.png', 'assets/blue_wizard/amg1_fr2.png'],
            ['assets/blue_wizard/amg1_lf1.png', 'assets/blue_wizard/amg1_lf2.png'],
            ['assets/blue_wizard/amg1_rt1.png', 'assets/blue_wizard/amg1_rt2.png'],
        ])
        self.spritesheets["spritesheet_red"] = create_spritesheet([
            ['assets/red_wizard/amg1_bk1.png', 'assets/red_wizard/amg1_bk2.png'],
            ['assets/red_wizard/amg1_fr1.png', 'assets/red_wizard/amg1_fr2.png'],
            ['assets/red_wizard/amg1_lf1.png', 'assets/red_wizard/amg1_lf2.png'],
            ['assets/red_wizard/amg1_rt1.png', 'assets/red_wizard/amg1_rt2.png'],
        ])
        self.spritesheets["spritesheet_cyan"] = create_spritesheet([
            ['assets/cyan_wizard/amg1_bk1.png', 'assets/cyan_wizard/amg1_bk2.png'],
            ['assets/cyan_wizard/amg1_fr1.png', 'assets/cyan_wizard/amg1_fr2.png'],
            ['assets/cyan_wizard/amg1_lf1.png', 'assets/cyan_wizard/amg1_lf2.png'],
            ['assets/cyan_wizard/amg1_rt1.png', 'assets/cyan_wizard/amg1_rt2.png'],
        ])
        self.spritesheets["spritesheet_fire"] = create_spritesheet([
            [
                'assets/fire_a/fire_0.png', 
                'assets/fire_a/fire_1.png',
                'assets/fire_a/fire_2.png', 
                'assets/fire_a/fire_3.png'
            ]
        ])

        from beast.tools import stringify_json
        LOG(stringify_json([1, 3, 4]))
        char_spritesheets = [
            self.spritesheets["spritesheet_cyan"],
            self.spritesheets["spritesheet_lime"],
            self.spritesheets["spritesheet_blue"],
            self.spritesheets["spritesheet_red"]
        ]

        player = Player({
            "IS_PAWN": True,
            "TICK_INTERVAL": 0.033,
            "POSITION_X": random_int(0, GLOBAL.SCREEN_W),
            "POSITION_Y": random_int(0, GLOBAL.SCREEN_H),
            "spritesheet": random_choice(char_spritesheets),
        })
    
        chars = 0
        while chars<8:
            NPC({ 
                "TICK_INTERVAL": 0.05,
                "POSITION_X": random_int(0, GLOBAL.SCREEN_W),
                "POSITION_Y": random_int(0, GLOBAL.SCREEN_H),
                "spritesheet": random_choice(char_spritesheets),
            })
            chars+=1

        player_controller = SomePlayerController({

        })
