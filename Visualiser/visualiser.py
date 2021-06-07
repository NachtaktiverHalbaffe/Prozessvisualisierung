"""
Filename: visualiser.py
Version name: 0.1, 2021-05-21
Short description: Module for visualisation output

(C) 2003-2021 IAS, Universitaet Stuttgart

"""

import pywavefront
import OpenGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from .skyboy import Skybox
from .package import PackageModel
from .iaslogo import IASModel
import time
import sys
sys.path.append('.')
sys.path.append('..')


class Visualiser(object):

    def __init__(self):
        self.isKilled = False
        self.modelName = 'IAS-Logo'
        self.model = None
        # resolution to render
        self.display = (1280, 720)
        # visualisation params
        self.isAssemled = True
        self.isPackaged = False
        self.paintColor = "#00fcef"
        self.color = '#CCCCCC'
        self.task = 'color'

    """
    Animations
    """

    def displayIdle(self):
        print("[VISUALISATION] Display idle")
        skybox = Skybox()
        texture_id = skybox.loadTexture()

        # drawing loop
        while not self.isKilled:
            # check user closed the game
            self._eventLoop(texture_id)
            if self.isKilled:
                glDeleteTextures(texture_id)
                break

            self._enableGLFeatures(True)
            skybox.ground()
            self._enableGLFeatures(False)
            pygame.display.flip()
            pygame.time.wait(40)

        return True

    def displayIncomingCarrier(self):
        print("[VISUALISATION] Display incoming carrier")
        skybox = Skybox()
        texture_id = skybox.loadTexture()
        hasReachedTarget = False
        self.loadModel()
        # drawing loop
        while not hasReachedTarget:
            # check events and params
            self._eventLoop(texture_id)
            if self.isKilled:
                glDeleteTextures(texture_id)
                break

            self._enableGLFeatures(True)
            # Move model 1 unit on x-axis
            matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
            if matrix[3][0] < -3:
                glTranslatef(0.1, 0, 0)

            else:
                hasReachedTarget = True

            # drawing
            skybox.ground()
            self.animateModel()
            self._enableGLFeatures(False)

            pygame.display.flip()
            pygame.time.wait(40)

        glDeleteTextures(texture_id)
        return True

    def displayOutgoingCarrier(self):
        print("[VISUALISATION] Display outgoing carrier")
        skybox = Skybox()
        texture_id = skybox.loadTexture()
        hasReachedTarget = False

        # drawing loop
        while not hasReachedTarget:
            self._eventLoop(texture_id)

            self._enableGLFeatures(True)
            # Move model 0.05 unit on x-axis
            matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
            if matrix[3][0] < 7:
                glTranslatef(0.1, 0, 0)
            else:
                hasReachedTarget = True
            self.animateModel()
            self._enableGLFeatures(False)
            skybox.ground()
            pygame.display.flip()
            pygame.time.wait(40)

        glDeleteTextures(texture_id)
        return True

    def displayProcessVisualisation(self):
        print("[VISUALISER] Display processvisualisation")
        DRY_TIME = 3
        skybox = Skybox()
        texture_id = skybox.loadTexture()
        finished = False
        timeStart = time.time()

        while not finished:
            self._eventLoop(texture_id)
            self._enableGLFeatures(True)
            currentTime = time.time() - timeStart
            if self.task == 'assemble':
                if currentTime < 5:
                    self.model.assemble(currentTime)
                else:
                    finished = True
                    self.isAssemled = True
                    self.model.assemble(currentTime)
            elif self.task == 'color':
                if currentTime < 5:
                    self.paint(currentTime)
                elif currentTime < 5 + DRY_TIME:
                    self.paint(5)
                else:
                    finished = True
                    self.model.setColor(self.paintColor)
                    self.paint(currentTime)
            elif self.task == 'package':
                if currentTime < 5:
                    self.package(currentTime)
                else:
                    finished = True
                    self.package(currentTime)
                    self.isPackaged = True
            elif self.task == 'unpackage':
                if currentTime < 5:
                    self.unpackage(currentTime)
                else:
                    finished = True
                    self.unpackage(currentTime)
                    self.isPackaged = False
            elif self.task == 'generic':
                if currentTime < 5:
                    self.generic(currentTime)
                else:
                    finished = True
                    self.generic(currentTime)
            skybox.ground()
            self._enableGLFeatures(False)
            pygame.display.flip()
            pygame.time.wait(40)
        return True

    def paint(self, currentTime):
        self.model.setAlpha(0.2 * currentTime)
        self.animateModel()

    def unpackage(self, currentTime):
        PackageModel().unpackage(currentTime)
        self.animateModel()

    def package(self, currentTime):
        PackageModel().package(currentTime)
        self.animateModel()

    """
    utils
    """

    def loadModel(self):
        if self.modelName == 'IAS-Logo':
            self.model = IASModel()
            self.model.setAssembled(self.isAssemled)
            self.model.setPackaged(self.isPackaged)
            self.model.setColor(self.color)
        else:
            # IAS logo is standard model to be loaded
            self.model = IASModel()
            self.model.setAssembled(self.isAssemled)
            self.model.setPackaged(self.isPackaged)
            self.model.setColor(self.color)

    def animateModel(self):
        if self.modelName == 'IAS-Logo':
            self.model.animateModel()
        else:
            # IAS logo is standard model to be loaded
            self.model.animateModel()
        return

    def initPygame(self):
        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        # set camera perspektive
        gluPerspective(60, (self.display[0] / self.display[1]), 1, 500.0)
        glTranslatef(-12, -2, -5)
        glRotatef(60, 1, 0, 0)
        # enable gl features
        glEnable(GL_DEPTH_TEST)
        # glClearColor(1.0, 1.0, 1.0, 0.0)
        glShadeModel(GL_FLAT)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendEquation(GL_FUNC_ADD)

        glEnable(GL_LIGHTING)
        glLight(GL_LIGHT0, GL_POSITION,  (0, 1, -7, 0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (2, 2, 2, 1))
        glLight(GL_LIGHT0, GL_POSITION, (0, .5, 1))
        glEnable(GL_COLOR_MATERIAL)

    def _enableGLFeatures(self, isEnabled):
        if isEnabled:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        elif not isEnabled:
            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)

    def _eventLoop(self, texture_id):
        # check events for closing
        for event in pygame.event.get():
            # Quit event (pressing close button on window)
            if event.type == pygame.QUIT:
                glDeleteTextures(texture_id)
                pygame.quit()
                quit()
            # escape pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    glDeleteTextures(texture_id)
                    pygame.quit()
                    quit()

    """
    Setter for state parameter
    """

    def setIsAssembled(self, isAssembled):
        self.isAssemled = isAssembled

    def setIsPackaged(self, isPackaged):
        self.isPackaged = isPackaged

    def setColor(self, color):
        self.color = color

    def setPaintColor(self, paintColor):
        self.paintColor = paintColor

    def setModelName(self, name):
        self.modelName = name

    def setTask(self, task):
        self.task = task

    def killVisualiser(self):
        self.isKilled = True

    def reviveVisualiser(self):
        self.isKilled = False


if __name__ == "__main__":
    # testcode to run
    from .iaslogo import IASModel
    visualiser = Visualiser()
    visualiser.displayIncomingCarrier()
    input("Continue")
    visualiser.displayProcessVisualisation()
    input("Continue")
    visualiser.displayOutgoingCarrier()
    # visualiser.displayIdle()
    pygame.quit()
    quit()
