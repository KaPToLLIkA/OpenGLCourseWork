from global_state import GlobalState
from input_devices import KeyboardEventCallbacks, MouseEventCallbacks
from render_scene import TexturesIds, Scene
from scene_parts import StaticBush, Gazebo, Axes, Grass

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def main():
    g_state = GlobalState()
    keyboard = KeyboardEventCallbacks(g_state)
    mouse = MouseEventCallbacks(g_state)
    scene = Scene(g_state, mouse, keyboard)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(g_state.window.width, g_state.window.height)
    glutInitWindowPosition(0, 0)
    glutInit(sys.argv)
    glutCreateWindow("")

    glutDisplayFunc(scene.draw)
    glutReshapeFunc(scene.reshape)

    # setup keyboard
    special.glutKeyboardFunc(keyboard.keyboard_func)
    special.glutKeyboardUpFunc(keyboard.keyboard_up_func)

    glutSpecialFunc(keyboard.special_func)
    glutSpecialUpFunc(keyboard.special_up_func)

    # setup mouse
    special.glutMouseFunc(mouse.mouse_func)
    special.glutMotionFunc(mouse.motion_func)
    special.glutPassiveMotionFunc(mouse.passive_motion_func)

    # enables
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT4)
    glEnable(GL_LIGHT5)
    glEnable(GL_LIGHT6)
    glEnable(GL_LIGHT7)

    # textures loading
    glEnable(GL_TEXTURE_2D)
    TexturesIds.load_all_textures()

    gazebo_size = dict(x=45, y=30, z=30)
    grass_size = dict(x=100, y=2, z=100)
    bush_size = dict(x=15, y=15)

    scene.add_drawable_object(
        Axes(length=5)
    )

    scene.add_drawable_object(
        Grass(TexturesIds.grass[0], size=grass_size)
    )

    scene.add_drawable_object(
        Gazebo(TexturesIds.wood[0], TexturesIds.wood[1], TexturesIds.light,
               size=gazebo_size, position=dict(x=0, y=grass_size['y'] / 2 + gazebo_size['y'] / 2, z=0))
    )

    scene.add_drawable_object(
        StaticBush(TexturesIds.bush[0], width=bush_size['x'], height=bush_size['y'],
                   position=dict(x=gazebo_size['x'], y=grass_size['y'] / 2, z=gazebo_size['z']))
    )

    scene.add_drawable_object(
        StaticBush(TexturesIds.bush[1], width=bush_size['x'], height=bush_size['y'],
                   position=dict(x=-gazebo_size['x'], y=grass_size['y'] / 2, z=0))
    )

    scene.add_drawable_object(
        StaticBush(TexturesIds.bush[2], width=bush_size['x'], height=bush_size['y'],
                   position=dict(x=gazebo_size['x'], y=grass_size['y'] / 2, z=-gazebo_size['z']))
    )

    scene.add_drawable_object(
        StaticBush(TexturesIds.bush[3], width=bush_size['x'], height=bush_size['y'],
                   position=dict(x=gazebo_size['x'], y=grass_size['y'] / 2, z=0))
    )

    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 100.0, 100.0, 0.0))

    glLightfv(GL_LIGHT1, GL_DIFFUSE, (255 / 256, 210 / 256, 120 / 256, 1))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (255 / 256, 210 / 256, 120 / 256, 1))
    glLightfv(GL_LIGHT1, GL_AMBIENT, (255 / 256, 210 / 256, 120 / 256, 1))
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.0014)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.000007)

    glViewport(0, 0, g_state.window.width, g_state.window.height)

    special.glutTimerFunc(33, scene.update, 1)
    glutMainLoop()


if __name__ == "__main__":
    main()