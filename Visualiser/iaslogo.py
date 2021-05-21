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

from .visualiser import Visualiser


class IASModel(object):
    def __init__(self):
        self.modelNames = [
            '3dmodels/IAS_Letter_I.obj',
            '3dmodels/IAS_Letter_A.obj',
            '3dmodels/IAS_Letter_S.obj'
        ]
        self.scaledSize = 1

    def model(self, isAssembled, color, isPackaged):
        models = []
        if not isPackaged:
            for model in self.modelNames:
                models.append(pywavefront.Wavefront(model, collect_faces=True))
            glBegin()
            for model in models:
                self._drawModel(self, model)
                if not isAssembled:
                    # TODO shift parts so it looks disassembled
                    pass
                if color != "#000000":
                    # Convert color to RGB
                    colorRGB = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                    # Colorize
                    glColor3fv(colorRGB)
                    pass
            glEnd()
        else:
            # TODO insert packaged model
            pass

    def assemble(self, color):
        models = []
        for model in self.modelNames:
            models.append(pywavefront.Wavefront(model, collect_faces=True))
            glBegin()
            for i in range(len(models)):
                self._drawModel(self, models[i])
            glEnd()

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
