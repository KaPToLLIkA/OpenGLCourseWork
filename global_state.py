from OpenGL.GL import *


class GlobalState:
    def __init__(self):
        self.mouse = MouseState(self)
        self.keyboard = KeyboardState(self)
        self.camera = CameraState(self)
        self.window = WindowState(self)
        self.scene = SceneState(self)


class MouseState:
    def __init__(self, parent: GlobalState):
        self.sensitivity = 0.25
        self.x = 0
        self.y = 0


class KeyboardState:
    def __init__(self, parent: GlobalState):
        self.keys_press_flags = {i.to_bytes(1, "big"): False for i in range(0, 255)}
        # arrows
        for i in range(100, 104):
            self.keys_press_flags[i] = False
        # F1 - F12
        for i in range(1, 13):
            self.keys_press_flags[i] = False


class CameraState:
    max_pitch = 89.99
    min_pitch = -89.99
    delta_move = 0.6
    delta_yaw = 5
    delta_pitch = 5

    def __init__(self, parent: GlobalState):
        self.position = [0.0, 0.0, 0.0]
        self.direction = [0.0, 0.0, -1.0]
        self.vertical = [0.0, 1.0, 0.0]
        self.yaw = 0.0
        self.pitch = 0.0
        self.field_of_view = 45
        self.near = 0.1
        self.far = 1000


class WindowState:
    def __init__(self, parent: GlobalState):
        self.height = 1000
        self.width = 1000


class SceneState:
    def __init__(self, parent: GlobalState):
        self.lights_enabled_flags = [True for i in range(0, 8)]
        self.lights_ids = [GL_LIGHT0, GL_LIGHT1, GL_LIGHT2, GL_LIGHT3,
                           GL_LIGHT4, GL_LIGHT5, GL_LIGHT6, GL_LIGHT7]
