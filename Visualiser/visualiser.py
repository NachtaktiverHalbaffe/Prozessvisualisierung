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
        self.isAssemled = False
        self.isPackaged = False
        self.color = '#000000'
        self.task = 'generic'
        self._initPygame()

    def displayIdle(self):
        pass

    def displayIncomingCarrier(self):
        hasReachedTarget = False
        self.loadModel()
        while not hasReachedTarget:
            print("inside drawing loop")
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
            print(matrix[3][0])
            if matrix[3][0] < -1:
                glTranslatef(0.05, 0, 0)

            else:
                hasReachedTarget = True
            self.animateModel()
            pygame.display.flip()
            pygame.time.wait(40)

    def displayOutgoingCarrier(self):
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
            # Move model 1 unit on x-axis
            matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
            print(matrix[3][0])
            if matrix[3][0] < 7:
                glTranslatef(0.05, 0, 0)

            else:
                hasReachedTarget = True
            self.animateModel()
            pygame.display.flip()
            pygame.time.wait(40)

    def displayProcessVisualisation(self):
        pass

    def loadModel(self):
        if self.modelName == 'IAS-Logo':
            self.model = IASModel()
        else:
            # IAS logo is standard model to be loaded
            self.model = IASModel()

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
        # set Camera perspektive
        gluPerspective(60, (self.display[0] / self.display[1]), 1, 500.0)

        glTranslatef(-12, -2, -5)
        glRotatef(70, 1, 0, 0)

        # enable fl features
        glEnable(GL_DEPTH_TEST)
        #glClearColor(1.0, 1.0, 1.0, 0.0)
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
    from iaslogo import IASModel
    visualiser = Visualiser()
    visualiser.displayIncomingCarrier()
    input("Continue")
    visualiser.displayOutgoingCarrier()
    pygame.quit()
    quit()
