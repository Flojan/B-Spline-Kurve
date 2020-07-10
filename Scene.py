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

    def __init__(self):
        self.points = []
        self.curvePoints = []
        self.curve = []
        self.modPoints = []
        self.lastPos = (0, 0)
        self.pointsWeight = []
        self.onPoint = False
        self.firstDraw = False
        self.idxPoint = 0
        self.weight = 1
        self.pointSize = 8
        self.m = 8  # Kurvenpunkte
        self.k = 5  # Ordnung

    def addPoint(self, posX, posY):
        self.pointsWeight.append([posX, posY, 1, self.weight])
        self.drawCurve()

    def getPoint(self, posX, posY):
        self.idxPoint = 0
        puffer = 0.01
        for point in self.points:
            if ((posX and point[0]) != 0) and ((posY and point[1]) != 0):
                xPointHitboxDown, xPointHitboxUp, yPointHitboxDown, yPointHitboxUp = abs(
                    point[0]) - puffer, abs(point[0]) + puffer, abs(point[1]) - puffer, abs(point[1]) + puffer
                if abs(posX) > xPointHitboxDown and abs(posX) < xPointHitboxUp and abs(posY) > yPointHitboxDown and abs(posY) < yPointHitboxUp:
                    self.onPoint = True
                    self.lastPos = (posX, posY)
                    return
            self.idxPoint += 1

    def drawPolygon(self):
        polyvbo = vbo.VBO(np.array(self.points, 'f'))
        polyvbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnable(GL_POINT_SMOOTH)
        glVertexPointer(2, GL_FLOAT, 0, polyvbo)
        glColor(1.0, 1.0, 1.0, 1.0)
        glLineWidth(2)
        glPointSize(self.pointSize)
        glDrawArrays(GL_POINTS, 0, len(self.points))
        if len(self.points) > 1:
            glDrawArrays(GL_LINE_STRIP, 0, len(self.points))
        self.drawCurvePoints()
        glDisableClientState(GL_VERTEX_ARRAY)
        polyvbo.unbind()

    def drawCurvePoints(self):
        if len(self.curvePoints) > 1:
            curvevbo = vbo.VBO(np.array(self.curvePoints, 'f'))
            curvevbo.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2, GL_FLOAT, 0, curvevbo)
            glLineWidth(5)
            glColor(0.05, 0.6, 1.0, 1.0)
            glEnable(GL_POINT_SMOOTH)

            glDrawArrays(GL_LINE_STRIP, 0, len(curvevbo))
            glDisableClientState(GL_VERTEX_ARRAY)
            curvevbo.unbind()

    def deBoor(self, ordnung, controlpoints, knotvector, t, idxOrdnung, r):
        if idxOrdnung == 0:
            return controlpoints[r]

        if (knotvector[r - idxOrdnung + ordnung] - knotvector[r]) == 0:
            alpha = 0
        else:
            alpha = (t - knotvector[r]) / (knotvector[r -
                                                      idxOrdnung + ordnung] - knotvector[r])

        p1 = [(1 - alpha) * b for b in self.deBoor(ordnung,
                                                   controlpoints, knotvector, t, idxOrdnung - 1, r - 1)]
        p2 = [
            alpha * b for b in self.deBoor(ordnung, controlpoints, knotvector, t, idxOrdnung - 1, r)]
        return [x[0] + x[1] for x in zip(p1, p2)]

    def drawCurve(self):
        self.modPoints.clear()
        [self.modPoints.append((pw[0] * pw[3], pw[1] * pw[3], pw[2] * pw[3]))
         for pw in self.pointsWeight]
        self.points.clear()
        [self.points.append((x/w, y/w)) for x, y, w in self.modPoints]

        if self.m == 0:
            self.m += 1
        if self.k == 0:
            self.k += 1
        if len(self.points) == self.k:
            self.firstDraw = True
            print("erste Kurve gezeichnet")
        n = len(self.points) - 1
        k = self.getKnotvector(self.k, n)
        if not k:
            self.curve.clear()
            return
        self.curve = []
        for i in range(self.m + 1):
            t = max(k) * (i / self.m)
            r = None
            for j in range(len(k)):
                if t == max(k):
                    r = len(k) - self.k - 1
                    break
                if k[j] <= t < k[j+1]:
                    r = j
                    break
            self.curve.append(self.deBoor(
                self.k, self.modPoints, k, t, self.k-1, r))
        self.curvePoints.clear()
        [self.curvePoints.append((x/w, y/w)) for x, y, w in self.curve]

    def getKnotvector(self, ordnung, n):
        if len(self.points) < ordnung:
            if self.firstDraw:
                self.k -= 1
                print("Ordnung größer als Points")
            return
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
