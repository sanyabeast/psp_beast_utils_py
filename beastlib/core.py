
## created by sanyabeast <a.gvrnsk@gmail.com>
## 4 dec 2020

import psp2d
import pspos
import pspnet
import pspmp3
import pspogg
from time import time, localtime
import datetime
import stackless
import sys
from beastlib.types import *

screen = psp2d.Screen()
screen.clear(psp2d.Color(0,0,0,255))
SCREEN_W = 480
SCREEN_H = 272
GLOBAL = {
    "logger": None,
    "engine": None,
    "rend": None,
    "screen": screen
}

class CoreObject(object):
    TAG = "object"
    alive = False
    screen = screen
    def __init__(self, props={}):
        self.children = {}
        self.alive = True
    def get(self, dict, path, def_value=None):
        return dict[path] if path in dict else def_value
    def die(self):
        self.alive = False
        for k in self.children: k.die()
    def add_child(self, child_id, child):
        self.children[child_id]=child
        return child
    def log(self, data="..."):
        t = "%s: %s" % (self.TAG, str(data))
        print(t)
        if GLOBAL["logger"]!=None: 
            GLOBAL["logger"].add_line(t)

class Tickable(CoreObject):
    TAG = "agent"
    def __init__(self, props={}):
        CoreObject.__init__(self, props)
        self.ch = stackless.channel()
        stackless.tasklet(self.tick)()
        self.log("created")
    def tick(self):
        while self.alive:
            self.on_tick()
            stackless.schedule()
    def on_tick(self):
        pass

