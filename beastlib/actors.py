
## created by sanyabeast <a.gvtnsk@gmail.com>
## 05 dec 2020

from beastlib.core import *
from beastlib.tools import cycle_number
from beastlib.framework import Actor

class Loader(Actor):
    tick_interval = 0.5
    letter_index = 0
    def __init__(self, props):
        Actor.__init__(self, props)
        self.letter_index = 0
        
    def on_tick(self, delta):
        self.letter_index = cycle_number(self.letter_index, len("..."), 1)

    def draw(self):

        t = "..."
        l = [char for char in t]  
        l[self.letter_index] = "`"
        t = "".join(l)
        GLOBAL.SCREEN.clear(psp2d.Color(0,0,0,255))
        GLOBAL.DEFAULT_FONT.drawText(GLOBAL.SCREEN, GLOBAL.SCREEN_W/2, GLOBAL.SCREEN_H/2, "LOADING " + t)
        

class DebugLog(Actor):
    lines = []
    max_log = 20
    tick_interval = 2
    creation_times = []
    line_lifetime = 5
    def __init__(self, props):
        Actor.__init__(self, props)
    def draw(self):
        c = 0
        for t in self.lines:
            GLOBAL.DEFAULT_FONT.drawText(GLOBAL.SCREEN, 10, c*10, t)
            c+=1

    def on_tick(self, delta):
        now = time()
        for index, l in enumerate(self.lines):
            if now - self.creation_times[index]:
                self.lines.pop(index)
                self.creation_times.pop(index)
                break
    def add_line(self, t):
        self.lines.append(t)
        self.creation_times.append(time())
        lines_len = len(self.lines)
        creation_times_len = len(self.creation_times)
        self.lines = self.lines[max(0, lines_len-self.max_log):lines_len]
        self.creation_times = self.creation_times[max(0, creation_times_len-self.max_log):creation_times_len]


