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
        self.pointSize = 3
        self.myvbo = []

    def addPoint(self, posX, posY):
        self.points.append((posX, posY))

    def delPoint(self):
        self.points = []

    def drawPoint(self):
        myvbo = vbo.VBO(np.array(self.points, 'f'))
        myvbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnable(GL_POINT_SMOOTH)
        glVertexPointer(2, GL_FLOAT, 0, myvbo)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor3fv([0, 0, 0])
        glPointSize(self.pointSize)
        glDrawArrays(GL_POINTS, 0, len(self.points))
        self.drawLine()
        glDisableClientState(GL_VERTEX_ARRAY)
        myvbo.unbind()

    def drawLine(self):
        if(len(self.points) > 1):
            glDrawArrays(GL_LINE_STRIP, 0, len(self.points))

    def deBoor(self, degree, controlpoints, knotvector, t):
        return

    # render
    def render(self):
        self.drawPoint()
