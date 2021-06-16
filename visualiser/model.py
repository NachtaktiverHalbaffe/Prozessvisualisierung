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
        # static color(s) of parts of the 3d model
        self.staticColor = (1.0, 1.0, 1.0)
        # state of workingpiece which is passed down from
        # processvisualisation
        self.isAssembled = False
        self.isPackaged = False
        self.color = '#000000'
        self.paintColor = '#000000'
        self.alpha = 1
        # path to the .obj-files of the model
        self.modelNames = []
        # "master" scale to all models
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
    animations which needs to be overridden in inherited class
    """

    #! Need to be overridden
    # Draw a static model (animation is applied in visualiser).
    # Translate, rotate and scale the .obj-models to correct the initial position
    # Apply self.staticcolor to parts which are protected from the "color"-task and
    # self.color to parts which can be painted by the "color"- task
    def drawModel(self):
        pass

    #! Need to be overridden
    # Draw a model an apply a assemble animation to it. Each Model
    # needs its own assemble animation (unlike package, unpackage and color which are applied to an static model).
    # Animate with translations and rotations.
    # @params:
    # time: elapsed time of the workingprocess
    def assemble(self, time):
        pass

    #! Need to be overridden
    # Draw a model an apply a generic animation to it. Each Model
    # needs its own assemble animation (unlike package, unpackage and color which are applied to an static model).
    # Animate with translations and rotations.
    # @params:
    # time: elapsed time of the workingprocess
    def generic(self, time):
        pass

    """
    utils
    """

    # This Methods gets model data (vertices, faces etc. from the .obj file) and creates a 3D model
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

        glPushMatrix()
        # scaling Model
        glScalef(*scene_scale)
        # draw Model
        for mesh in model.mesh_list:
            glEnable(GL_COLOR_MATERIAL)
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    # draw face
                    glVertex3f(*model.vertices[vertex_i])
                    # color face
                    glColor3fv(color)
            glEnd()
            glDisable(GL_COLOR_MATERIAL)
        glPopMatrix()

    # convert hex color values to rgb values (float between 0 and 1)
    def _hexToRGB(self, hex):
        colorRGBBin = tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))
        colorRGBFloat = tuple(color / 255. for color in colorRGBBin)
        return colorRGBFloat
