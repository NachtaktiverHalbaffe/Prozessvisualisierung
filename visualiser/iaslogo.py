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
        # static color(s) of parts of the 3d model ("IAS blue")
        self.staticColor = (0.007, 0.175, 0.546)
        # state of workingpiece which is passed down from
        # processvisualisation
        self.isAssembled = False
        self.isPackaged = False
        self.color = '#CCCCCC'
        self.paintColor = '#000000'
        self.alpha = 1
        # path to the .obj-files of the model
        cwd = CWP_DIR
        self.modelNames = [
            cwd + '/visualiser/3dmodels/IAS_Letter_I_FINAL.obj',
            cwd + '/visualiser/3dmodels/IAS_Letter_A_FINAL.obj',
            cwd + '/visualiser/3dmodels/IAS_Letter_S_FINAL.obj'
        ]
        # "master" scale to all models
        self.scaledSize = 4
        # load .obj files
        self.models = []
        for model in self.modelNames:
            self.models.append(pywavefront.Wavefront(
                model, collect_faces=True))

    """
    Drawing models and costum animations
    """

    # draws model with right state and corrects position of submodels of the whole 3D-Model,
    # because parts of models can initially be on wrong position depending of the .obj-file
    def drawModel(self):
        # only draw model if it isnt packed
        if not self.isPackaged:
            for i in range(len(self.models)):
                if i == 0:
                    # correcting position. Be shure to encapsulate all corrections
                    # beetween glPushMatrix() amd glPopMatrix() so the corrections
                    # are applied to the model and not to the whole scene
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
                    # correcting position. Be shure to encapsulate all corrections
                    # beetween glPushMatrix() amd glPopMatrix() so the corrections
                    # are applied to the model and not to the whole scene
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
                        color = tuple(
                            abs(float(colorRGB[i] + paintColorRGB[i])) for i in range(len(colorRGB)))
                        self._drawModel(self.models[i], color)
                    elif self.paintColor == '#000000':
                        glColor3d(colorRGB[0], colorRGB[1],
                                  colorRGB[2])
                        self._drawModel(self.models[i], colorRGB)
                    glDisable(GL_COLOR_MATERIAL)
                    glPopMatrix()
                elif i == 2:
                    glPushMatrix()
                    # correcting position. Be shure to encapsulate all corrections
                    # beetween glPushMatrix() amd glPopMatrix() so the corrections
                    # are applied to the model and not to the whole scene
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
            # draw model of package
            PackageModel().drawModel()

    # animate the assemble task
    def assemble(self, time):
        for i in range(len(self.models)):
            if i == 0:
                glPushMatrix()
                # move letter towards the middle letter
                glTranslated(-3+0.56*time, 0, 0)
                glRotated(90, 0, 1, 0)
                glScaled(0.75, 0.75, 0.75)
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            elif i == 1:
                glPushMatrix()
                glRotated(90, 0, 1, 0)
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
                # move letter towards the middle letter
                glTranslated(2-0.3*time, 0, -0.3)
                glRotated(90, 0, 1, 0)
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()

    # animates the generic task. In this case its a disassembly of the logo
    def generic(self, time):
        for i in range(len(self.models)):
            if i == 0:
                glPushMatrix()
                # move letter away from the middle letter
                glTranslated(-0.2-0.56*time, 0, 0)
                glRotated(90, 0, 1, 0)
                glScaled(0.75, 0.75, 0.75)
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            elif i == 1:
                glPushMatrix()
                glRotated(90, 0, 1, 0)
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
                # move letter away from the middle letter
                glTranslated(0.5 + 0.3*time, 0, -0.3)
                glRotated(90, 0, 1, 0)
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
