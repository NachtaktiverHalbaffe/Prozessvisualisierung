"""
Filename: iaslogo.py
Version name: 0.1, 2021-05-21
Short description: model object of ias logo

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
import pygame
import pywavefront
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from .skyboy import Skybox
import time
import os

from .model import Model
from .package import PackageModel
from api.constants import CWP_DIR


class IASModel(Model):
    def __init__(self):
        self.isAssembled = False
        self.isPackaged = False
        self.staticColor = (0.007, 0.175, 0.546)
        self.color = '#CCCCCC'
        self.paintColor = '#000000'
        self.alpha = 1
        # os.chdir("..")
        cwd = CWP_DIR
        self.modelNames = [
            cwd + '/visualiser/3dmodels/IAS_Letter_I_FINAL.obj',
            cwd + '/visualiser/3dmodels/IAS_Letter_A_FINAL.obj',
            cwd + '/visualiser/3dmodels/IAS_Letter_S_FINAL.obj'
        ]
        self.scaledSize = 4
        self.models = []
        for model in self.modelNames:
            self.models.append(pywavefront.Wavefront(
                model, collect_faces=True))

    """
    Loading and drawing models and costum animations
    """
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
                    self._drawModel(self.models[i], self.staticColor)
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
                    if self.paintColor != '#000000':
                        paintColorRGB = self._hexToRGB(self.paintColor)
                        colorRGB = tuple(
                            float(colorRGB[i] * (1-self.alpha)) for i in range(len(colorRGB)))
                        paintColorRGB = tuple(
                            float(paintColorRGB[i] * self.alpha) for i in range(len(paintColorRGB)))
                        color = tuple(abs(float(colorRGB[i]+ paintColorRGB[i])) for i in range(len(colorRGB)))
                        self._drawModel(self.models[i], color)
                    elif self.paintColor == '#000000':
                        glColor3d(colorRGB[0], colorRGB[1],
                                  colorRGB[2])
                        self._drawModel(self.models[i], colorRGB)  
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
                    self._drawModel(self.models[i], self.staticColor)
                    glDisable(GL_COLOR_MATERIAL)
                    glPopMatrix()
        else:
            PackageModel().animateModel()
            pass

    # animate the assemble task
    def assemble(self, time):
        for i in range(len(self.models)):
            if i == 0:
                # correcting position
                glPushMatrix()
                glTranslated(-3+0.56*time, 0, 0)
                glRotated(90, 0, 1, 0)
                glScaled(0.75, 0.75, 0.75)
                # coloring
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
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
                self._drawModel(self.models[i], colorRGB)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            elif i == 2:
                glPushMatrix()
                # correcting position
                glTranslated(2-0.3*time, 0, -0.3)
                glRotated(90, 0, 1, 0)
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()

    # animates the generic task
    def generic(self, time):
        for i in range(len(self.models)):
            if i == 0:
                glPushMatrix()
                glTranslated(-0.2-0.56*time, 0, 0)
                glRotated(90, 0, 1, 0)
                glScaled(0.75, 0.75, 0.75)
                # coloring
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            elif i == 1:
                glPushMatrix()
                glRotated(90, 0, 1, 0)
                # coloring depending if piece was painted or not
                glEnable(GL_COLOR_MATERIAL)
                if self.color != '#000000':
                    colorRGB = self._hexToRGB(self.color)
                else:
                    colorRGB = (1, 1, 1)
                self._drawModel(self.models[i], colorRGB)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            elif i == 2:
                glPushMatrix()
                glTranslated(0.5 + 0.3*time, 0, -0.3)
                glRotated(90, 0, 1, 0)
                glEnable(GL_COLOR_MATERIAL)
                # coloring
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
