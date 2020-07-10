import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

import numpy as np
import math

from Scene import Scene


class B_Spline_Kurve:
    """GLFW Rendering window class"""

    def __init__(self):

        # save current working directory
        cwd = os.getcwd()

        # Initialize the library
        if not glfw.init():
            return

        # restore cwd
        os.chdir(cwd)

        # buffer hints
        glfw.window_hint(glfw.DEPTH_BITS, 32)

        # define desired frame rate
        self.frame_rate = 100

        # make a window
        self.width, self.height = 640, 480
        self.aspectwidth = float(self.width) / float(self.height)
        self.window = glfw.create_window(
            self.width, self.height, "2D Graphics", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glMatrixMode(GL_MODELVIEW)

        # set window callbacks
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_cursor_pos_callback(self.window, self.onMouseMove)
        glfw.set_key_callback(self.window, self.onKeyboard)

        # create 3D
        self.scene = Scene()

        # exit flag
        self.exitNow = False

        # mouse
        self.leftMouseClicked = False
        self.mousePos = (0, 0)

    def onMouseButton(self, win, button, action, mods):
        # print("mouse button: ", win, button, action, mods)

        if button == glfw.MOUSE_BUTTON_LEFT and not mods == glfw.MOD_SHIFT:
            if action == glfw.RELEASE:
                print("Punkt gesetzt")
                self.scene.addPoint(self.mousePos[0], self.mousePos[1])

        if button == glfw.MOUSE_BUTTON_LEFT and mods == glfw.MOD_SHIFT:
            if action == glfw.PRESS:
                self.leftMouseClicked = True
            elif action == glfw.RELEASE:
                self.leftMouseClicked = False
                self.scene.onPoint = False

    def onMouseMove(self, win, posX, posY):
        x = posX / self.width * 2 - 1
        y = (posY / self.height * 2 - 1) * (-1)
        self.mousePos = (x, y)
        if(self.leftMouseClicked):
            if self.scene.onPoint:
                if self.scene.lastPos[1] > self.mousePos[1]:
                    actWeight = self.scene.pointsWeight[self.scene.idxPoint]
                    oldWeight = actWeight[3]
                    if oldWeight > 1:
                        newWeight = oldWeight - 0.25
                        actWeight[3] = newWeight
                else:
                    actWeight = self.scene.pointsWeight[self.scene.idxPoint]
                    oldWeight = actWeight[3]
                    if oldWeight < 10:
                        newWeight = oldWeight + 0.25
                        actWeight[3] = newWeight
                self.scene.pointsWeight[self.scene.idxPoint] = actWeight
                self.scene.lastPos = self.mousePos
                self.scene.drawCurve()
            else:
                self.scene.getPoint(self.mousePos[0], self.mousePos[1])

    def onKeyboard(self, win, key, scancode, action, mods):
        # print("keyboard: ", win, key, scancode, action, mods)
        if action == glfw.PRESS:
            # ESC to quit
            if key == glfw.KEY_ESCAPE:
                self.exitNow = True

           # Ordnung der Kurve verringern
            if key == glfw.KEY_K and not mods == glfw.MOD_SHIFT:
                print("[k]:", self.scene.k, "Ordnung")
                self.scene.k -= 1
                self.scene.drawCurve()

             # Ordnung der Kurve erhöhen
            if key == glfw.KEY_K and mods == glfw.MOD_SHIFT:
                print("[K]:", self.scene.k, "Ordnung")
                self.scene.k += 1
                self.scene.drawCurve()

            # Anzahl zu berechnender Kurvenpunkte verringern
            if key == glfw.KEY_M and not mods == glfw.MOD_SHIFT:
                print("[m]:", self.scene.m, "Kurvenpunkte")
                self.scene.m -= 1
                self.scene.drawCurve()

            # Anzahl zu berechnender Kurvenpunkte erhöhen
            if key == glfw.KEY_M and mods == glfw.MOD_SHIFT:
                print("[M]:", self.scene.m, "Kurvenpunkte")
                self.scene.m += 1
                self.scene.drawCurve()

    def run(self):
        # initializer timer
        glfw.set_time(0.0)
        t = 0.0

        while not glfw.window_should_close(self.window) and not self.exitNow:
            # update every x seconds
            currT = glfw.get_time()
            if currT - t > 1.0/self.frame_rate:
                # update time
                t = currT
                # clear
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                # render scene
                self.scene.render()

                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()
        # end
        glfw.terminate()


# main() function
def main():
    print("Simple glfw render Window")
    rw = B_Spline_Kurve()
    rw.run()


# call main
if __name__ == '__main__':
    main()
