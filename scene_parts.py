from math import *

from OpenGL.GL import *
from OpenGL.GLUT import *


class Drawable:
    def __init__(self):
        pass

    def draw(self):
        pass


class Line(Drawable):
    def __init__(self, color: dict, start_p: dict, end_p: dict):
        super().__init__()
        self.end_p = end_p
        self.start_p = start_p
        self.color = color

    def draw(self):
        glPushMatrix()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glColor3f(self.color['r'], self.color['g'], self.color['b'])
        glVertex3f(self.start_p['x'], self.start_p['y'], self.start_p['z'])
        glVertex3f(self.end_p['x'], self.end_p['y'], self.end_p['z'])
        glEnd()
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
        glPopMatrix()


class Axes(Drawable):
    def __init__(self, length, position=None, rotate=None):
        super().__init__()
        self.length = length

        if position is None:
            position = dict(x=0, y=0, z=0)
        self.position = position

        if rotate is None:
            rotate = dict(x=0, y=0, z=0)
        self.rotate = rotate

        self.objects = list()

        self.objects.append(
            Line(color=dict(r=1, g=0, b=0),
                 start_p=dict(x=0, y=0, z=0),
                 end_p=dict(x=self.length, y=0, z=0)
                 )
        )

        self.objects.append(
            Line(color=dict(r=0, g=1, b=0),
                 start_p=dict(x=0, y=0, z=0),
                 end_p=dict(x=0, y=self.length, z=0)
                 )
        )

        self.objects.append(
            Line(color=dict(r=0, g=0, b=1),
                 start_p=dict(x=0, y=0, z=0),
                 end_p=dict(x=0, y=0, z=self.length)
                 )
        )

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate['x'], 1, 0, 0)
        glRotatef(self.rotate['y'], 0, 1, 0)
        glRotatef(self.rotate['z'], 0, 0, 1)

        for obj in self.objects:
            obj.draw()

        glPopMatrix()


class StaticBush(Drawable):
    def __init__(self, t_id, width, height, position=None, rotate_angle=0):
        super().__init__()
        if position is None:
            position = dict(x=0, y=0, z=0)
        self.rotate_angle = rotate_angle
        self.width = width
        self.height = height
        self.position = position
        self.t = t_id

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate_angle, 0, 1, 0)
        glTranslatef(-self.width / 2, 0, -self.width / 2)
        draw_model(self.width, self.height, self.t)
        glPopMatrix()


class Grass(Drawable):
    def __init__(self, t_side_id, size=None, position=None, rotate=None):
        super().__init__()
        if size is None:
            size = dict(x=0, y=0, z=0)

        if position is None:
            position = dict(x=0, y=0, z=0)

        if rotate is None:
            rotate = dict(x=0, y=0, z=0)

        self.size = size
        self.position = position
        self.rotate = rotate
        self.t_side_id = t_side_id

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate['x'], 1, 0, 0)
        glRotatef(self.rotate['y'], 0, 1, 0)
        glRotatef(self.rotate['z'], 0, 0, 1)

        glTranslatef(-self.size['x'] / 2, -self.size['y'] / 2, -self.size['z'] / 2)
        draw_rect_single_texture(self.size['x'], self.size['y'], self.size['z'], self.t_side_id)

        # glDisable(self.l_id)
        glPopMatrix()


class Lamp(Drawable):
    def __init__(self, t_side_id, size, position, rotate, index):
        super().__init__()
        self.rotate = rotate
        self.position = position
        self.t_side_id = t_side_id
        self.size = size
        if 0 < index < 8:
            if index == 1:
                self.l_id = GL_LIGHT1
            if index == 2:
                self.l_id = GL_LIGHT2
            if index == 3:
                self.l_id = GL_LIGHT3
            if index == 4:
                self.l_id = GL_LIGHT4
            if index == 5:
                self.l_id = GL_LIGHT5
            if index == 6:
                self.l_id = GL_LIGHT6
            if index == 7:
                self.l_id = GL_LIGHT7

        glLightfv(self.l_id, GL_DIFFUSE, (255 / 256, 213 / 256, 0 / 256, 1))
        glLightfv(self.l_id, GL_SPECULAR, (255 / 256 * 0.4, 213 / 256 * 0.4, 0 / 256 * 0.4, 1))
        glLightfv(self.l_id, GL_AMBIENT, (255 / 256 * 0.8, 213 / 256 * 0.8, 0 / 256 * 0.8, 1))
        glLightf(self.l_id, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(self.l_id, GL_LINEAR_ATTENUATION, 0.0014)
        glLightf(self.l_id, GL_QUADRATIC_ATTENUATION, 0.000007)

        self.objects = list()

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate['x'], 1, 0, 0)
        glRotatef(self.rotate['y'], 0, 1, 0)
        glRotatef(self.rotate['z'], 0, 0, 1)

        glLightfv(self.l_id, GL_POSITION, (0, 0, 0, 1.0))
        glTranslatef(-self.size['x'] / 2, -self.size['y'] / 2, -self.size['z'] / 2)
        draw_rect_single_texture(self.size['x'], self.size['y'], self.size['z'], self.t_side_id)

        glPopMatrix()


