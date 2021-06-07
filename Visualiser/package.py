"""
Filename: ipackage.py
Version name: 0.1, 2021-05-25
Short description: model object of package

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
from model import Model
import pygame
import pywavefront
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import sys
sys.path.append('.')
sys.path.append('..')


class PackageModel(Model):
    def __init__(self):
        self.isAssembled = True
        self.isPackaged = False
        self.staticColor = (0.62740, 0.3215, 0.176)
        self.color = '#cd853f'
        self.paintColor = '#000000'
        self.alpha = 1
        # self.modelNames = [
        #     '3dmodels/PACKAGE_BOTTOM_FINAL.obj',
        #     '3dmodels/PACKAGE_LEFT_SIDE_FINAL.obj',
        #     '3dmodels/PACKAGE_TOP_SIDE_FINAL.obj',
        #     '3dmodels/PACKAGE_RIGHT_SIDE_FINAL.obj',
        #     '3dmodels/PACKAGE_BOTTOM_SIDE_FINAL.obj',
        #     '3dmodels/PACKAGE_TOP_FINAL.obj',
        # ]
        self.modelNames = [
            '3dmodels/PACKAGE_TOP_FINAL.obj',
            '3dmodels/PACKAGE_BOX_FINAL.obj'
        ]
        self.scaledSize = 7
        self.models = []
        for model in self.modelNames:
            self.models.append(pywavefront.Wavefront(
                model, collect_faces=True))

    """
    Loading and drawing models and costum animations
    """
    # draws model with right state

    # def animateModel(self):
    #     for i in range(len(self.models)):
    #         if i == 0:
    #             # correcting position
    #             glPushMatrix()
    #             glTranslated(6.5, 0.2, -3)
    #             glRotated(90, 0, 1, 0)
    #             glRotated(90, 0, 1, 0)
    #             glScaled(0.99, 1, 1)
    #             # coloring
    #             glEnable(GL_COLOR_MATERIAL)
    #             glColor3d(
    #                 self.staticColor[0], self.staticColor[1], self.staticColor[2])
    #             self._drawModel(self.models[i])
    #             glDisable(GL_COLOR_MATERIAL)
    #             glPopMatrix()
    #         elif i == 1:
    #             glPushMatrix()
    #             # correcting position
    #             glScaled(0.25, 0.25, 0.65)
    #             glTranslated(-1.6, 0, -0.50)
    #             # glRotated(90, 0, 1, 0)
    #             # glRotated(90, 0, 1, 0)
    #             # glRotated(90, 1, 0, 0)

    #             # coloring depending if piece was painted or not
    #             glEnable(GL_COLOR_MATERIAL)
    #             glColor3d(
    #                 self.staticColor[0], self.staticColor[1], self.staticColor[2])
    #             self._drawModel(self.models[i])
    #             glDisable(GL_COLOR_MATERIAL)
    #             glPopMatrix()
    #         elif i == 2:
    #             glPushMatrix()
    #             # correcting position
    #             glScaled(0.65, 0.4, 0.475)
    #             glTranslated(11.75, 0, 0.25)
    #             glRotated(90, 0, 1, 0)
    #             glEnable(GL_COLOR_MATERIAL)
    #             # coloring
    #             glColor3d(
    #                 self.staticColor[0], self.staticColor[1], self.staticColor[2])
    #             self._drawModel(self.models[i])
    #             glDisable(GL_COLOR_MATERIAL)
    #             glPopMatrix()
    #         elif i == 3:
    #             glPushMatrix()
    #             # correcting position
    #             glTranslated(-0.1, 0, 2.5)
    #             glRotated(90, 0, 1, 0)
    #             glRotated(90, 1, 0, 0)
    #             glScaled(0.5, 1, 0.345)
    #             glEnable(GL_COLOR_MATERIAL)
    #             # coloring
    #             glColor3d(
    #                 self.staticColor[0], self.staticColor[1], self.staticColor[2])
    #             self._drawModel(self.models[i])
    #             glDisable(GL_COLOR_MATERIAL)
    #             glPopMatrix()
    #         elif i == 4:
    #             glPushMatrix()
    #             # correcting position
    #             glTranslated(-1, 0, -0.3)
    #             #glRotated(90, 0, 0, -1)
    #             glScaled(1, 0.345, 0.5)
    #             glEnable(GL_COLOR_MATERIAL)
    #             # coloring
    #             glColor3d(
    #                 self.staticColor[0], self.staticColor[1], self.staticColor[2])
    #             self._drawModel(self.models[i])
    #             glDisable(GL_COLOR_MATERIAL)
    #             glPopMatrix()
    #         elif i == 5:
    #             glPushMatrix()
    #             # correcting position
    #             glTranslated(-0.75, -2.2, -0.28)
    #             #glRotated(90, 0, 1, 0)
    #             glScaled(1, 1, 1.1)
    #             glEnable(GL_COLOR_MATERIAL)
    #             # coloring
    #             glColor3d(
    #                 self.staticColor[0], self.staticColor[1], self.staticColor[2])
    #             self._drawModel(self.models[i])
    #             glDisable(GL_COLOR_MATERIAL)
    #             glPopMatrix()

    # draws model with right state

    def animateModel(self):
        for i in range(len(self.models)):
            if i == 0:
                # correcting position
                glPushMatrix()
                glTranslated(-1.5, -0.5, 0)
                glScaled(1.1, 0.5, 1.45)
                # coloring
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            if i == 1:
                glPushMatrix()
                # correcting position
                glTranslated(-1.5, 0, 0)
                glScaled(1.1, 0.4, 1.5)
                # coloring depending if piece was painted or not
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()

    # animate the assemble task

    def package(self, time):
        for i in range(len(self.models)):
            if i == 0:
                # correcting position
                glPushMatrix()
                glTranslated(-1.5, -0.5, 0)
                glScaled(1.1, 0.5, 1.5)
                glRotated(90, -1, 0, 0)
                glRotated(18 * time, 1, 0, 0)
                # coloring
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            if i == 1:
                glPushMatrix()
                # correcting position
                glTranslated(-1.5, 0, 0)
                glScaled(1.1, 0.08 * time, 1.5)
                # coloring depending if piece was painted or not
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
        return True

    # animates the generic task
    def unpackage(self, time):
        for i in range(len(self.models)):
            if i == 0:
                # correcting position
                glPushMatrix()
                glTranslated(-1.5, -0.5, 0)
                glScaled(1.1, 0.5, 1.5)
                glRotated(18 * time, -1, 0, 0)
                # coloring
                glEnable(GL_COLOR_MATERIAL)
                if time < 5:
                    self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            if i == 1:
                glPushMatrix()
                # correcting position
                glTranslated(-1.5, 0, 0)
                glScaled(1.1, 0.38 - 0.08 * time, 1.5)
                # coloring depending if piece was painted or not
                glEnable(GL_COLOR_MATERIAL)
                if time < 5:
                    self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
        return True
