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
        self.aspectwidth = float(self.width) / self.height
        self.aspectheight = float(self.height) / self.width
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
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glMatrixMode(GL_MODELVIEW)

        # glLoadIdentity()

        # set window callbacks
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_cursor_pos_callback(self.window, self.onMouseMove)
        glfw.set_key_callback(self.window, self.onKeyboard)

        # create 3D
        self.scene = Scene(self.width, self.height)
        self.mousePos = (0, 0)

        # exit flag
        self.exitNow = False

        # mouse
        self.leftMouseClicked = False

    def onMouseButton(self, win, button, action, mods):
        r = min(self.width, self.height) / 2.0
        print("mouse button: ", win, button, action, mods)

        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                self.leftMouseClicked = True
            elif action == glfw.RELEASE:
                # Scene..
                self.leftMouseClicked = False

    def onMouseMove(self, win, posX, posY):
        x = posX
        y = posY
        self.mousePos = (x, y)

    def onKeyboard(self, win, key, scancode, action, mods):
        print("keyboard: ", win, key, scancode, action, mods)
        if action == glfw.PRESS:
            # ESC to quit
            if key == glfw.KEY_ESCAPE:
                self.exitNow = True

            # Ordnung der Kurve
            if key == glfw.KEY_K:
                return

            # Anzahl zu berechnender Kurvenpunkte
            if key == glfw.KEY_M:
                return

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
