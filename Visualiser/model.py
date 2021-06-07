"""
Filename: model.py
Version name: 0.1, 2021-05-21
Short description: 3d model Superclass

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Model(object):

    def __init__(self):
        # a inherited class should set default values for all of this params
        self.isAssembled = False
        self.isPackaged = False
        self.staticColor = (0.0, 0.0, 0.0)
        self.color = '#000000'
        self.paintColor = '#000000'
        self.alpha = 1
        self.modelNames = []
        self.scaledSize = 1
        self.models = []

    """
    Setter
    """

    def setAssembled(self, isAssembled):
        self.isAssembled = isAssembled

    def setPackaged(self, isPackaged):
        self.isPackaged = isPackaged

    def setColor(self, color):
        self.color = color

    def setAlpha(self, alpha):
        self.alpha = alpha

    def setPaintColor(self, paintColor):
        self.paintColor = paintColor

    """
    utils
    """
    # This Methods gets model data and creates a 3D model

    def _drawModel(self, model, color):
        # calculating parameter
        scene_box = (model.vertices[0], model.vertices[0])
        for vertex in model.vertices:
            min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
            max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
            scene_box = (min_v, max_v)

        scene_size = [scene_box[1][i]-scene_box[0][i] for i in range(3)]
        max_scene_size = max(scene_size)
        scene_scale = [self.scaledSize/max_scene_size for i in range(3)]

        # scaling Model
        glPushMatrix()
        glScalef(*scene_scale)
        # draw Model
        for mesh in model.mesh_list:
            glEnable(GL_COLOR_MATERIAL)
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
                    glColor3fv(color)
            glEnd()
            glDisable(GL_COLOR_MATERIAL)
        glPopMatrix()

    def _hexToRGB(self, hex):
        colorRGBBin = tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))
        colorRGBFloat = tuple(color / 255. for color in colorRGBBin)
        return colorRGBFloat
