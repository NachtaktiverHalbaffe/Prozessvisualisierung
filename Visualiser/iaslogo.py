"""
Filename: iaslogo.py
Version name: 0.1, 2021-05-21
Short description: model object of ias logo

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
import pywavefront
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from model import Model


class IASModel(Model):
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

    # animate the assemble task
    def assemble(self):
        pass
