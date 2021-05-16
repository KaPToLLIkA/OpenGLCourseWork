from PIL import Image

from OPEN_GL_state import OPEN_GL_state
from global_state import GlobalState
from input_devices import KeyboardEventCallbacks, MouseEventCallbacks
from v_math import *
from scene_parts import Drawable

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class TexturesIds:
    _woodBase = 10
    wood = [1, 2]

    _roofBase = 20
    roof = [1]

    _grassBase = 30
    grass = [1]

    _bushBase = 100
    bush = [1, 2, 3, 4]

    _lightBase = 200
    light = 1

    @staticmethod
    def prepare_textures_ids():
        TexturesIds.wood = list(map(lambda el: el + TexturesIds._woodBase, TexturesIds.wood))
        TexturesIds.roof = list(map(lambda el: el + TexturesIds._roofBase, TexturesIds.roof))
        TexturesIds.grass = list(map(lambda el: el + TexturesIds._grassBase, TexturesIds.grass))
        TexturesIds.bush = list(map(lambda el: el + TexturesIds._bushBase, TexturesIds.bush))
        TexturesIds.light += TexturesIds._lightBase

    @staticmethod
    def load_all_textures():
        TexturesIds.prepare_textures_ids()
        loader = TexturesIds.load_texture

        # load all wood textures
        glBindTexture(GL_TEXTURE_2D, TexturesIds.wood[0])
        loader('./res/tex/wood/side.png')
        glBindTexture(GL_TEXTURE_2D, TexturesIds.wood[1])
        loader('./res/tex/wood/top_bottom.png')
        glBindTexture(GL_TEXTURE_2D, TexturesIds.light)
        loader('./res/tex/light/light_box.png')
        #
        # # load all roof textures
        # for _id in TexturesIds.roof:
        #     glBindTexture(GL_TEXTURE_2D, _id)
        #     loader('./res/tex/roof/' + str(_id - TexturesIds._roofBase) + '.png')
        #
        # load all grass textures
        for _id in TexturesIds.grass:
            glBindTexture(GL_TEXTURE_2D, _id)
            loader('./res/tex/grass/' + str(_id - TexturesIds._grassBase) + '.png')

        # load all bush textures
        for _id in TexturesIds.bush:
            glBindTexture(GL_TEXTURE_2D, _id)
            loader('./res/tex/bush/' + str(_id - TexturesIds._bushBase) + '.png')

    @staticmethod
    def load_texture(file):
        image = Image.open(file)
        pixels = image.load()
        width, height = image.size

        all_pixels = []
        for x in range(width):
            for y in range(height):
                all_pixels.append(pixels[x, height - y - 1])

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, height, width, 0, GL_RGBA, GL_UNSIGNED_BYTE, all_pixels)
        glEnable(GL_TEXTURE_GEN_S)
        glEnable(GL_TEXTURE_GEN_T)
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)


class Scene:
    def __init__(self, g_state: GlobalState, mouse: MouseEventCallbacks, keyboard: KeyboardEventCallbacks):
        self.state = g_state
        self.mouse = mouse
        self.keyboard = keyboard
        self.objects = list()

    def add_drawable_object(self, new_object: Drawable):
        self.objects.append(new_object)

    def draw(self):
        self.mouse.process_mouse()
        self.keyboard.process_keys()

        state = self.state
        window = state.window
        camera = state.camera

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(149 / 255, 200 / 255, 216 / 255, 0)

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

        glLightfv(GL_LIGHT1, GL_POSITION, (camera.position[0], camera.position[1], camera.position[2], 1.0))

        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.6, 0.6, 0.6, 1))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0, 0, 0, 1))
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0, 0, 0, 1))

        print(OPEN_GL_state.enable_textures)
        if OPEN_GL_state.enable_textures:
            glEnable(GL_TEXTURE_2D)
            glEnable(GL_TEXTURE_GEN_S)
            glEnable(GL_TEXTURE_GEN_T)
        else:
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_TEXTURE_GEN_S)
            glDisable(GL_TEXTURE_GEN_T)
        # center

        for drawable_object in self.objects:
            drawable_object.draw()

        if OPEN_GL_state.enable_textures:
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_TEXTURE_GEN_T)
            glDisable(GL_TEXTURE_GEN_S)
        else:
            glEnable(GL_TEXTURE_2D)
            glEnable(GL_TEXTURE_GEN_T)
            glEnable(GL_TEXTURE_GEN_S)
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
