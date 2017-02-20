import numpy as np
import math

def j(j0, j1):
    return np.array([[j0], [j1]])

def qwp(theta):
    return math.exp**(j*math.pi/4)*np.matrix([[math.cos(theta)**2 + j*math.sin(theta)**2, (1-j)*math.cos(theta)*math.sin(theta) ],
    [(1-j)*math.cos(theta)*math.sin(theta), math.sin(theta)**2 + j*math.cos(theta)**2]])

def hwp(theta):
    return np.matrix([[math.cos(2*theta), math.sin(2*theta)],
    [math.sin(2*theta), -math.cos(2*theta)]])
