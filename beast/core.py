
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
from beast.btypes import *
from beast.tools import *
import random
import threading
from beast.tools import get_random_string
import types

font = psp2d.Font('assets/font.png')    
screen = psp2d.Screen()
screen.clear(psp2d.Color(0,0,0,255))

class GLOBAL(object):
    SCREEN = screen
    REGISTER = {}
    TYPED_REGISTER_COUNT = {}
    TYPED_REGISTER = {}
    STATE = {}
    SCREEN_W = 480
    SCREEN_H = 272
    ETHALON_TICK_INTERVAL = 0.0333333
    DEFAULT_BUTTON_THROTTLE = 0.025
    DEFAULT_FONT = font
    NON_CONFIGURABLE_PROPS = ["TAG", "TAGS", "UUID", "IS_ALIVE", "PROPS_IS_INITED"]

class CoreObject(object):
    IS_ALIVE = False
    UUID = None
    PROPS_IS_INITED = False
    def __init__(self, PROPS={}, INIT_PROPS=True):
        from beast.tools import get_class_tags
        self.TAG = self.__class__.__name__
        self.TAGS = get_class_tags(self.__class__)
        self.UUID = get_random_string(self.TAG + "-")
        if INIT_PROPS: self.INIT_PROPS(PROPS)
        self.IS_ALIVE = True
        self.REGISTER_OBJECT()
    def I(self, PROPS={}):
        return self.INIT_PROPS(PROPS)
    def INIT_PROPS(self, PROPS={}):
        if self.PROPS_IS_INITED: return
        self.PROPS_IS_INITED = True
        # used = []
        for k in PROPS:
            if k in GLOBAL.NON_CONFIGURABLE_PROPS:
                print("permitted to configure core prop `%s`" % (k))
                continue
            if (hasattr(self, k)):
                if type(getattr(self, k))==types.MethodType:
                    if PROPS[k]==True: getattr(self, k)(PROPS)
                else:
                    setattr(self, k, PROPS[k])
            else:
                pass
                print("%s has no prop `%s`" % (self.TAG, k))

        # for uk in used:
        #     del PROPS[uk]
    def COUNT_OBJECTS_BY_TYPE(self, OBJECT_TYPE):
        r = 0
        if OBJECT_TYPE in GLOBAL.TYPED_REGISTER_COUNT:
            r =  GLOBAL.TYPED_REGISTER_COUNT[OBJECT_TYPE]
        return r
    def FIND_OBJECT_BY_TYPE(self, OBJECT_TYPE=""):
        r = None
        if OBJECT_TYPE in GLOBAL.TYPED_REGISTER:
            for k in GLOBAL.TYPED_REGISTER[OBJECT_TYPE]:
                r = GLOBAL.TYPED_REGISTER[OBJECT_TYPE][k] 
                break
        return r
    def FIND_T(self, OBJECT_TYPE=""): return self.FIND_OBJECT_BY_TYPE(OBJECT_TYPE)
    def COUNT_T(self, OBJECT_TYPE=""): return self.COUNT_OBJECTS_BY_TYPE(OBJECT_TYPE)
    def IS_A (self, OBJECT_TYPE):
        return OBJECT_TYPE in self.TAGS
    def FIND_OBJECTS_OF_TYPE(self, OBJECT_TYPE=""):
        r = {}
        if OBJECT_TYPE in GLOBAL.TYPED_REGISTER:
            r = GLOBAL.TYPED_REGISTER[OBJECT_TYPE]
        return r    
    def REGISTER_OBJECT(self):
        GLOBAL.REGISTER[self.UUID] = self
        
        for k in self.TAGS:
            if not k in GLOBAL.TYPED_REGISTER: GLOBAL.TYPED_REGISTER[k] = {}
            if not k in GLOBAL.TYPED_REGISTER_COUNT: GLOBAL.TYPED_REGISTER_COUNT[k] = 0
            GLOBAL.TYPED_REGISTER[k][self.UUID] = self
            GLOBAL.TYPED_REGISTER_COUNT[k]+=1

    def UNREGISTER_OBJECT(self):
        if self.UUID in GLOBAL.REGISTER:
            del GLOBAL.REGISTER[self.UUID]
        for k in self.TAGS:
            if k in GLOBAL.TYPED_REGISTER and self.UUID in GLOBAL.TYPED_REGISTER[k]:
                del GLOBAL.TYPED_REGISTER[k][self.UUID]
                GLOBAL.TYPED_REGISTER_COUNT[k]-=1
            
    def GET(self, dict, path, def_value=None):
        return dict[path] if path in dict else def_value
    def DESTROY_ALL(self):
        keys = GLOBAL.REGISTER.keys()
        for ob in keys:
            if ob in GLOBAL.REGISTER and GLOBAL.REGISTER[ob].IS_ALIVE: GLOBAL.REGISTER[ob].DESTROY()
    def DESTROY(self, REASON="default"):
        self.ON_DESTROY(REASON)
        self.IS_ALIVE = False
        self.UNREGISTER_OBJECT()
    def ON_DESTROY(self, REASON="default"):
        pass
    def LOG(self, data="...", to_console=False, to_screen=True):
        t = "%s: %s" % (self.TAG, str(data))
        if to_console: print(t)
        if to_screen:
            DebugLog = self.FIND_OBJECT_BY_TYPE("DebugLog")
            if (DebugLog!=None):
                DebugLog.add_line(t)
    
