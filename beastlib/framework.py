
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
from beastlib.core import CoreObject, Tickable, GLOBAL, PadButtonsObserver, DEFAULT_BUTTON_THROTTLE
from beastlib.types import *


def_font = psp2d.Font('assets/font.png')    

class Renderer(Tickable):
    TAG = "renderer"
    def __init__(self, props={}):
        Tickable.__init__(self, props)
        self.renderables = []
        GLOBAL["rend"] = self
    def on_tick(self):
        self.screen.clear(psp2d.Color(0,0,0,255))
        for renderable in self.renderables:
            renderable.draw(self.screen)
        self.screen.swap()
    def die (self):
        for renderable in self.renderables:
            renderable.alive = False
        CoreObject.die(self)

class Engine(Tickable):
    TAG = "engine"
    Controller = psp2d.Controller
    debug = False
    rend = None
    def __init__(self, props={}):
        Tickable.__init__(self, props)
        GLOBAL["engine"] = self
        pspos.setclocks( self.get(props, "cpu_clock", 333), self.get(props, "mem_clock", 166) )
        self.rend = self.add_child("rend", Renderer({}))
        self.debug = self.get(props, "debug")
        if (self.debug):  GLOBAL["logger"] = DebugLog({ "rend": self.rend  })
        self.log("created")
    def create_spritesheet(self, urls):
        sprites = []
        for u in urls:
            sprites.append((psp2d.Image(u[0]), psp2d.Image(u[1]))) #Direction = north   = 0
        return sprites
    def load_font(self, url):
        return psp2d.Font(url)   
    def die(self):
        print("die")
        CoreObject.die(self)
        
class Renderable(Tickable):
    TAG = "renderable"
    def __init__(self, props):
        Tickable.__init__(self, props)
        self.rend = props["rend"]   
        self.rend.renderables.append(self) # Adds this agent to the renderer
        self.position = Vec2(0, 0)
    def draw(self, screen):
        pass

class Actor(Renderable, PadButtonsObserver):
    TAG = "actor"
    is_pawn = False
    pad_state = {}
    def __init__(self, props):
        Renderable.__init__(self, props)
        PadButtonsObserver.__init__(self, props)
    def on_tick(self):
        Renderable.on_tick(self)
        PadButtonsObserver.on_tick(self)
    #     if self.is_pawn:
    #         pad = GLOBAL["engine"].Controller()
    #         if   pad.cross:     self.is_button_throttled("cross") and self.on_pad_cross(pad)
    #         elif pad.triangle:  self.is_button_throttled("triangle") and self.on_pad_triangle(pad)
    #         elif pad.circle:    self.is_button_throttled("circle") and self.on_pad_circle(pad)
    #         elif pad.square:    self.is_button_throttled("square") and self.on_pad_square(pad)
    #         elif pad.down:      self.is_button_throttled("down") and self.on_pad_down(pad)
    #         elif pad.up:        self.is_button_throttled("up") and self.on_pad_up(pad)
    #         elif pad.left:      self.is_button_throttled("left") and self.on_pad_left(pad)
    #         elif pad.right:     self.is_button_throttled("right") and self.on_pad_right(pad)
    # def on_pad_cross(self, pad): pass
    # def on_pad_triangle(self, pad): pass
    # def on_pad_circle(self, pad): pass
    # def on_pad_square(self, pad): pass
    # def on_pad_down(self, pad): pass
    # def on_pad_up(self, pad): pass
    # def on_pad_left(self, pad): pass
    # def on_pad_right(self, pad): pass

    

class DebugLog(Renderable):
    TAG = "debuglog"
    lines = []
    max_log = 10
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


