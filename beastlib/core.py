
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
from beastlib.tools import *
import random
import threading
from beastlib.tools import get_random_string

font = psp2d.Font('assets/font.png')    
screen = psp2d.Screen()
screen.clear(psp2d.Color(0,0,0,255))

class GLOBAL(object):
    SCREEN = screen
    REGISTER = {}
    TYPED_REGISTER = {}
    STATE = {}
    SCREEN_W = 480
    SCREEN_H = 272
    ETHALON_TICK_INTERVAL = 0.0333333
    DEFAULT_BUTTON_THROTTLE = 0.025
    DEFAULT_FONT = font

class CoreObject(object):
    alive = False
    screen = screen
    children_count = 0
    child_id = None
    parent = None
    UUID = None

    def __init__(self, props={}):
        from beastlib.tools import get_class_tags
        self.TAG = self.__class__.__name__
        self.TAGS = get_class_tags(self.__class__)
        self.UUID = get_random_string(self.TAG)
        self.children = {}
        self.alive = True
        self.register_object()
    def find_object_by_type(self, object_type="Object"):
        r = None
        if object_type in GLOBAL.TYPED_REGISTER:
            for k in GLOBAL.TYPED_REGISTER[object_type]:
                r = GLOBAL.TYPED_REGISTER[object_type][k] 
                break
        return r
    def is_a (object_type):
        return object_type in self.TAGS
    def find_objects_by_type(self, object_type="Object"):
        r = {}
        if object_type in GLOBAL.TYPED_REGISTER:
            r = GLOBAL.TYPED_REGISTER[object_type]
        return r    
    def register_object(self):
        GLOBAL.REGISTER[self.UUID] = self
        
        for k in self.TAGS:
            if not k in GLOBAL.TYPED_REGISTER: GLOBAL.TYPED_REGISTER[k] = {}
            GLOBAL.TYPED_REGISTER[k][self.UUID] = self

    def unregister_object(self):
        if self.UUID in GLOBAL.REGISTER:
            del GLOBAL.REGISTER[self.UUID]
        for k in self.TAGS:
            if k in GLOBAL.TYPED_REGISTER and self.UUID in GLOBAL.TYPED_REGISTER[k]:
                del GLOBAL.TYPED_REGISTER[k][self.UUID]
            
    def get(self, dict, path, def_value=None):
        return dict[path] if path in dict else def_value
    def die(self):
        self.alive = False
        if self.parent:
            self.parent.remove_child(self)
        for k in self.children: self.children[k].die()
        self.unregister_object()
    def add_child(self, child=None, child_id=None):
        if (child==None):
            self.log(data="child is None", to_console=True)
            return
            
        if child_id==None: child_id=str(self.children_count)
        child.child_id = child_id
        child.parent = self
        self.children[child_id]=child
        self.children_count+=1
        return child

    def remove_child(self, child=None, child_id=None):
        id = child.child_id if child!=None else child_id
        c = self.children[id]
        del self.children[id]
        c.parent=None
        c.child_id = None
        return c
    def log(self, data="...", to_console=False, to_screen=True):
        t = "%s: %s" % (self.TAG, str(data))
        if to_console: print(t)
        if to_screen:
            debug_log = self.find_object_by_type("DebugLog")
            if (debug_log!=None):
                debug_log.add_line(t)
    
class Tickable(CoreObject):
    tick_interval = GLOBAL.ETHALON_TICK_INTERVAL
    prev_tick_time = time()
    tick_delta = 1
    tick_started = False
    def __init__(self, props={}):
        CoreObject.__init__(self, props)
        self.ch = stackless.channel()
        stackless.tasklet(self.tick)()
        self.set_tick_interval(self.get(props, "tick_interval", self.tick_interval))
    def set_tick_interval(self, interval=1/30):
        self.tick_interval= interval
    def tick(self):
        while self.alive:
            now = time()
            if now - self.prev_tick_time>self.tick_interval:
                self.tick_delta = delta = (now - self.prev_tick_time)/GLOBAL.ETHALON_TICK_INTERVAL
                self.on_tick(delta)
                self.prev_tick_time = now
            stackless.schedule()
    def on_tick(self, delta=1):
        if not self.tick_started:
            self.tick_started = True
            self.on_begin()
    def on_begin(self):
        pass

class PadButtonsObserver(CoreObject):
    pad_buttons_observe_enabled = False
    def __init__(self, props={}):
        CoreObject.__init__(self, props)
        now = time()
        
        self.pad_buttons_observer_state = {
            "button_throttle": {
                "cross":GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "triangle":GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "square":GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "circle":GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "up":GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "down":GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "left": GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "right":GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "select":GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "start":GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "l":GLOBAL.DEFAULT_BUTTON_THROTTLE,
                "r":GLOBAL.DEFAULT_BUTTON_THROTTLE,
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
            pad = self.find_object_by_type("Engine").Controller()
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

    def set_button_throttling(self, name, delay=GLOBAL.DEFAULT_BUTTON_THROTTLE):
        self.pad_buttons_observer_state["button_throttle"][name] = delay
    def is_button_throttled(self, name):
        delay = self.pad_buttons_observer_state["button_throttle"][name]
        now = time()
        if now - self.pad_buttons_observer_state["prev_time"][name]<delay:
            return False
        else:
            self.pad_buttons_observer_state["prev_time"][name] = now
            return True