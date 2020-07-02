import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

import numpy as np
import math


class Scene:
    """ OpenGL 2D scene class """
    # initialization

    def __init__(self, width, height):
        self.points = []
        self.myvbo = []

    def deBoor(self, degree, controlpoints, knotvector, t):
        return

    # render
    def render(self):
        return
