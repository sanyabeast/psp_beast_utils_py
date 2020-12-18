# -*- coding: iso-8859-1 -*-


from beast.core import GLOBAL, Launcher
from beast.tools import random_bool, random_choice, random_int
from beast.framework import Engine, Pawn, Actor, Tickable, TaskManager, Game, PlayerController
from time import time
import stackless
import math

launcher = Launcher()
# App = launcher.create_app("knights")
App = launcher.create_app("knights_ii")
app = App({
    "TICK_INTERVAL": 1
})
print(app)

# game = DungeonGame({
#     "TICK_INTERVAL": 1
# })

engine = Engine({
    "DEBUG": True,
    "IS_LOADING": True,
    "CREATE_RENDERER": True,
    "CREATE_TASK_MANAGER": True
})
stackless.run()