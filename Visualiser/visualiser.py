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

        # check user closed the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                glDeleteTextures(texture_id)
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    glDeleteTextures(texture_id)
                    pygame.quit()
                    quit()
        if self.isKilled:
            glDeleteTextures(texture_id)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        skybox.ground()
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)
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
            # check user closed the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    glDeleteTextures(texture_id)
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        glDeleteTextures(texture_id)
                        pygame.quit()
                        quit()
            if self.isKilled:
                glDeleteTextures(texture_id)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
            # Move model 1 unit on x-axis
            matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
            if matrix[3][0] < -3:
                glTranslatef(0.05, 0, 0)

            else:
                hasReachedTarget = True
            skybox.ground()
            self.animateModel()
            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)

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
            # check user closed the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
            # check if visualiser is killed
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
            # Move model 0.05 unit on x-axis
            matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
            if matrix[3][0] < 7:
                glTranslatef(0.05, 0, 0)

            else:
                hasReachedTarget = True
            self.animateModel()
            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)
            skybox.ground()
            pygame.display.flip()
            pygame.time.wait(40)

        glDeleteTextures(texture_id)
        return True

    def displayProcessVisualisation(self):
        if self.task == 'assemble':
            self.model.assemble()
        elif self.task == 'color':
            self.paint()
        elif self.task == 'package':
            self.package()
        elif self.task == 'unpackage':
            self.unpackage()
        elif self.task == 'generic':
            self.model.generic()
        return True

    def paint(self):
        print("[VISUALISATION] Display painting process")
        skybox = Skybox()
        texture_id = skybox.loadTexture()
        isColored = False
        timeStart = time.time()
        self.loadModel()
        self.model.setAlpha(0)
        self.model.setPaintColor(self.paintColor)

        # drawing loop
        while not isColored:
            # check user closed the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            # check if visualiser is killed

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
            # Move model 0.05 unit on x-axis
            currentTime = time.time() - timeStart
            if currentTime < 5:
                self.model.setAlpha(0.2 * currentTime)
                self.animateModel()
            else:
                isColored = True
                self.model.setAlpha(1)
                self.animateModel()
            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)
            skybox.ground()
            pygame.display.flip()
            pygame.time.wait(40)

        self.model.setColor(self.paintColor)
        glDeleteTextures(texture_id)
        return True

    def unpackage(self):
        print("[VISUALISATION] Display painting process")
        skybox = Skybox()
        texture_id = skybox.loadTexture()
        isFinished = False
        timeStart = time.time()
        self.model.setPackaged(False)

        # drawing loop
        while not isFinished:
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
            # Move model 0.05 unit on x-axis
            currentTime = time.time() - timeStart
            if currentTime < 5:
                PackageModel().unpackage(currentTime)
                self.animateModel()
            else:
                isFinished = True
                PackageModel().unpackage(currentTime)
                self.animateModel()
            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)
            skybox.ground()
            pygame.display.flip()
            pygame.time.wait(40)

        glDeleteTextures(texture_id)
        return True

    def package(self):
        print("[VISUALISATION] Display painting process")
        isFinished = False
        timeStart = time.time()
        skybox = Skybox()
        texture_id = skybox.loadTexture()

        # drawing loop
        while not isFinished:
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
            # Move model 0.05 unit on x-axis
            currentTime = time.time() - timeStart
            if currentTime < 5:
                PackageModel().package(currentTime)
                self.animateModel()
            else:
                isFinished = True
                PackageModel().package(currentTime)
                self.animateModel()
            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)
            skybox.ground()
            pygame.display.flip()
            pygame.time.wait(40)

        glDeleteTextures(texture_id)
        self.model.setPackaged(True)
        return True

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

    def _initPygame(self):
        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        # set camera perspektive
        gluPerspective(60, (self.display[0] / self.display[1]), 1, 500.0)
        glTranslatef(-12, -2, -5)
        glRotatef(60, 1, 0, 0)
        # enable gl features
        glEnable(GL_DEPTH_TEST)
        #glClearColor(1.0, 1.0, 1.0, 0.0)
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