class WoodenPlank(Drawable):
    def __init__(self, t_side_id, t_top_bottom_id, size=None, position=None, rotate=None):
        super().__init__()
        if size is None:
            size = dict(x=0, y=0, z=0)

        if position is None:
            position = dict(x=0, y=0, z=0)

        if rotate is None:
            rotate = dict(x=0, y=0, z=0)

        self.size = size
        self.position = position
        self.rotate = rotate
        self.t = [t_side_id, t_side_id, t_top_bottom_id, t_top_bottom_id, t_side_id, t_side_id]

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate['x'], 1, 0, 0)
        glRotatef(self.rotate['y'], 0, 1, 0)
        glRotatef(self.rotate['z'], 0, 0, 1)
        # self.rotate['y'] += 1
        # self.rotate['x'] += 1
        # self.rotate['z'] += 1
        glTranslatef(-self.size['x'] / 2, -self.size['y'] / 2, -self.size['z'] / 2)
        draw_rect_multi_textures(self.size['x'], self.size['y'], self.size['z'], self.t)
        glPopMatrix()


class WoodenFan(Drawable):
    def __init__(self, t_side_id, t_top_bottom_id, size, position, speed):
        super().__init__()
        self.rotate = 0
        self.speed = speed
        self.position = position
        self.t_top_bottom_id = t_top_bottom_id
        self.t_side_id = t_side_id
        self.size = size
        self.objects = list()

        axis_h = 0.96 * size['y']
        axis_s = size['x'] * 0.01
        blade_h = size['y'] - axis_h
        blade_l = size['x'] / 2
        blade_w = blade_h * 10
        angle = 15

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=axis_s, y=axis_h, z=axis_s),
                        position=dict(x=0, y=blade_h / 2, z=0),
                        rotate=dict(x=0, y=0, z=0))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=blade_h, y=blade_l, z=blade_w),
                        position=dict(x=-blade_l / 2, y=-axis_h / 2 + blade_h / 2, z=0),
                        rotate=dict(x=angle, y=0, z=90))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=blade_h, y=blade_l, z=blade_w),
                        position=dict(x=blade_l / 2, y=-axis_h / 2 + blade_h / 2, z=0),
                        rotate=dict(x=-angle, y=0, z=90))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=blade_h, y=blade_l, z=blade_w),
                        position=dict(x=0, y=-axis_h / 2 + blade_h / 2, z=-blade_l / 2),
                        rotate=dict(x=90, y=angle + 90, z=180))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=blade_h, y=blade_l, z=blade_w),
                        position=dict(x=0, y=-axis_h / 2 + blade_h / 2, z=blade_l / 2),
                        rotate=dict(x=90, y=90 - angle, z=180))
        )

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate, 0, 1, 0)
        self.rotate += self.speed

        for obj in self.objects:
            obj.draw()

        glPopMatrix()


