
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

DEFAULT_BUTTON_THROTTLE = 0.025
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

class PadButtonsObserver(CoreObject):
    TAG = "padbuttonsobserver"
    pad_buttons_observe_enabled = False
    def __init__(self, props={}):
        CoreObject.__init__(self, props)
        now = time()
        
        self.pad_buttons_observer_state = {
            "button_throttle": {
                "cross":DEFAULT_BUTTON_THROTTLE,
                "triangle":DEFAULT_BUTTON_THROTTLE,
                "square":DEFAULT_BUTTON_THROTTLE,
                "circle":DEFAULT_BUTTON_THROTTLE,
                "up":DEFAULT_BUTTON_THROTTLE,
                "down":DEFAULT_BUTTON_THROTTLE,
                "left": DEFAULT_BUTTON_THROTTLE,
                "right":DEFAULT_BUTTON_THROTTLE
            },
            "prev_time": {
                "cross":now,
                "triangle":now,
                "square":now,
                "circle":now,
                "up":now,
                "down":now,
                "left": now,
                "right":now
            }
        }

        self.pad_buttons_observe_enabled = self.get(props, "is_pawn", False)
    def on_tick(self):
        if self.pad_buttons_observe_enabled:
            pad = GLOBAL["engine"].Controller()
            if   pad.cross:     self.is_button_throttled("cross") and self.on_pad_cross(pad)
            elif pad.triangle:  self.is_button_throttled("triangle") and self.on_pad_triangle(pad)
            elif pad.circle:    self.is_button_throttled("circle") and self.on_pad_circle(pad)
            elif pad.square:    self.is_button_throttled("square") and self.on_pad_square(pad)
            elif pad.down:      self.is_button_throttled("down") and self.on_pad_down(pad)
            elif pad.up:        self.is_button_throttled("up") and self.on_pad_up(pad)
            elif pad.left:      self.is_button_throttled("left") and self.on_pad_left(pad)
            elif pad.right:     self.is_button_throttled("right") and self.on_pad_right(pad)
    def on_pad_cross(self, pad): pass
    def on_pad_triangle(self, pad): pass
    def on_pad_circle(self, pad): pass
    def on_pad_square(self, pad): pass
    def on_pad_down(self, pad): pass
    def on_pad_up(self, pad): pass
    def on_pad_left(self, pad): pass
    def on_pad_right(self, pad): pass

    def set_button_throttling(self, name, delay=DEFAULT_BUTTON_THROTTLE):
        self.pad_buttons_observer_state["button_throttle"][name] = delay
    def is_button_throttled(self, name):
        delay = self.pad_buttons_observer_state["button_throttle"][name]
        now = time()
        if now - self.pad_buttons_observer_state["prev_time"][name]<delay:
            return False
        else:
            self.pad_buttons_observer_state["prev_time"][name] = now
            return True