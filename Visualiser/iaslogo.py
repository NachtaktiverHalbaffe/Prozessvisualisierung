"""
Filename: iaslogo.py
Version name: 0.1, 2021-05-21
Short description: model object of ias logo

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
import pywavefront
import OpenGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from visualiser import Visualiser


class IASModel(object):
    def __init__(self):
        self.isAssembled = False
        self.isPackaged = False
        self.staticColor = (0.007, 0.175, 0.546)
        self.color = '#CCCCCC'
        self.modelNames = [
            '3dmodels/IAS_Letter_I_FINAL.obj',
            '3dmodels/IAS_Letter_A_FINAL.obj',
            '3dmodels/IAS_Letter_S_FINAL.obj'
        ]
        self.scaledSize = 4
        self.models = []
        for model in self.modelNames:
            self.models.append(pywavefront.Wavefront(
                model, collect_faces=True))

    # draws model with right state
    def animateModel(self):
        if not self.isPackaged:
            for i in range(len(self.models)):
                if i == 0:
                    # correcting position
                    glPushMatrix()
                    if self.isAssembled:
                        glTranslated(-0.2, 0, 0)
                    else:
                        glTranslated(-3, 0, 0)
                    glRotated(90, 0, 1, 0)
                    glScaled(0.75, 0.75, 0.75)
                    # coloring
                    glEnable(GL_COLOR_MATERIAL)
                    glColor3d(
                        self.staticColor[0], self.staticColor[1], self.staticColor[2])
                    self._drawModel(self.models[i])
                    glDisable(GL_COLOR_MATERIAL)
                    glPopMatrix()
                elif i == 1:
                    glPushMatrix()
                    # correcting position
                    glRotated(90, 0, 1, 0)
                    # coloring depending if piece was painted or not
                    glEnable(GL_COLOR_MATERIAL)
                    if self.color != '#000000':
                        colorRGB = self._hexToRGB(self.color)
                    else:
                        colorRGB = (1, 1, 1)
                    glColor3d(colorRGB[0], colorRGB[1], colorRGB[2])
                    self._drawModel(self.models[i])
                    self._drawModel(self.models[i])
                    glDisable(GL_COLOR_MATERIAL)
                    glPopMatrix()
                elif i == 2:
                    glPushMatrix()
                    # correcting position
                    if self.isAssembled:
                        glTranslated(0.5, 0, -0.3)
                    else:
                        glTranslated(2, 0, -0.3)
                    glRotated(90, 0, 1, 0)
                    glEnable(GL_COLOR_MATERIAL)
                    # coloring
                    glColor3d(
                        self.staticColor[0], self.staticColor[1], self.staticColor[2])
                    self._drawModel(self.models[i])
                    glDisable(GL_COLOR_MATERIAL)
                    glPopMatrix()
        else:
            # TODO insert packaged model
            pass

    # animate the
    def assemble(self):
        pass

    # This Methods gets model data and creates a 3D model
    def _drawModel(self, model):
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
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()
        glPopMatrix()

    def _hexToRGB(self, hex):
        colorRGBBin = tuple(int(hex[i+1:i+3], 16) for i in (0, 2, 4))
        colorRGBFloat = tuple(color/255 for color in colorRGBBin)
        return colorRGBFloat

    # Setter for state values
    def setAssembled(self, isAssembled):
        self.isAssembled = isAssembled

    def setPackaged(self, isPackaged):
        self.isPackaged = isPackaged

    def setColor(self, color):
        self.color = color