class WoodenTable(Drawable):
    def __init__(self, t_side_id, t_top_bottom_id, size, position, rotate):
        super().__init__()
        self.rotate = rotate
        self.position = position
        self.t_top_bottom_id = t_top_bottom_id
        self.t_side_id = t_side_id
        self.size = size
        self.objects = list()

        table_h = 0.1 * size['y']
        column_h = size['y'] - table_h
        column_s = size['x'] * 0.05

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=size['x'], y=table_h, z=size['z']),
                        position=dict(x=0, y=size['y'] / 2 - table_h / 2, z=0),
                        rotate=dict(x=0, y=0, z=0))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=column_s, y=column_h, z=column_s),
                        position=dict(x=-size['x'] / 2 + column_s / 2, y=-table_h / 2, z=-size['z'] / 2 + column_s / 2),
                        rotate=dict(x=0, y=0, z=0))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=column_s, y=column_h, z=column_s),
                        position=dict(x=size['x'] / 2 - column_s / 2, y=-table_h / 2, z=size['z'] / 2 - column_s / 2),
                        rotate=dict(x=0, y=0, z=0))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=column_s, y=column_h, z=column_s),
                        position=dict(x=size['x'] / 2 - column_s / 2, y=-table_h / 2, z=-size['z'] / 2 + column_s / 2),
                        rotate=dict(x=0, y=0, z=0))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=column_s, y=column_h, z=column_s),
                        position=dict(x=-size['x'] / 2 + column_s / 2, y=-table_h / 2, z=size['z'] / 2 - column_s / 2),
                        rotate=dict(x=0, y=0, z=0))
        )

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate['x'], 1, 0, 0)
        glRotatef(self.rotate['y'], 0, 1, 0)
        glRotatef(self.rotate['z'], 0, 0, 1)

        for obj in self.objects:
            obj.draw()

        glPopMatrix()


class Gazebo(Drawable):
    def __init__(self, t_side_id, t_top_bottom_id, t_lamp, size=None, position=None, rotate=None):
        super().__init__()
        self.t_lamp = t_lamp
        if size is None:
            size = dict(x=0, y=0, z=0)

        if position is None:
            position = dict(x=0, y=0, z=0)

        if rotate is None:
            rotate = dict(x=0, y=0, z=0)

        self.size = size
        self.position = position
        self.rotate = rotate

        self.objects = list()

        floor_height = size['y'] * 0.1
        walls_height = size['y'] * 0.6
        roof_height = size['y'] * 0.3
        table_height = size['y'] * 0.25

        self.objects.append(
            GazeboFloor(t_side_id, t_top_bottom_id,
                        size=dict(x=size['x'], y=floor_height, z=size['z']),
                        position=dict(x=0, y=-size['y'] / 2 + floor_height / 2, z=0),
                        rotate=dict(x=0, y=0, z=0)
                        )
        )

        self.objects.append(
            GazeboWalls(t_side_id, t_top_bottom_id,
                        size=dict(x=size['x'], y=walls_height, z=size['z']),
                        position=dict(x=0, y=-size['y'] / 2 + floor_height + walls_height / 2, z=0),
                        rotate=dict(x=0, y=0, z=0)
                        )
        )

        self.objects.append(
            GazeboRoof(t_side_id, t_top_bottom_id, t_lamp,
                       size=dict(x=size['x'], y=roof_height, z=size['z']),
                       position=dict(x=0, y=size['y'] / 2 - roof_height / 2, z=0),
                       rotate=dict(x=0, y=0, z=0)
                       )
        )

        self.objects.append(
            WoodenTable(t_side_id, t_top_bottom_id,
                        size=dict(x=size['x'] * 0.3, y=table_height, z=size['z'] * 0.3),
                        position=dict(x=0, y=-size['y'] / 2 + floor_height + table_height / 2, z=0),
                        rotate=dict(x=0, y=0, z=0)
                        )
        )

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate['x'], 1, 0, 0)
        glRotatef(self.rotate['y'], 0, 1, 0)
        glRotatef(self.rotate['z'], 0, 0, 1)

        for obj in self.objects:
            obj.draw()

        glPopMatrix()


