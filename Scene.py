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
        self.polyvbo = []
        self.curvePoints = []
        self.curvevbo = []
        self.pointSize = 3
        self.m = 3  # Kurvenpunkte
        self.k = 5  # Ordnung

    def addPoint(self, posX, posY):
        self.points.append((posX, posY))
        self.drawCurve()

    def delPoint(self):
        self.points = []

    def drawPolygon(self):
        polyvbo = vbo.VBO(np.array(self.points, 'f'))
        polyvbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnable(GL_POINT_SMOOTH)
        glVertexPointer(2, GL_FLOAT, 0, polyvbo)
        glColor3fv([0, 0, 0])
        glPointSize(self.pointSize)
        glDrawArrays(GL_POINTS, 0, len(self.points))
        # Lines
        if len(self.points) > 1:
            glDrawArrays(GL_LINE_STRIP, 0, len(self.points))
        self.drawCurvePoints()
        glDisableClientState(GL_VERTEX_ARRAY)
        polyvbo.unbind()

    def drawCurvePoints(self):
        if len(self.curvePoints) > 1:
            self.curvevbo = vbo.VBO(np.array(self.curvePoints, 'f'))
            self.curvevbo.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2, GL_FLOAT, 0, self.curvevbo)
            glColor3fv([1, 0, 0])
            glLineWidth(2)
            glDrawArrays(GL_LINE_STRIP, 0, len(self.curvevbo))
            glDisableClientState(GL_VERTEX_ARRAY)
            self.curvevbo.unbind()

    def deBoor(self, ordnung, controlpoints, knotvector, t, idxOrdnung, r):
        if idxOrdnung == 0:
            '''if r == len(controlpoints):
                return controlpoints[r - 1]'''
            return controlpoints[r]

        if (knotvector[r - idxOrdnung + ordnung] - knotvector[r]) == 0:
            alpha = 0
        else:
            alpha = (t - knotvector[r]) / (knotvector[r -
                                                      idxOrdnung + ordnung] - knotvector[r])

        p1 = [(1 - alpha) * b for b in self.deBoor(ordnung,
                                                   controlpoints, knotvector, t, idxOrdnung - 1, r - 1)]
        p2 = [alpha * b for b in self.deBoor(ordnung,
                                             controlpoints, knotvector, t, idxOrdnung - 1, r)]
        return [x[0] + x[1] for x in zip(p1, p2)]

    def drawCurve(self):
        if self.m == 0:
            self.m += 1
            print("keine Kurvenpunkte")
        n = len(self.points)-1
        k = self.getKnotvector(self.k, n)
        print(self.m, "Kurvenpunkte")
        print(self.k, "Ordnung")
        if not k:
            self.curvePoints.clear()
            return
        self.curvePoints = []
        for i in range(self.m+1):
            t = max(k)*(i/self.m)
            r = None
            for j in range(len(k)):
                if t == max(k):
                    r = len(k)-self.k-1
                    break
                if k[j] <= t < k[j+1]:
                    r = j
                    break
            self.curvePoints.append(self.deBoor(
                self.k, self.points, k, t, self.k-1, r))

    def getKnotvector(self, ordnung, n):
        if len(self.points) - 1 < ordnung - 1:
            print("Punktanzahl kleiner als Ordnung")
            return None
        knoten = [0.0] * ordnung
        knoten += [float(i)
                   for i in range(1, (n - (ordnung - 1)) + 1)]
        knoten += [float((n - (ordnung - 2)))] * ordnung
        return knoten

    # render
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.drawPolygon()
        glFlush()
