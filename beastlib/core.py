

import psp2d
import pspos
import pspnet
import pspmp3
import pspogg
from time import time, localtime
import datetime
import stackless
import sys

SCREEN_W = 480
SCREEN_H = 272
GLOBAL = {
    "logger": None,
    "engine": None,
    "rend": None
}

screen = psp2d.Screen()
screen.clear(psp2d.Color(0,0,0,255))

def_font = psp2d.Font('font.png')    

class CoreObject(object):
    TAG = "object"
    alive = False
    def __init__(self, props={}):
        self.children = {}
        self.alive = True

    def get(self, dict, path):
        return dict[path] if path in dict else None

    def die(self):
        self.alive = False
        for k in self.children: k.die()

    def add_child(self, child_id, child):
        self.children[child_id]=child

    def log(self, data="..."):
        t = "%s: %s" % (self.TAG, str(data))
        print(t)
        if GLOBAL["logger"]!=None: 
            GLOBAL["logger"].add_line(t)

class Tickable(CoreObject):
    TAG = "agent"
    def __init__(self, props={}):
        CoreObject.__init__(self, props)
        self.ch = stackless.channel()       # Communication channel (not used here)
        stackless.tasklet(self.tick)() # Creates the agent tasklet
        self.log("created")

    def tick(self):
        while self.alive:
            self.on_tick()
            stackless.schedule()
    def on_tick(self):
        pass

class Renderer(Tickable):
    TAG = "renderer"
    def __init__(self, props={}):
        Tickable.__init__(self, props)
        self.renderables = []
        GLOBAL["rend"] = self

    def on_tick(self):
        screen.clear(psp2d.Color(0,0,0,255))
        # def_font.drawText(screen, 10, 225, "Move your character with directional")
        # def_font.drawText(screen, 10, 240, "Triangle takes screenshot")
        # def_font.drawText(screen, 10, 255, "Press X to exit")
        for renderable in self.renderables:
            renderable.draw(screen)
        screen.swap()

    def die (self):
        # When the player calls the exit, tell all renderables to stop alive
        for renderable in self.renderables:
            # print "Stopped renderable %s" % renderable
            renderable.alive = False
        CoreObject.die(self)

class Engine(Tickable):
    TAG = "engine"
    Controller = psp2d.Controller
    screen = None
    debug = False
    rend = None

    def __init__(self, props={}):
        Tickable.__init__(self, props)
        GLOBAL["engine"] = self
        
        pspos.setclocks(333,166)
        #pspos.setclock(100)
        #pspos.setbus(50)
        self.screen = screen
        self.rend = Renderer({})

        print "Localtime: ", localtime()
        print "Datetime: ", datetime.datetime.now()

        self.debug = self.get(props, "debug")
        if (self.debug):
            GLOBAL["logger"] = DebugLog({
                "rend": self.rend
            })

        self.log("created")

    def create_spritesheet(self, urls):
        sprites = []
        for u in urls:
            sprites.append((psp2d.Image(u[0]), psp2d.Image(u[1]))) #Direction = north   = 0
        return sprites
    def load_font(self, url):
        return psp2d.Font('font.png')   
    def die(self):
        print("die")
        CoreObject.die(self)
        

class Renderable(Tickable):
    TAG = "renderable"
    def __init__(self, props):
        Tickable.__init__(self, props)
        self.rend = props["rend"]   
        self.rend.renderables.append(self) # Adds this agent to the renderer
        self.posX = 0
        self.posY = 0

    def draw(self, screen):
        pass

class Actor(Renderable):
    TAG = "actor"
    def __init__(self, props):
        Renderable.__init__(self, props)

    def on_tick(self):
        pass

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
        self.lines = self.lines[lines_len-self.max_log:lines_len]