class GazeboFloor(Drawable):
    def __init__(self, t_side_id, t_top_bottom_id, size, position, rotate):
        super().__init__()
        self.rotate = rotate
        self.position = position
        self.t_top_bottom_id = t_top_bottom_id
        self.t_side_id = t_side_id
        self.size = size
        self.objects = list()

        wooden_planks_count = 24
        wooden_plank_height = 0.2 * size['y']
        wooden_plank_size_x = size['x'] / wooden_planks_count
        wooden_plank_size_z = size['z']

        wooden_column_height = size['y'] - wooden_plank_height * 2
        wooden_column_side_size_x = 0.05 * size['x']
        wooden_column_side_size_z = 0.05 * size['z']

        start_x = -size['x'] / 2 + wooden_plank_size_x / 2
        for i in range(0, wooden_planks_count):
            self.objects.append(
                WoodenPlank(t_side_id, t_top_bottom_id,
                            size=dict(x=wooden_plank_size_x, y=wooden_plank_size_z, z=wooden_plank_height),
                            position=dict(x=start_x, y=wooden_column_height / 2 + wooden_plank_height / 2, z=0),
                            rotate=dict(x=90, y=0, z=0))
            )
            start_x += wooden_plank_size_x

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=wooden_column_side_size_z, y=size['x'], z=wooden_plank_height),
                        position=dict(x=0, y=wooden_column_height / 2 - wooden_plank_height / 2,
                                      z=size['z'] / 2 - wooden_column_side_size_z / 2),
                        rotate=dict(x=90, y=0, z=90))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=wooden_column_side_size_z, y=size['x'], z=wooden_plank_height),
                        position=dict(x=0, y=wooden_column_height / 2 - wooden_plank_height / 2,
                                      z=-size['z'] / 2 + wooden_column_side_size_z / 2),
                        rotate=dict(x=90, y=0, z=90))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=wooden_column_side_size_x, y=wooden_column_height, z=wooden_column_side_size_z),
                        position=dict(x=size['x'] / 2 - wooden_column_side_size_x / 2, y=-wooden_plank_height,
                                      z=size['z'] / 2 - wooden_column_side_size_z / 2))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=wooden_column_side_size_x, y=wooden_column_height, z=wooden_column_side_size_z),
                        position=dict(x=-size['x'] / 2 + wooden_column_side_size_x / 2, y=-wooden_plank_height,
                                      z=size['z'] / 2 - wooden_column_side_size_z / 2))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=wooden_column_side_size_x, y=wooden_column_height, z=wooden_column_side_size_z),
                        position=dict(x=size['x'] / 2 - wooden_column_side_size_x / 2, y=-wooden_plank_height,
                                      z=-size['z'] / 2 + wooden_column_side_size_z / 2))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=wooden_column_side_size_x, y=wooden_column_height, z=wooden_column_side_size_z),
                        position=dict(x=-size['x'] / 2 + wooden_column_side_size_x / 2, y=-wooden_plank_height,
                                      z=-size['z'] / 2 + wooden_column_side_size_z / 2))
        )

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate['x'], 1, 0, 0)
        glRotatef(self.rotate['y'], 0, 1, 0)
        glRotatef(self.rotate['z'], 0, 0, 1)

        for obj in self.objects:
            obj.draw()

        glPopMatrix()


