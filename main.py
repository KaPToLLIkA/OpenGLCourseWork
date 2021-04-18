from global_state import GlobalState
from input_devices import KeyboardEventCallbacks, MouseEventCallbacks
from render_scene import TexturesIds, Scene

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

    glLightfv(GL_LIGHT0, GL_DIFFUSE, (204 / 256, 0 / 256, 255 / 256, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (204 / 256, 0 / 256, 255 / 256, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (204 / 256, 0 / 256, 255 / 256, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (100.0, 100.0, 100.0, 0.0))

    glViewport(0, 0, g_state.window.width, g_state.window.height)

    special.glutTimerFunc(33, scene.update, 1)
    glutMainLoop()


if __name__ == "__main__":
    main()