class Tickable(CoreObject):
    TICK_INTERVAL = GLOBAL.ETHALON_TICK_INTERVAL
    PREV_TICK_TIME = time()
    TICK_DELTA = 1
    TICK_STARTED = False
    TICK_AUTOSTART = True
    STACKLESS_CHANNEL = None
    def __init__(self, PROPS={}, INIT_PROPS=True):
        CoreObject.__init__(self, PROPS, False)
        if INIT_PROPS: self.INIT_PROPS(PROPS)
        if (self.TICK_AUTOSTART):
            self.START_TICKING()
    def START_TICKING(self):
        self.STACKLESS_CHANNEL = stackless.channel()
        stackless.tasklet(self.TICK)()
    def TICK(self):
        while self.IS_ALIVE:
            NOW = time()
            if NOW - self.PREV_TICK_TIME>self.TICK_INTERVAL:
                if self.TICK_STARTED==True:
                    self.TICK_DELTA = delta = (NOW - self.PREV_TICK_TIME)/GLOBAL.ETHALON_TICK_INTERVAL
                    self.ON_TICK(delta)
                    self.PREV_TICK_TIME = NOW
                else:
                    self.TICK_STARTED = True
                    self.ON_BEGIN()
            stackless.schedule()
    def ON_TICK(self, delta=1):
        pass    
    def ON_BEGIN(self):
        if not self.PROPS_IS_INITED: print("PROPS for %s was not inited" % self.TAG)
        pass