class GazeboWalls(Drawable):
    def __init__(self, t_side_id, t_top_bottom_id, size, position, rotate):
        super().__init__()
        self.rotate = rotate
        self.position = position
        self.t_top_bottom_id = t_top_bottom_id
        self.t_side_id = t_side_id
        self.size = size
        self.objects = list()

        pillars_count_x = 5
        pillars_count_z = 5

        pillar_y = size['y']
        pillar_x = size['x'] * 0.025
        pillar_z = size['x'] * 0.025

        pillar_y2 = size['y'] * 0.45
        pillar_x2 = size['x'] * 0.015
        pillar_z2 = size['x'] * 0.015

        delta_z = (size['z'] - pillar_z) / (pillars_count_z - 1)
        delta_x = (size['x'] - pillar_x) / (pillars_count_x - 1)
        delta_z2 = (delta_z - pillar_z2) / (pillars_count_z + 1)
        delta_x2 = (delta_x - pillar_x2) / (pillars_count_x + 1)

        railing_width = size['x'] * 0.025
        railing_height = railing_width / 2

        start_x = -size['x'] / 2 + pillar_x / 2
        for x in range(0, pillars_count_x):
            self.objects.append(
                WoodenPlank(t_side_id, t_top_bottom_id,
                            size=dict(x=pillar_x, y=pillar_y, z=pillar_z),
                            position=dict(x=start_x, y=0,  # pillar_y / 2
                                          z=-size['z'] / 2 + pillar_z / 2))
            )

            if x != pillars_count_x - 1:
                start_x2 = start_x + delta_x2 + pillar_x2 / 2
                for x2 in range(0, pillars_count_x):
                    self.objects.append(
                        WoodenPlank(t_side_id, t_top_bottom_id,
                                    size=dict(x=pillar_x2, y=pillar_y2, z=pillar_z2),
                                    position=dict(x=start_x2, y=-pillar_y / 2 + pillar_y2 / 2,
                                                  z=-size['z'] / 2 + pillar_z2 / 2))
                    )

                    self.objects.append(
                        WoodenPlank(t_side_id, t_top_bottom_id,
                                    size=dict(x=pillar_x2, y=pillar_y2, z=pillar_z2),
                                    position=dict(x=start_x2, y=-pillar_y / 2 + pillar_y2 / 2,
                                                  z=size['z'] / 2 - pillar_z2 / 2))
                    )

                    start_x2 += delta_x2

            self.objects.append(
                WoodenPlank(t_side_id, t_top_bottom_id,
                            size=dict(x=pillar_x, y=pillar_y, z=pillar_z),
                            position=dict(x=start_x, y=0,  # pillar_y / 2
                                          z=size['z'] / 2 - pillar_z / 2))
            )

            start_x += delta_x

        start_z = -size['z'] / 2 + pillar_z / 2 + delta_z
        for z in range(1, pillars_count_z):
            start_z2 = start_z + delta_z2 + pillar_z2 / 2 - delta_z
            for z2 in range(0, pillars_count_z):
                if z != 1:
                    self.objects.append(
                        WoodenPlank(t_side_id, t_top_bottom_id,
                                    size=dict(x=pillar_x2, y=pillar_y2, z=pillar_z2),
                                    position=dict(x=-size['x'] / 2 + pillar_x2 / 2, y=-pillar_y / 2 + pillar_y2 / 2,
                                                  z=start_z2))
                    )

                if z != pillars_count_z - 1:
                    self.objects.append(
                        WoodenPlank(t_side_id, t_top_bottom_id,
                                    size=dict(x=pillar_x2, y=pillar_y2, z=pillar_z2),
                                    position=dict(x=size['x'] / 2 - pillar_x2 / 2, y=-pillar_y / 2 + pillar_y2 / 2,
                                                  z=start_z2))
                    )

                start_z2 += delta_z2

            if z != pillars_count_z - 1:
                self.objects.append(
                    WoodenPlank(t_side_id, t_top_bottom_id,
                                size=dict(x=pillar_x, y=pillar_y, z=pillar_z),
                                position=dict(x=-size['x'] / 2 + pillar_x / 2, y=0,  # pillar_y / 2
                                              z=start_z))
                )

                self.objects.append(
                    WoodenPlank(t_side_id, t_top_bottom_id,
                                size=dict(x=pillar_x, y=pillar_y, z=pillar_z),
                                position=dict(x=size['x'] / 2 - pillar_x / 2, y=0,  # pillar_y / 2
                                              z=start_z))
                )

            start_z += delta_z

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=railing_width, y=size['z'] - delta_z - pillar_z * 2, z=railing_height),
                        rotate=dict(x=90, y=0, z=0),
                        position=dict(x=-size['x'] / 2 + railing_width / 2,
                                      y=-(pillar_y / 2 - pillar_y2) + railing_height / 2,
                                      z=delta_z / 2))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=railing_width, y=size['z'] - delta_z - pillar_z * 2, z=railing_height),
                        rotate=dict(x=90, y=0, z=0),
                        position=dict(x=size['x'] / 2 - railing_width / 2,
                                      y=-(pillar_y / 2 - pillar_y2) + railing_height / 2,
                                      z=-delta_z / 2))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=railing_width, y=size['x'] - pillar_z * 2, z=railing_height),
                        rotate=dict(x=90, y=0, z=90),
                        position=dict(x=0,
                                      y=-(pillar_y / 2 - pillar_y2) + railing_height / 2,
                                      z=size['z'] / 2 - railing_width / 2))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=railing_width, y=size['x'] - pillar_z * 2, z=railing_height),
                        rotate=dict(x=90, y=0, z=90),
                        position=dict(x=0,
                                      y=-(pillar_y / 2 - pillar_y2) + railing_height / 2,
                                      z=-size['z'] / 2 + railing_width / 2))
        )

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate['x'], 1, 0, 0)
        glRotatef(self.rotate['y'], 0, 1, 0)
        glRotatef(self.rotate['z'], 0, 0, 1)

        for obj in self.objects:
            obj.draw()

        glPopMatrix()


