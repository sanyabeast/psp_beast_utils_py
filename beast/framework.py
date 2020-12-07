
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
from beast.core import CoreObject, Tickable, GLOBAL, PadButtonsObserver, stringify_json

class Renderer(Tickable):
    def __init__(self, PROPS={}, INIT_PROPS=True):
        Tickable.__init__(self, PROPS, False)
        if INIT_PROPS: self.I(PROPS)
        from beast.actors import Loader
        self.Loader = Loader(PROPS)
        if self.GET(PROPS, "IS_LOADING")==True: self.SET_LOADING(True)

    def ON_TICK(self, DELTA):
        GLOBAL.SCREEN.clear(psp2d.Color(0,0,0,255))
        ACTORS = self.FIND_OBJECTS_OF_TYPE("Actor")
        for a in ACTORS:
            if ACTORS[a].VISIBLE: ACTORS[a].DRAW()
        GLOBAL.SCREEN.swap()
    def DESTROY (self):
        Tickable.DESTROY(self)
    def SET_LOADING(self, SHOW_LOADER=True):
        self.SHOW_LOADER = False
        self.Loader.VISIBLE = False

class Engine(Tickable):
    DEBUG = False
    DebugLog = None
    IS_LOADING = False
    CPU_CLOCK = 333
    MEM_CLOCK = 166
    @property
    def Renderer(self): return self.FIND_T("Renderer")
    @property
    def TaskManager(self): return self.FIND_T("TaskManager")
    def __init__(self, PROPS={}, INIT_PROPS=True):
        Tickable.__init__(self, PROPS, False)
        if INIT_PROPS: self.I(PROPS)
        pspos.setclocks( self.CPU_CLOCK, self.MEM_CLOCK )
        from beast.actors import DebugLog
        if (self.DEBUG): self.DebugLog = DebugLog(PROPS)
    def CREATE_RENDERER(self, PROPS={}):
        return Renderer(PROPS)
    def CREATE_TASK_MANAGER(self, PROPS={}):
        return TaskManager(PROPS)
    def CREATE_SPRITESHEET(self, urls):
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
    def DESTROY(self):
        self.IS_ALIVE = False
        self.DESTROY_ALL()
    def SET_LOADING(self, IS_LOADING=False):
        self.IS_LOADING = IS_LOADING
        self.FIND_T("Loader").VISIBLE = False
        # self.FIND_T("Renderer").SET_LOADING(False)

class Component(Tickable):
    pass

class Actor(Tickable):
    VISIBLE = True
    POSITION_X = 0
    POSITION_Y = 0
    def __init__(self, PROPS, INIT_PROPS=True):
        Tickable.__init__(self, PROPS, False)
        if INIT_PROPS: self.I(PROPS)
        # self.POSITION = Vec2(self.GET(PROPS, "POSITION_X", 0), self.GET(PROPS, "POSITION_Y", 0))
    def DRAW(self):
        pass

class Pawn(Actor):
    def __init__(self, PROPS, INIT_PROPS=True):
        Actor.__init__(self, PROPS, False)
        if INIT_PROPS: self.INIT_PROPS(PROPS)
    def ON_TICK(self, DELTA=1):
        Actor.ON_TICK(self, DELTA)

class TaskManager(Tickable):
    TASKS = []
    TASK_IN_PROGRESS = False
    TICK_INTERVAL = 0.1
    def __init__(self, PROPS={}, INIT_PROPS=True):
        Tickable.__init__(self, PROPS, False)
        if INIT_PROPS: self.I(PROPS)
    def ON_TICK(self, DELTA):
        if (self.TASK_IN_PROGRESS or len(self.TASKS)==0): return
        self.TASK_IN_PROGRESS = True
        TASK = self.TASKS.pop(0)
        self.TASKS = self.TASKS[1:len(self.TASKS)]
        if (TASK!=None):
            self.LOG("task started " + str(len(self.TASKS)))
            TASK(self.FINISH_TASK)
        else: 
            self.TASK_IN_PROGRESS = False
    def FINISH_TASK(self):
        self.LOG("task finished")
        self.TASK_IN_PROGRESS = False
    def ADD_TASK(self, TASK):
        self.TASKS.append(TASK)

class Game(Tickable):
    TICK_INTERVAL = 0.0625
    def __init__(self, PROPS, INIT_PROPS=True):
        Tickable.__init__(self, PROPS, False)
        if INIT_PROPS: self.I(PROPS)

class PlayerController(PadButtonsObserver):
    PAD_BUTTON_OBSERVER_ENABLED = True
    def __init__(self, PROPS, INIT_PROPS=True):
        PadButtonsObserver.__init__(self, PROPS, False)
        if INIT_PROPS: self.INIT_PROPS(PROPS)
    
