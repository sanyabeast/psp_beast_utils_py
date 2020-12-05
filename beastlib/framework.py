
## created by sanyabeast <a.gvrnsK@gmail.com>
## 04 dec 2020

import psp2d
import pspos
import pspnet
import pspmp3
import pspogg
from time import time, localtime, sleep
import datetime
import stackless
import sys
from beastlib.core import CoreObject, Tickable, GLOBAL, PadButtonsObserver
from beastlib.types import Vec2


class Renderer(Tickable):
    is_Renderer = True
    def __init__(self, props={}):
        Tickable.__init__(self, props)
        from beastlib.actors import Loader
        self.loader = Loader(props)
        if self.get(props, "is_loading")==True: self.set_loading(True)

    def on_tick(self, delta):
        GLOBAL.SCREEN.clear(psp2d.Color(0,0,0,255))
        actors = self.find_objects_by_type("Actor")
        for a in actors:
            if actors[a].visible: actors[a].draw()
        GLOBAL.SCREEN.swap()
    def die (self):
        Tickable.die(self)

    def set_loading(self, show_loader=True):
        self.show_loader = False
        self.loader.visible = False

class Engine(Tickable):
    is_Engine = True
    Controller = psp2d.Controller
    debug = False
    rend = None
    debug_log = None
    is_loading = False
    def __init__(self, props={}):
        Tickable.__init__(self, props)
        pspos.setclocks( self.get(props, "cpu_clock", 333), self.get(props, "mem_clock", 166) )
        self.renderer = Renderer(props)
        self.debug = self.get(props, "debug", False)
        self.is_loading = self.get(props, "is_loading", False)
        from beastlib.actors import DebugLog
        if (self.debug): self.debug_log = DebugLog({ "rend": self.rend  })
    def create_spritesheet(self, urls):
        sprites = []
        for u in urls:
            if type(u) is str:
                sprites.append(psp2d.Image(u))
            elif type(u) is list:
                r = []
                for uu in u:
                    r.append(psp2d.Image(uu))
                sprites.append(r) #Direction = north   = 0
            elif (type(u) is tuple):
                sprites.append((psp2d.Image(u[0]), psp2d.Image(u[1]))) #Direction = north   = 0
        return sprites
    def load_font(self, url):
        return psp2d.Font(url)   
    def die(self):
        Tickable.die(self)
    def set_loading(self, is_loading=False):
        self.is_loading = is_loading
        # self.find_object_by_type("Renderer").set_loading(False)

class Actor(Tickable):
    visible = True
    def __init__(self, props):
        Tickable.__init__(self, props)
        rend = props["rend"] if ("rend" in props and props["rend"]!=None) else self.find_object_by_type("Renderer")
        self.position = Vec2(self.get(props, "position_x", 0), self.get(props, "position_y", 0))
    def draw(self):
        pass

class Pawn(Actor, PadButtonsObserver):
    TAG = "Pawn"
    is_actor = True
    is_pawn = False
    pad_state = {}
    def __init__(self, props):
        Actor.__init__(self, props)
        PadButtonsObserver.__init__(self, props)
    def on_tick(self, delta=1):
        Actor.on_tick(self, delta)
        PadButtonsObserver.on_tick(self, delta)

