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
import time

from model import Model


class IASModel(Model):
    def __init__(self):
        self.isAssembled = False
        self.isPackaged = False
        self.staticColor = (0.007, 0.175, 0.546)
        self.color = '#CCCCCC'
        self.paintColor = '#000000'
        self.alpha = 1
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
                    if self.paintColor != '#000000':
                        paintColorRGB = self._hexToRGB(self.paintColor)
                    if self.paintColor == '#000000':
                        glColor3d(colorRGB[0], colorRGB[1],
                                  colorRGB[2])
                    else:
                        colorRGB = tuple(
                            float(colorRGB[i] * 1-self.alpha) for i in range(len(colorRGB)))
                        paintColorRGB = tuple(
                            float(paintColorRGB[i] * self.alpha) for i in range(len(paintColorRGB)))
                        print(paintColorRGB)
                        glColor3d(colorRGB[0] + paintColorRGB[0], colorRGB[1] + paintColorRGB[1],
                                  colorRGB[2] + paintColorRGB[2])
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
        print("[VISUALISATION] Assemble working Piece")
        hasFinished = False
        timeStart = time.time()
        while not hasFinished:
            # check user closed the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
            currentTime = time.time() - timeStart
            if currentTime < 5:
                self._animationAssemble(currentTime)
            else:
                hasFinished = True
                self._animationAssemble(currentTime)
            pygame.display.flip()
            pygame.time.wait(40)
        self.isAssembled = True
        return True

    # animates the generic task
    def generic(self):
        print("[VISUALISATION] Generic Task: Check working Piece")
        hasFinished = False
        timeStart = time.time()
        while not hasFinished:
            # check user closed the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
            currentTime = time.time() - timeStart
            if currentTime < 2:
                self._animationAssemble(currentTime)
            else:
                hasFinished = True
                self._animationAssemble(currentTime)

            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)
            pygame.display.flip()
            pygame.time.wait(40)
        return True

    def _animationAssemble(self, time):
        for i in range(len(self.models)):
            if i == 0:
                # correcting position
                glPushMatrix()
                glTranslated(-3+0.56*time, 0, 0)
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
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            elif i == 2:
                glPushMatrix()
                # correcting position
                glTranslated(2-0.3*time, 0, -0.3)
                glRotated(90, 0, 1, 0)
                glEnable(GL_COLOR_MATERIAL)
                # coloring
                glColor3d(
                    self.staticColor[0], self.staticColor[1], self.staticColor[2])
                self._drawModel(self.models[i])
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()

    def _flipAnimation(self, time):
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