class GazeboRoof(Drawable):
    def __init__(self, t_side_id, t_top_bottom_id, t_lamp, size, position, rotate):
        super().__init__()
        self.rotate = rotate
        self.position = position
        self.t_top_bottom_id = t_top_bottom_id
        self.t_side_id = t_side_id
        self.size = size
        self.objects = list()

        fan_h = size['y'] * 0.2
        fan_s = size['x'] * 0.2

        balk_height = size['y'] * 0.12
        balk_width = size['y'] * 0.16
        size_x = size['x'] * 1.2
        size_z = size['z'] * 1.2

        columns_count = 7
        column_height = size['y'] - balk_height * 2

        light_source_s = balk_width * 1.2

        self.objects.append(
            Lamp(t_lamp,
                 size=dict(x=light_source_s, y=light_source_s, z=light_source_s),
                 position=dict(x=-size_x / 2 + balk_width / 2,
                               y=-size['y'] / 2 + balk_height / 2,
                               z=-size['z'] / 2 + balk_width / 2),
                 rotate=dict(x=0, y=0, z=0), index=4)
        )

        self.objects.append(
            Lamp(t_lamp,
                 size=dict(x=light_source_s, y=light_source_s, z=light_source_s),
                 position=dict(x=size_x / 2 - balk_width / 2,
                               y=-size['y'] / 2 + balk_height / 2,
                               z=-size['z'] / 2 + balk_width / 2),
                 rotate=dict(x=0, y=0, z=0), index=5)
        )

        self.objects.append(
            Lamp(t_lamp,
                 size=dict(x=light_source_s, y=light_source_s, z=light_source_s),
                 position=dict(x=-size_x / 2 + balk_width / 2,
                               y=-size['y'] / 2 + balk_height / 2,
                               z=size['z'] / 2 - balk_width / 2),
                 rotate=dict(x=0, y=0, z=0), index=6)
        )

        self.objects.append(
            Lamp(t_lamp,
                 size=dict(x=light_source_s, y=light_source_s, z=light_source_s),
                 position=dict(x=size_x / 2 - balk_width / 2,
                               y=-size['y'] / 2 + balk_height / 2,
                               z=size['z'] / 2 - balk_width / 2),
                 rotate=dict(x=0, y=0, z=0), index=7)
        )

        self.objects.append(
            WoodenFan(t_side_id, t_top_bottom_id,
                      size=dict(x=fan_s, y=fan_h, z=fan_s),
                      position=dict(x=0, y=-size['y'] / 2 - fan_h / 2 + balk_height, z=0),
                      speed=3)
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=balk_height, y=size['x'], z=balk_width),
                        position=dict(x=0, y=-size['y'] / 2 + balk_height / 2, z=-size['z'] / 2 + balk_width / 2),
                        rotate=dict(x=0, y=0, z=90))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=balk_height, y=size['x'], z=balk_width),
                        position=dict(x=0, y=-size['y'] / 2 + balk_height / 2, z=size['z'] / 2 - balk_width / 2),
                        rotate=dict(x=0, y=0, z=90))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=balk_width, y=size['z'], z=balk_height),
                        position=dict(x=size['x'] / 2 - balk_width / 2, y=-size['y'] / 2 + balk_height / 2, z=0),
                        rotate=dict(x=90, y=0, z=0))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=balk_width, y=size['z'], z=balk_height),
                        position=dict(x=-size['x'] / 2 + balk_width / 2, y=-size['y'] / 2 + balk_height / 2, z=0),
                        rotate=dict(x=90, y=0, z=0))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=balk_height, y=size_x, z=balk_width),
                        position=dict(x=0, y=-size['y'] / 2 + balk_height * 1.5, z=-size['z'] / 2 + balk_width / 2),
                        rotate=dict(x=0, y=0, z=90))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=balk_height, y=size_x, z=balk_width),
                        position=dict(x=0, y=-size['y'] / 2 + balk_height * 1.5, z=size['z'] / 2 - balk_width / 2),
                        rotate=dict(x=0, y=0, z=90))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=balk_height, y=size['x'], z=balk_width),
                        position=dict(x=0, y=-size['y'] / 2 + balk_height * 1.5, z=0),
                        rotate=dict(x=0, y=0, z=90))
        )

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=balk_height, y=size_x, z=balk_width),
                        position=dict(x=0, y=size['y'] / 2 + balk_height / 2, z=0),
                        rotate=dict(x=0, y=0, z=90))
        )

        start_x = -size['x'] / 2 + balk_height / 2
        delta_x = (size['x'] - balk_height) / (columns_count - 1)

        for i in range(0, columns_count):
            self.objects.append(
                WoodenPlank(t_side_id, t_top_bottom_id,
                            size=dict(x=balk_width, y=column_height, z=balk_height),
                            position=dict(x=start_x, y=balk_height, z=0),
                            rotate=dict(x=0, y=90, z=0))
            )

            start_x += delta_x

        l = size['z'] * 0.7
        a = degrees(atan((column_height + balk_height) / (size['z'] / 2 - balk_width / 2)))
        dz = l / 2 * cos(radians(a))
        dy = l / 2 * sin(radians(a))
        dy -= ((size['y']) / 2 + balk_height)

        balks_count = 11
        delta_x = (size_x - balk_width) / (balks_count - 1)
        start_x = -size_x / 2 + balk_width / 2

        for i in range(0, balks_count):
            self.objects.append(
                WoodenPlank(t_side_id, t_top_bottom_id,
                            size=dict(x=balk_width, y=l, z=balk_height),
                            position=dict(x=start_x, y=-dy, z=-dz),
                            rotate=dict(x=90 - a, y=0, z=0))
            )

            self.objects.append(
                WoodenPlank(t_side_id, t_top_bottom_id,
                            size=dict(x=balk_width, y=l, z=balk_height),
                            position=dict(x=start_x, y=-dy, z=dz),
                            rotate=dict(x=-90 + a, y=0, z=0))
            )

            start_x += delta_x

        roof_plank_width = size['z'] * 0.1
        roof_plank_height = size['y'] * 0.1
        roof_plank_l = size_x
        rotate = 10
        width_scale_factor = 0.8
        start_y = size['y'] / 2 + balk_height
        roof_plank_dy = roof_plank_height * width_scale_factor / tan(radians(a))
        planks_count = int(l / roof_plank_width) + 1

        # initial planks

        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=roof_plank_width, y=roof_plank_l, z=roof_plank_height),
                        position=dict(x=0, y=start_y, z=0),
                        rotate=dict(x=90, y=0, z=90))
        )
        self.objects.append(
            WoodenPlank(t_side_id, t_top_bottom_id,
                        size=dict(x=roof_plank_width * width_scale_factor, y=roof_plank_l, z=roof_plank_height),
                        position=dict(x=0, y=start_y + roof_plank_height, z=0),
                        rotate=dict(x=90, y=0, z=90))
        )

        for i in range(0, planks_count):
            self.objects.append(
                WoodenPlank(t_side_id, t_top_bottom_id,
                            size=dict(x=roof_plank_width, y=roof_plank_l, z=roof_plank_height),
                            position=dict(x=0, y=start_y,
                                          z=-roof_plank_width / 2 - i * roof_plank_width * width_scale_factor),
                            rotate=dict(x=-rotate + 90, y=0, z=90))
            )

            self.objects.append(
                WoodenPlank(t_side_id, t_top_bottom_id,
                            size=dict(x=roof_plank_width, y=roof_plank_l, z=roof_plank_height),
                            position=dict(x=0, y=start_y,
                                          z=roof_plank_width / 2 + i * roof_plank_width * width_scale_factor),
                            rotate=dict(x=rotate + 90, y=0, z=90))
            )

            start_y -= roof_plank_dy

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.position['x'], self.position['y'], self.position['z'])
        glRotatef(self.rotate['x'], 1, 0, 0)
        glRotatef(self.rotate['y'], 0, 1, 0)
        glRotatef(self.rotate['z'], 0, 0, 1)

        for obj in self.objects:
            obj.draw()

        glPopMatrix()


