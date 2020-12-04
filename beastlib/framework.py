
## created by sanyabeast <a.gvrnsK@gmail.com>
## 04 dec 2020

import psp2d
import pspos
import pspnet
import pspmp3
import pspogg
from time import time, localtime
import datetime
import stackless
import sys
from beastlib.core import CoreObject, Tickable, GLOBAL, PadButtonsObserver, DEFAULT_BUTTON_THROTTLE, SCREEN_W, SCREEN_H
from beastlib.types import *


def_font = psp2d.Font('assets/font.png')    

class Renderer(Tickable):
    TAG = "renderer"
    is_renderer = True
    def __init__(self, props={}):
        Tickable.__init__(self, props)
        self.renderables = []
        GLOBAL["rend"] = self
    def on_tick(self, delta):
        self.screen.clear(psp2d.Color(0,0,0,255))
        for renderable in self.renderables:
            renderable.draw(self.screen)
        self.screen.swap()
    def die (self):
        for renderable in self.renderables:
            renderable.alive = False
        CoreObject.die(self)

    def add_child(self, child=None, child_id=None):
        Tickable.add_child(self, child, child_id)
        if (child.is_renderable):
            self.renderables.append(child)

class Engine(Tickable):
    TAG = "engine"
    is_engine = True
    Controller = psp2d.Controller
    debug = False
    rend = None
    def __init__(self, props={}):
        Tickable.__init__(self, props)
        GLOBAL["engine"] = self
        pspos.setclocks( self.get(props, "cpu_clock", 333), self.get(props, "mem_clock", 166) )
        self.add_child(Renderer(props))
        self.debug = self.get(props, "debug")
        if (self.debug):  GLOBAL["logger"] = DebugLog({ "rend": self.rend  })
        self.log("created")
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
        print("die")
        CoreObject.die(self)
        
class Renderable(Tickable):
    TAG = "renderable"
    is_renderable = True
    def __init__(self, props):
        Tickable.__init__(self, props)
        rend = props["rend"] if ("rend" in props and props["rend"]!=None) else GLOBAL["rend"]
        rend.add_child(self) # Adds this agent to the renderer
        self.position = Vec2(self.get(props, "position_x", 0), self.get(props, "position_y", 0))
    def draw(self, screen):
        pass

class Actor(Renderable, PadButtonsObserver):
    TAG = "actor"
    is_actor = True
    is_pawn = False
    pad_state = {}
    def __init__(self, props):
        Renderable.__init__(self, props)
        PadButtonsObserver.__init__(self, props)
    def on_tick(self, delta=1):
        Renderable.on_tick(self, delta)
        PadButtonsObserver.on_tick(self, delta)

class DebugLog(Renderable):
    TAG = "debuglog"
    is_debuglog = True
    lines = []
    max_log = 20
    tick_interval = 0.5
    def __init__(self, props):
        Renderable.__init__(self, props)
    def draw(self, screen):
        c = 0
        for t in self.lines:
            def_font.drawText(screen, 10, c*10, t)
            c+=1
    def add_line(self, t):
        self.lines.append(t)
        lines_len = len(self.lines)
        self.lines = self.lines[max(0, lines_len-self.max_log):lines_len]


