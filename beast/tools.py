
## created by sanyabeast <a.gvrnsk@gmail.com>
## 05 dec 2020

import simplejson as json
import math

def get_random_string(prefix="uuid", length=16):
    from random import choice
    # return prefix + "".join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length)])
    return prefix + "".join([choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length)])

def random_bool(f=1):
    from random import random
    return random()< 0.5 * (f)
def random_int(a=0, b=100):
    from random import randint
    return randint(a, b)
def random_choice(arr=[]):
    from random import choice
    return choice(arr)
def run_on_thread(cb):
    from threading import Thread
    th = Thread(target=cb)
    return th
def cycle_number(num=0, max=1, direction=1):
    return (num+direction)%max
def parse_json(str_data="{}"):
    return json.loads(str_data)
def stringify_json(data={}):
    return json.dumps(data)
def get_class_tags(cl):
    if cl.__name__ in ["str", "object", "int", "float", "bool"]: return []
    r = [cl.__name__]
    for b in cl.__bases__:
        r += get_class_tags(b)
    return r
def get_vec2_length(x, y):
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2))