def draw_rect_multi_textures(lx, ly, lz, t: list):
    n = [0, 0, 1]
    # near
    glBindTexture(GL_TEXTURE_2D, t[4])
    glNormal3f(n[0], n[1], n[2])
    ss = [0, 1 / ly, 0, 0]
    tt = [1 / lx, 0, 0, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, lz)
    glVertex3f(0, ly, lz)
    glVertex3f(lx, ly, lz)
    glVertex3f(lx, 0, lz)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, t[5])
    # far
    n = [0, 0, -1]
    glNormal3f(n[0], n[1], n[2])
    ss = [0, 1 / ly, 0, 0]
    tt = [1 / lx, 0, 0, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, ly, 0)
    glVertex3f(lx, ly, 0)
    glVertex3f(lx, 0, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, t[2])
    # top
    n = [0, 1, 0]
    glNormal3f(n[0], n[1], n[2])
    ss = [1 / lx, 0, 0, 0]
    tt = [0, 0, 1 / lz, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(0, ly, 0)
    glVertex3f(0, ly, lz)
    glVertex3f(lx, ly, lz)
    glVertex3f(lx, ly, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, t[3])
    # bottom
    n = [0, -1, 0]
    glNormal3f(n[0], n[1], n[2])
    ss = [1 / lx, 0, 0, 0]
    tt = [0, 0, 1 / lz, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, lz)
    glVertex3f(lx, 0, lz)
    glVertex3f(lx, 0, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, t[0])
    # left
    n = [1, 0, 0]
    glNormal3f(n[0], n[1], n[2])
    ss = [0, 1 / ly, 0, 0]
    tt = [0, 0, 1 / lz, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(lx, 0, 0)
    glVertex3f(lx, 0, lz)
    glVertex3f(lx, ly, lz)
    glVertex3f(lx, ly, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, t[1])
    # right
    n = [-1, 0, 0]
    glNormal3f(n[0], n[1], n[2])
    ss = [0, 1 / ly, 0, 0]
    tt = [0, 0, 1 / lz, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, lz)
    glVertex3f(0, ly, lz)
    glVertex3f(0, ly, 0)
    glEnd()


def draw_rect_single_texture(lx, ly, lz, t: int):
    n = [0, 0, 1]
    # near
    glBindTexture(GL_TEXTURE_2D, t)
    glNormal3f(n[0], n[1], n[2])
    ss = [0, 1 / ly, 0, 0]
    tt = [1 / lx, 0, 0, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, lz)
    glVertex3f(0, ly, lz)
    glVertex3f(lx, ly, lz)
    glVertex3f(lx, 0, lz)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, t)
    # far
    n = [0, 0, -1]
    glNormal3f(n[0], n[1], n[2])
    ss = [0, 1 / ly, 0, 0]
    tt = [1 / lx, 0, 0, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, ly, 0)
    glVertex3f(lx, ly, 0)
    glVertex3f(lx, 0, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, t)
    # top
    n = [0, 1, 0]
    glNormal3f(n[0], n[1], n[2])
    ss = [1 / lx, 0, 0, 0]
    tt = [0, 0, 1 / lz, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(0, ly, 0)
    glVertex3f(0, ly, lz)
    glVertex3f(lx, ly, lz)
    glVertex3f(lx, ly, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, t)
    # bottom
    n = [0, -1, 0]
    glNormal3f(n[0], n[1], n[2])
    ss = [1 / lx, 0, 0, 0]
    tt = [0, 0, 1 / lz, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, lz)
    glVertex3f(lx, 0, lz)
    glVertex3f(lx, 0, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, t)
    # left
    n = [1, 0, 0]
    glNormal3f(n[0], n[1], n[2])
    ss = [0, 1 / ly, 0, 0]
    tt = [0, 0, 1 / lz, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(lx, 0, 0)
    glVertex3f(lx, 0, lz)
    glVertex3f(lx, ly, lz)
    glVertex3f(lx, ly, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, t)
    # right
    n = [-1, 0, 0]
    glNormal3f(n[0], n[1], n[2])
    ss = [0, 1 / ly, 0, 0]
    tt = [0, 0, 1 / lz, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, lz)
    glVertex3f(0, ly, lz)
    glVertex3f(0, ly, 0)
    glEnd()


def draw_model(w, h, t):
    glPushMatrix()

    glPushMatrix()
    glRotate(-45, 0, 1, 0)
    glTranslatef((sqrt(w * w + w * w) - w) / 2, 0, 0)

    glBindTexture(GL_TEXTURE_2D, t)
    ss = [0, 1 / w, 0, 0]
    tt = [1 / w, 0, 0, 0]
    glTexGendv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGendv(GL_T, GL_OBJECT_PLANE, tt)

    n = [0, 0, -1]
    glNormal3f(n[0], n[1], n[2])
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, h, 0)
    glVertex3f(w, h, 0)
    glVertex3f(w, 0, 0)
    glEnd()
    n = [0, 0, 1]
    glNormal3f(n[0], n[1], n[2])
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0.001)
    glVertex3f(0, h, 0.001)
    glVertex3f(w, h, 0.001)
    glVertex3f(w, 0, 0.001)
    glEnd()

    glPopMatrix()

    glRotate(45, 0, 1, 0)
    glTranslatef(sqrt(w * w + w * w) / -2, 0, sqrt(w * w + w * w) / 2)
    glTranslatef((sqrt(w * w + w * w) - w) / 2, 0, 0)

    n = [0, 0, -1]
    glNormal3f(n[0], n[1], n[2])
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, h, 0)
    glVertex3f(w, h, 0)
    glVertex3f(w, 0, 0)
    glEnd()
    n = [0, 0, 1]
    glNormal3f(n[0], n[1], n[2])
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0.001)
    glVertex3f(0, h, 0.001)
    glVertex3f(w, h, 0.001)
    glVertex3f(w, 0, 0.001)
    glEnd()

    glPopMatrix()
