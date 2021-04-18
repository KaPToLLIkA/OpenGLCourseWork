from global_state import GlobalState
from input_devices import KeyboardEventCallbacks, MouseEventCallbacks
from v_math import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class TexturesIds:
    pass


class Scene:
    def __init__(self, g_state: GlobalState, mouse: MouseEventCallbacks, keyboard: KeyboardEventCallbacks):
        self.state = g_state
        self.mouse = mouse
        self.keyboard = keyboard

    def draw(self):
        self.mouse.process_mouse()
        self.keyboard.process_keys()

        state = self.state
        window = state.window
        camera = state.camera

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 0)

        # projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(camera.field_of_view,
                       float(window.width) / float(window.height),
                       camera.near,
                       camera.far)

        cam_cur_dir = add_vec_3f(camera.position, camera.direction)

        gluLookAt(
            camera.position[0], camera.position[1], camera.position[2],
            cam_cur_dir[0], cam_cur_dir[1], cam_cur_dir[2],
            camera.vertical[0], camera.vertical[1], camera.vertical[2])

        glPushMatrix()

        # model view
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.6, 0.6, 0.6, 1))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0, 0, 0, 1))
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0, 0, 0, 1))

        glutSolidCube(1)

        # projection
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glutSwapBuffers()

    def reshape(self, width, height):
        self.state.window.width = width
        self.state.window.height = height
        glViewport(0, 0, width, height)

    def update(self, value):
        glutPostRedisplay()
        special.glutTimerFunc(33, self.update, 1)
