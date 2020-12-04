
## created by sanyabeast <a.gvrnsk@gmail.com>
## 4 dec 2020

import psp2d
import pspos
import pspnet
import pspmp3
import pspogg
from time import time, localtime, sleep
import datetime
import stackless
import sys
from beastlib.types import *
import random


ETHALON_TICK_INTERVAL = 0.0333333
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
    children_count = 0
    def __init__(self, props={}):
        self.children = {}
        self.alive = True
    def get(self, dict, path, def_value=None):
        return dict[path] if path in dict else def_value
    def die(self):
        self.alive = False
        for k in self.children: self.children[k].die()
    def add_child(self, child=None, child_id=None):
        if (child==None):
            self.log(data="child is None", to_console=True)
            return
        if child_id==None: child_id=str(self.children_count)
        self.children[child_id]=child
        self.children_count+=1
        return child
    def log(self, data="...", to_console=False, to_screen=True):
        t = "%s: %s" % (self.TAG, str(data))
        if to_console: print(t)
        if to_screen and GLOBAL["logger"]!=None: 
            GLOBAL["logger"].add_line(t)
    def random_bool(self, f=1):
        return random.random()< 0.5 * (f)
    def random_int(self, a=0, b=100):
        return random.randint(a, b)
    def random_choice(self, arr=[]):
        return random.choice(arr)

class Tickable(CoreObject):
    TAG = "agent"
    tick_interval = ETHALON_TICK_INTERVAL
    prev_tick_time = time()
    tick_delta = 1
    def __init__(self, props={}):
        CoreObject.__init__(self, props)
        self.ch = stackless.channel()
        stackless.tasklet(self.tick)()
        self.set_tick_interval(self.get(props, "tick_interval", self.tick_interval))
        self.log("created")
    def set_tick_interval(self, interval=1/30):
        self.tick_interval= interval
        print self.tick_interval
    def tick(self):
        
        while self.alive:
            now = time()
            if now - self.prev_tick_time>self.tick_interval:
                self.tick_delta = delta = (now - self.prev_tick_time)/ETHALON_TICK_INTERVAL
                self.on_tick(delta)
                self.prev_tick_time = now
            stackless.schedule()
    def on_tick(self, delta=1):
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
                "right":DEFAULT_BUTTON_THROTTLE,
                "select":DEFAULT_BUTTON_THROTTLE,
                "start":DEFAULT_BUTTON_THROTTLE,
                "l":DEFAULT_BUTTON_THROTTLE,
                "r":DEFAULT_BUTTON_THROTTLE,
            },
            "prev_time": {
                "cross":now,
                "triangle":now,
                "square":now,
                "circle":now,
                "up":now,
                "down":now,
                "left": now,
                "right":now,
                "select":now,
                "start":now,
                "l":now,
                "r":now,
            }
        }

        self.pad_buttons_observe_enabled = self.get(props, "is_pawn", False)
    def on_tick(self, delta=1):
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
            elif pad.start:     self.is_button_throttled("start") and self.on_pad_start(pad)
            elif pad.select:    self.is_button_throttled("select") and self.on_pad_select(pad)
            elif pad.l:         self.is_button_throttled("l") and self.on_pad_l(pad)
            elif pad.r:         self.is_button_throttled("r") and self.on_pad_r(pad)


    def on_pad_cross(self, pad): pass
    def on_pad_triangle(self, pad): pass
    def on_pad_circle(self, pad): pass
    def on_pad_square(self, pad): pass
    def on_pad_down(self, pad): pass
    def on_pad_up(self, pad): pass
    def on_pad_left(self, pad): pass
    def on_pad_right(self, pad): pass
    def on_pad_start(self, pad): pass
    def on_pad_select(self, pad): pass
    def on_pad_l(self, pad): pass
    def on_pad_r(self, pad): pass

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