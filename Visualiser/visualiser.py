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
import time

from .iaslogo import IASModel


class Visualiser(object):

    def __init__(self):
        self.modelName = 'IAS-Logo'
        self.model = None
        # resolution to render
        self.display = (1280, 720)
        # visualisation params
        self.isAssemled = False
        self.isPackaged = False
        self.color = '#000000'
        self.task = 'generic'

    def displayIdle(self):
        pass

    def displayIncomingCarrier(self):
        self._initPygame()
        self.loadModel(self.modelName)
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
            # Move model 1 unit on x-axis
            matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
            if matrix[3][0] != 10:
                glTranslatef(1, 0, 0)
            else:
                hasReachedTarget = True
            self.model
            pygame.display.flip()
            pygame.time.wait(40)

    def displayOutgoingCarrier(self):
        self._initPygame()
        self.loadModel('IAS-Logo')
        hasReachedTarget = False

        # shift model to stopper position
        glTranslatef(10, 0, 0)

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
            # Move model 1 unit on x-axis
            matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
            if matrix[3][0] != 20:
                glTranslatef(1, 0, 0)
            else:
                hasReachedTarget = True
            self.model
            pygame.display.flip()
            pygame.time.wait(40)

    def displayProcessVisualisation(self):
        pass

    def loadModel(self):
        if self.modelName == 'IAS-Logo':
            self.model = IASModel().model(isAssembled=self.isAssemled,
                                          color=self.color, isPackaged=self.isPackaged)
        else:
            # IAS logo is standard model to be loaded
            self.model = IASModel().model(isAssembled=self.isAssemled,
                                          color=self.color, isPackaged=self.isPackaged)
        return

    def _initPygame(self):
        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        # set Camera perspektive
        gluPerspective(60, (self.display[0] / self.display[1]), 1, 500.0)
        glTranslatef(0.0, 0.0, -10)
        # enable fl features
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glShadeModel(GL_FLAT)
        glEnable(GL_COLOR_MATERIAL)

    # setter for state params
    def setIsAssembled(self, isAssembled):
        self.isAssemled = isAssembled

    def setIsPackaged(self, isPackaged):
        self.isPackaged = isPackaged

    def setColor(self, color):
        self.color = color

    def setModelName(self, name):
        self.modelName = name


if __name__ == "__main__":
    # Testumgebung
    visualiser = Visualiser()
    visualiser.displayIncomingCarrier()
    visualiser.displayOutgoingCarrier()
