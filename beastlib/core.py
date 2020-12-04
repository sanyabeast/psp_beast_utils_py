
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

DEFAULT_BUTTON_THROTTLE = 0.025
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

    def get(self, dict, path, def_value=None):
        return dict[path] if path in dict else def_value

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
    is_pawn = False
    pad_state = {}
    def __init__(self, props):
        Renderable.__init__(self, props)
        now = time()
        self.pad_state = {
            "button_throttle": {"cross":DEFAULT_BUTTON_THROTTLE,"triangle":DEFAULT_BUTTON_THROTTLE,"up":DEFAULT_BUTTON_THROTTLE,"down":DEFAULT_BUTTON_THROTTLE,"left": DEFAULT_BUTTON_THROTTLE,"right":DEFAULT_BUTTON_THROTTLE},
            "prev_time": {"cross":now,"triangle":now,"up":now,"down":now,"left": now,"right":now}
        }
        self.is_pawn = self.get(props, "is_pawn", False)

    def on_tick(self):
        if self.is_pawn:
            pad = GLOBAL["engine"].Controller()
            if   pad.cross:     self.is_button_throttled("cross") and self.on_pad_cross()
            elif pad.triangle:  self.is_button_throttled("triangle") and self.on_pad_triangle()
            elif pad.down:      self.is_button_throttled("down") and self.on_pad_down()
            elif pad.up:        self.is_button_throttled("up") and self.on_pad_up()
            elif pad.left:      self.is_button_throttled("left") and self.on_pad_left()
            elif pad.right:     self.is_button_throttled("right") and self.on_pad_right()
    def on_pad_cross(self): pass
    def on_pad_triangle(self): pass
    def on_pad_down(self): pass
    def on_pad_up(self): pass
    def on_pad_left(self): pass
    def on_pad_right(self): pass
    
    def set_button_throttling(self, name, delay=DEFAULT_BUTTON_THROTTLE):
        self.pad_state["button_throttle"][name] = delay
    def is_button_throttled(self, name):
        delay = self.pad_state["button_throttle"][name]
        now = time()
        if now - self.pad_state["prev_time"][name]<delay:
            return False
        else:
            self.pad_state["prev_time"][name] = now
            return True

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