class PadButtonsObserver(Tickable):
    PAD_BUTTON_OBSERVER_ENABLED = True
    def __init__(self, PROPS={}, INIT_PROPS=True):
        Tickable.__init__(self, PROPS, False)
        if INIT_PROPS: self.INIT_PROPS(PROPS)
        NOW = time()
        self.BUTTONS_STATE = {
            "DPAD": { "x": 0, "y": 0, "pressed": False, "length": 0 },
            "ANALOG": { "x": 0, "y": 0, "length": 0 },
            "PRESSED": {
                "cross":False,
                "triangle":False,
                "square":False,
                "circle":False,
                "up":False,
                "down":False,
                "left": False,
                "right":False,
                "select":False,
                "start":False,
                "l":False,
                "r":False,
            },
            "BUTTON_THROTTLE": {
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
            "BUTTON_PREV_TIME": {
                "cross":NOW,
                "triangle":NOW,
                "square":NOW,
                "circle":NOW,
                "up":NOW,
                "down":NOW,
                "left": NOW,
                "right":NOW,
                "select":NOW,
                "start":NOW,
                "l":NOW,
                "r":NOW,
            }
        }

    def ON_TICK(self, DELTA=1):
        if self.PAD_BUTTON_OBSERVER_ENABLED:
            PAD = psp2d.Controller()
            self.SET_BUTTON_PRESSED("cross",      PAD.cross,            PAD)    
            self.SET_BUTTON_PRESSED("triangle",   PAD.triangle,         PAD) 
            self.SET_BUTTON_PRESSED("circle",     PAD.circle,           PAD)   
            self.SET_BUTTON_PRESSED("square",     PAD.square,           PAD)   
            self.SET_BUTTON_PRESSED("down",       PAD.down,             PAD)     
            self.SET_BUTTON_PRESSED("up",         PAD.up,               PAD)       
            self.SET_BUTTON_PRESSED("left",       PAD.left,             PAD)     
            self.SET_BUTTON_PRESSED("right",      PAD.right,            PAD)    
            self.SET_BUTTON_PRESSED("start",      PAD.start,            PAD)    
            self.SET_BUTTON_PRESSED("select",     PAD.select,           PAD)   
            self.SET_BUTTON_PRESSED("l",          PAD.l,                PAD)        
            self.SET_BUTTON_PRESSED("r",          PAD.r,                PAD)        
    def ON_PAD(self, NAME, PAD, DPAD, ANALOG):
        pass
    def ON_PAD_PRESSED(self, NAME, PAD, DPAD, ANALOG):
        pass
    def ON_PAD_RELEASED(self, NAME, PAD, DPAD, ANALOG):
        pass
    def SET_BUTTON_PRESSED(self, NAME, PRESSED=1, PAD=psp2d.Controller()):
        DPAD = self.BUTTONS_STATE["DPAD"]
        ANALOG = self.BUTTONS_STATE["ANALOG"]

        DPAD["x"]=DPAD["y"]=0

        if PAD.left: DPAD["x"]-=1
        if PAD.right: DPAD["x"]+=1
        if PAD.up: DPAD["y"]-=1
        if PAD.down: DPAD["y"]+=1
        DPAD["pressed"] = PAD.left or PAD.right or PAD.up or PAD.down
        DPAD["length"] = get_vec2_length(DPAD["x"], DPAD["y"])
        DPAD["length_c"] = get_vec2_length(DPAD["x"], DPAD["y"])
        
        ANALOG["x"] = PAD.analogX
        ANALOG["y"] = PAD.analogY
        ANALOG["length"] = get_vec2_length(PAD.analogX, PAD.analogY)


        if self.BUTTONS_STATE["PRESSED"][NAME] and not PRESSED:
            self.BUTTONS_STATE["PRESSED"][NAME] = False
            self.ON_PAD_RELEASED(NAME, PAD, DPAD, ANALOG)
        if not self.BUTTONS_STATE["PRESSED"][NAME] and PRESSED:
            self.BUTTONS_STATE["PRESSED"][NAME] = True
            self.ON_PAD_PRESSED(NAME, PAD, DPAD, ANALOG)
        
        return True
    def SET_BUTTON_THROTTLING(self, NAME, DELAY=GLOBAL.DEFAULT_BUTTON_THROTTLE):
        self.BUTTONS_STATE["BUTTON_THROTTLE"][NAME] = DELAY
    def IS_BUTTON_THROTTLED(self, NAME):
        DELAY = self.BUTTONS_STATE["BUTTON_THROTTLE"][NAME]
        NOW = time()
        if NOW - self.BUTTONS_STATE["BUTTON_PREV_TIME"][NAME]<DELAY:
            return False
        else:
            self.BUTTONS_STATE["BUTTON_PREV_TIME"][NAME] = NOW
            return True