import numpy as np
import random

def random_rgb():
    c1 = hex(random.randint(0,255))[2:]
    c2 = hex(random.randint(0,255))[2:]
    c3 = hex(random.randint(0,255))[2:]
    ret = "#" + c1 + c2 + c3
    return ret