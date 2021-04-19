from global_state import GlobalState
from v_math import *

from OpenGL._bytes import as_8_bit
from OpenGL.GLUT import *


class KeyboardEventCallbacks:
    def __init__(self, g_state: GlobalState):
        self.state = g_state

    def keyboard_func(self, key, x, y):
        self.state.keyboard.keys_press_flags[key] = True

    def keyboard_up_func(self, key, x, y):
        self.state.keyboard.keys_press_flags[key] = False

    def special_func(self, key, x, y):
        self.state.keyboard.keys_press_flags[key] = True

    def special_up_func(self, key, x, y):
        self.state.keyboard.keys_press_flags[key] = False

    def process_keys(self):
        x = 0
        y = 1
        z = 2

        keyboard = self.state.keyboard

        w_pressed = keyboard.keys_press_flags[as_8_bit('w')] or keyboard.keys_press_flags[as_8_bit('W')]
        a_pressed = keyboard.keys_press_flags[as_8_bit('a')] or keyboard.keys_press_flags[as_8_bit('A')]
        s_pressed = keyboard.keys_press_flags[as_8_bit('s')] or keyboard.keys_press_flags[as_8_bit('S')]
        d_pressed = keyboard.keys_press_flags[as_8_bit('d')] or keyboard.keys_press_flags[as_8_bit('D')]

        r_pressed = keyboard.keys_press_flags[as_8_bit('r')] or keyboard.keys_press_flags[as_8_bit('R')]
        f_pressed = keyboard.keys_press_flags[as_8_bit('f')] or keyboard.keys_press_flags[as_8_bit('F')]

        right_pressed = keyboard.keys_press_flags[102]
        left__pressed = keyboard.keys_press_flags[100]
        up____pressed = keyboard.keys_press_flags[101]
        down__pressed = keyboard.keys_press_flags[103]

        camera = self.state.camera

        vec = [
            cos(radians(camera.yaw)) * cos(radians(camera.pitch)),
            sin(radians(camera.pitch)),
            sin(radians(camera.yaw)) * cos(radians(camera.pitch))
        ]

        camera.direction = normalize_vec3f(vec)

        if w_pressed:
            camera.position = add_vec_3f(camera.position,
                                         mul_vec_3f(
                                             camera.direction,
                                             camera.delta_move
                                         ))
        if s_pressed:
            camera.position = sub_vec_3f(camera.position,
                                         mul_vec_3f(
                                             camera.direction,
                                             camera.delta_move
                                         ))

        if a_pressed:
            camera.position = sub_vec_3f(camera.position,
                                         mul_vec_3f(
                                             normalize_vec3f(
                                                 cross_vec3f(
                                                     camera.direction,
                                                     camera.vertical
                                                 )
                                             ),
                                             camera.delta_move
                                         ))

        if d_pressed:
            camera.position = add_vec_3f(camera.position,
                                         mul_vec_3f(
                                             normalize_vec3f(
                                                 cross_vec3f(
                                                     camera.direction,
                                                     camera.vertical
                                                 )
                                             ),
                                             camera.delta_move
                                         ))

        if r_pressed:
            camera.position[y] += camera.delta_move

        if f_pressed:
            camera.position[y] -= camera.delta_move

        if left__pressed:
            camera.yaw -= camera.delta_yaw

        if right_pressed:
            camera.yaw += camera.delta_yaw

        if up____pressed:
            camera.pitch += camera.delta_pitch

        if down__pressed:
            camera.pitch -= camera.delta_pitch

        if camera.pitch > camera.max_pitch:
            camera.pitch = camera.max_pitch

        if camera.pitch < camera.min_pitch:
            camera.pitch = camera.min_pitch


class MouseEventCallbacks:
    def __init__(self, g_state: GlobalState):
        self.state = g_state
        self.old_x = g_state.mouse.x
        self.old_y = g_state.mouse.y
        self.delta_x = 0
        self.delta_y = 0
        self.enabled_motion = False

    def passive_motion_func(self, x, y):
        self.old_x = self.state.mouse.x
        self.old_y = self.state.mouse.y
        self.state.mouse.x = x
        self.state.mouse.y = y
        self.delta_x = self.old_x - x
        self.delta_y = self.old_y - y

    def motion_func(self, x, y):
        self.passive_motion_func(x, y)

    def mouse_func(self, key, state, x, y):
        if key == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.enabled_motion = True
            else:
                self.enabled_motion = False

    def process_mouse(self):
        if self.enabled_motion:
            mouse = self.state.mouse
            camera = self.state.camera

            self.delta_x *= mouse.sensitivity
            self.delta_y *= mouse.sensitivity

            camera.yaw += self.delta_x
            camera.pitch -= self.delta_y

            self.delta_x, self.delta_y = 0, 0

            if camera.pitch > camera.max_pitch:
                camera.pitch = camera.max_pitch

            if camera.pitch < camera.min_pitch:
                camera.pitch = camera.min_pitch

            vec = [
                cos(radians(camera.yaw)) * cos(radians(camera.pitch)),
                sin(radians(camera.pitch)),
                sin(radians(camera.yaw)) * cos(radians(camera.pitch))
            ]

            camera.direction = normalize_vec3f(vec)
