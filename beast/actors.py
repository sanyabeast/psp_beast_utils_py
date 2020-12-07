
## created by sanyabeast <a.gvtnsk@gmail.com>
## 05 dec 2020

from beast.core import *
from beast.tools import cycle_number
from beast.framework import Actor

class Loader(Actor):
    TICK_INTERVAL = 0.5
    anim_letter_index = 0
    def __init__(self, PROPS, INIT_PROPS=True):
        Actor.__init__(self, PROPS, False)
        if self.INIT_PROPS: self.INIT_PROPS(PROPS)
        self.anim_letter_index = 0
    
    def ON_TICK(self, delta):
        self.anim_letter_index = cycle_number(self.anim_letter_index, len("..."), 1)
    def DRAW(self):
        t = "..."
        l = [char for char in t]  
        l[self.anim_letter_index] = "`"
        t = "".join(l)
        GLOBAL.SCREEN.clear(psp2d.Color(0,0,0,255))
        GLOBAL.DEFAULT_FONT.drawText(GLOBAL.SCREEN, GLOBAL.SCREEN_W/2, GLOBAL.SCREEN_H/2, "LOADING " + t)
        

class DebugLog(Actor):
    TICK_INTERVAL = 2
    lines = []
    history_length = 20
    creation_dates = []
    line_lifetime = 5
    def __init__(self, PROPS, INIT_PROPS=True):
        Actor.__init__(self, PROPS, False)
        if self.INIT_PROPS: self.INIT_PROPS(PROPS)
    def DRAW(self):
        c = 0
        for t in self.lines:
            GLOBAL.DEFAULT_FONT.drawText(GLOBAL.SCREEN, 10, c*10, t)
            c+=1
    def ON_TICK(self, delta):
        now = time()
        for index, l in enumerate(self.lines):
            if now - self.creation_dates[index]:
                self.lines.pop(index)
                self.creation_dates.pop(index)
                break
    def add_line(self, t):
        self.lines.append(t)
        self.creation_dates.append(time())
        lines_len = len(self.lines)
        creation_dates_len = len(self.creation_dates)
        self.lines = self.lines[max(0, lines_len-self.history_length):lines_len]
        self.creation_dates = self.creation_dates[max(0, creation_dates_len-self.history_length):creation_dates_len]


