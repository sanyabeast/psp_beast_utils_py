

import psp2d
import pspos
import pspnet
import pspmp3
import pspogg
from time import time, localtime
import datetime
import stackless

screen = psp2d.Screen()
screen.clear(psp2d.Color(0,0,0,255))

def_font = psp2d.Font('font.png')    

# Creates the Agent base class
class Agent(object):
    def __init__(self):
        self.ch = stackless.channel()       # Communication channel (not used here)
        self.running = True                 # Flag to control the running status
        stackless.tasklet(self.runAction)() # Creates the agent tasklet

    def runAction(self):
        # Here we define the main action, a repetition of the function self.action()
        while self.running:
            # Runs the action
            self.action()
            # Give other tasklets its turn
            stackless.schedule()

    def action(self):
        # In the base class do nothing
        pass


class Renderer(Agent):
    # This is the renderer agent
    def __init__(self):
        Agent.__init__(self)
        self.agents = []

    def exit(self):
        # When the player calls the exit, tell all Agents to stop running
        print "Stopping agents..."
        for agent in self.agents:
            print "Stopped agent %s" % agent
            agent.running = False
        self.running = False
        print "Stopped self..."

    def action(self):
        # Each frame the renderer clears the screen,
        # writes the text and draws each registered agent.
        screen.clear(psp2d.Color(0,0,0,255))
        def_font.drawText(screen, 10, 225, "Move your character with directional")
        def_font.drawText(screen, 10, 240, "Triangle takes screenshot")
        def_font.drawText(screen, 10, 255, "Press X to exit")
        for agent in self.agents:
            screen.blit(agent.sprite, 0, 0, agent.sprite.width,
                        agent.sprite.height, agent.posX, agent.posY, True)
        screen.swap()


class Engine(Agent):
    Controller = psp2d.Controller
    screen = None

    def __init__(self):
        # Set processor and bus speed
        pspos.setclocks(333,166)
        #pspos.setclock(100)
        #pspos.setbus(50)
        self.screen = screen

        print "Localtime: ", localtime()
        print "Datetime: ", datetime.datetime.now()


        # Creates the screen and its background color (Black)
        

    def create_spritesheet(self, urls):
        sprites = []
        for u in urls:
            sprites.append((psp2d.Image(u[0]), psp2d.Image(u[1]))) #Direction = north   = 0
        return sprites
    def load_font(self, url):
        return psp2d.Font('font.png')    



