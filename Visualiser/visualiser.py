"""
Filename: visualiser.py
Version name: 0.1, 2021-05-21
Short description: Module for visualisation output

(C) 2003-2021 IAS, Universitaet Stuttgart

"""


from package import PackageModel
import pywavefront
import OpenGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import sys
sys.path.append('.')
sys.path.append('..')


class Visualiser(object):

    def __init__(self):
        self.modelName = 'IAS-Logo'
        self.model = None
        # resolution to render
        self.display = (1280, 720)
        # visualisation params
        self.isAssemled = True
        self.isPackaged = False
        self.paintColor = "#00fcef"
        self.color = '#CCCCCC'
        self.task = 'package'
        self._initPygame()

    """
    Animations
    """

    def displayIdle(self):
        pass

    def displayIncomingCarrier(self):
        print("[VISUALISATION] Display incoming carrier")
        hasReachedTarget = False
        self.loadModel()
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
            self.animateModel()

            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)
            pygame.display.flip()
            pygame.time.wait(40)
        return True

    def displayOutgoingCarrier(self):
        print("[VISUALISATION] Display outgoing carrier")
        hasReachedTarget = False
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
            pygame.display.flip()
            pygame.time.wait(40)
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
        isColored = False
        timeStart = time.time()
        self.loadModel()
        self.model.setAlpha(0)
        self.model.setPaintColor(self.paintColor)
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
            pygame.display.flip()
            pygame.time.wait(40)
        self.model.setColor(self.paintColor)
        return True

    def unpackage(self):
        print("[VISUALISATION] Display painting process")
        isFinished = False
        timeStart = time.time()
        self.model.setPackaged(False)
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
            pygame.display.flip()
            pygame.time.wait(40)

        return True

    def package(self):
        print("[VISUALISATION] Display painting process")
        isFinished = False
        timeStart = time.time()

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
            pygame.display.flip()
            pygame.time.wait(40)
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

        glEnable(GL_LIGHTING)
        glLight(GL_LIGHT0, GL_POSITION,  (0, 1, -7, 0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (2, 2, 2, 1))
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

    def setModelName(self, name):
        self.modelName = name


if __name__ == "__main__":
    # testcode to run
    from iaslogo import IASModel
    visualiser = Visualiser()
    visualiser.displayIncomingCarrier()
    input("Continue")
    visualiser.displayProcessVisualisation()
    input("Continue")
    visualiser.displayOutgoingCarrier()
    pygame.quit()
    quit()
