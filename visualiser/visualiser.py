"""
Filename: visualiser.py
Version name: 0.1, 2021-05-21
Short description: Module for visualisation output

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
import pygame  # nopep8
import logging  # nopep8
import time  # nopep8
import sys  # nopep8
from pygame.locals import *  # nopep8
from OpenGL.GL import *  # nopep8
from OpenGL.GLU import *  # nopep8
from threading import Thread  # nopep8
sys.path.append('.')  # nopep8
sys.path.append('..')  # nopep8

from .skyboy import Skybox  # nopep8
from .package import PackageModel  # nopep8
from .iaslogo import IASModel  # nopep8
from .timer import Timer  # nopep8
from api.constants import BASE_LEVEL_HEIGHT, STREAM_HANDLER, FILE_HANDLER_PV, FILE_HANDLER_ERROR  # nopep8
from carrierdetection.carrierdetection import CarrierDetection  # nopep8


class Visualiser(object):

    def __init__(self):
        self.isKilled = False
        self.movSpeed = 0.2
        # 3d model params
        self.modelName = 'IAS-Logo'
        self.model = None
        # resolution to render
        self.display = (1920, 1080)
        # visualisation params
        self.isAssembled = True
        self.isPackaged = False
        self.paintColor = "#00fcef"
        self.color = '#CCCCCC'
        self.task = 'color'

        # setup logger
        self.logger = logging.getLogger("visualiser")
        self.logger.setLevel(logging.INFO)
        self.errorLogger = logging.getLogger("error")
        self.errorLogger.setLevel(logging.warning)
        # add logger handler to logger
        self.logger.handlers = []
        self.logger.addHandler(STREAM_HANDLER)
        self.logger.addHandler(FILE_HANDLER_PV)
        self.errorLogger.handlers = []
        self.errorLogger.addHandler(STREAM_HANDLER)
        self.errorLogger.addHandler(FILE_HANDLER_ERROR)

    """
    Animations
    """

    def displayIdle(self):
        self.logger.info("[VISUALISATION] Display idle")
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
            # pygame.time.wait(40)

        return True

    def displayIdleStill(self):
        self.logger.info("[VISUALISATION] Display idle")
        skybox = Skybox()
        texture_id = skybox.loadTexture()

        # check user closed the game
        self._eventLoop(texture_id)
        self._enableGLFeatures(True)
        skybox.ground()
        self._enableGLFeatures(False)
        pygame.display.flip()
        pygame.time.wait(40)

        return True

    def displayIncomingCarrier(self):
        self.logger.info("[VISUALISATION] Display incoming carrier")
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
            # Move model on x-axis
            matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
            if matrix[3][0] < -3:
                glTranslatef(self.movSpeed, 0, 0)

            else:
                hasReachedTarget = True

            # drawing
            skybox.ground()
            self.drawModel()
            self._enableGLFeatures(False)

            pygame.display.flip()
            pygame.time.wait(40)

        glDeleteTextures(texture_id)
        return True

    def displayOutgoingCarrier(self):
        self.logger.info("[VISUALISATION] Display outgoing carrier")
        skybox = Skybox()
        texture_id = skybox.loadTexture()
        hasReachedTarget = False

        # drawing loop
        while not hasReachedTarget:
            self._eventLoop(texture_id)

            self._enableGLFeatures(True)
            # Move model 0.05 unit on x-axis
            matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
            if matrix[3][0] < 9:
                glTranslatef(self.movSpeed, 0, 0)
            else:
                hasReachedTarget = True
            self.drawModel()
            self._enableGLFeatures(False)
            skybox.ground()
            pygame.display.flip()
            pygame.time.wait(40)

        glDeleteTextures(texture_id)
        return True

    def displayProcessVisualisation(self):
        self.logger.info("[VISUALISER] Display processvisualisation")
        DRY_TIME = 3
        # load skybox
        skybox = Skybox()
        texture_id = skybox.loadTexture()
        finished = False
        # setup timer and intrusiondetection
        timer = Timer()
        carrierDetection = CarrierDetection()
        Thread(target=carrierDetection.checkForIntrusion,
               args=[BASE_LEVEL_HEIGHT]).start()
        timer.start()
        currentTime = 0

        # drawing loop
        while not finished:
            self._eventLoop(texture_id)
            self._enableGLFeatures(True)
            # check for object intrusion
            if not carrierDetection.detectedIntrusion:
                # no intrusion, get timer time or resume timer
                if not timer.isPaused:
                    currentTime = timer.getTime()
                elif timer.isPaused:
                    self.errorLogger.warning(
                        "[VISUALISER] Intrusion removed. Resuming process")
                    currentTime = timer.resume()
            else:
                # detected intrusion, pausing timer
                if not timer.isPaused:
                    self.errorLogger.warning(
                        "[VISUALISER] Detected intrusion. Pausing process")
                    currentTime = timer.pause()
            # draw models depending on task
            if self.task == 'assemble':
                if currentTime < 5:
                    self.model.assemble(currentTime)
                else:
                    finished = True
                    self.setIsAssembled(True)
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
                    self.setIsPackaged(True)
            elif self.task == 'unpackage':
                self.setIsPackaged(False)
                if currentTime < 5:
                    self.unpackage(currentTime)
                else:
                    finished = True
                    self.unpackage(currentTime)
                    self.setIsPackaged(False)
            elif self.task == 'generic':
                if currentTime < 5:
                    self.model.generic(currentTime)
                else:
                    finished = True
                    self.model.generic(currentTime)
                    self.setIsAssembled(False)
            skybox.ground()
            self._enableGLFeatures(False)
            pygame.display.flip()
            pygame.time.wait(30)
        # kill intrusion detection thread
        carrierDetection.kill()
        time.sleep(0.3)
        return True

    # animation of the task "color". It gets applied on a
    # static 3d model
    def paint(self, currentTime):
        self.model.paintColor = self.paintColor
        self.model.setAlpha(0.2 * currentTime)
        self.drawModel()

    # animation of the task "unpackage". It gets applied on a
    # static 3d model
    def unpackage(self, currentTime):
        PackageModel().unpackage(currentTime)
        self.drawModel()

    # animation of the task "package". It gets applied on a
    # static 3d model
    def package(self, currentTime):
        PackageModel().package(currentTime)
        self.drawModel()

    """
    utils
    """

    def loadModel(self):
        if self.modelName == 'IAS-Logo':
            self.model = IASModel()
            self.model.setAssembled(self.isAssembled)
            self.model.setPackaged(self.isPackaged)
            self.model.setColor(self.color)
        else:
            # IAS logo is standard model to be loaded
            self.model = IASModel()
            self.model.setAssembled(self.isAssembled)
            self.model.setPackaged(self.isPackaged)
            self.model.setColor(self.color)

    def drawModel(self):
        if self.modelName == 'IAS-Logo':
            self.model.drawModel()
        else:
            # IAS logo is standard model to be loaded
            self.model.drawModel()
        return

    def initPygame(self):
        pygame.init()
        pygame.display.set_mode(self.display, FULLSCREEN | DOUBLEBUF | OPENGL)
        # set camera perspektive
        gluPerspective(60, (self.display[0] / self.display[1]), 1, 500.0)
        glTranslatef(-15, -2, -5)
        glRotatef(60, 1, 0, 0)
        # enable gl features
        glEnable(GL_DEPTH_TEST)
        # glClearColor(1.0, 1.0, 1.0, 0.0)
        glShadeModel(GL_FLAT)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendEquation(GL_FUNC_ADD)

        # glEnable(GL_LIGHTING)
        #glLight(GL_LIGHT0, GL_POSITION,  (0, 1, -7, 0))
        #glLightfv(GL_LIGHT0, GL_AMBIENT, (1, 1, 1, 1))
        #glLightfv(GL_LIGHT0, GL_DIFFUSE, (2, 2, 2, 1))
        #glLight(GL_LIGHT0, GL_POSITION, (0, .5, 1))
        glEnable(GL_COLOR_MATERIAL)

    def _enableGLFeatures(self, isEnabled):
        if isEnabled:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # glEnable(GL_LIGHTING)
            # glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        elif not isEnabled:
            # glDisable(GL_LIGHT0)
            # glDisable(GL_LIGHTING)
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
        self.isAssembled = isAssembled
        if self.model != None:
            self.model.setAssembled(isAssembled)

    def setIsPackaged(self, isPackaged):
        self.isPackaged = isPackaged
        if self.model != None:
            self.model.setPackaged(isPackaged)

    def setColor(self, color):
        self.color = color
        if self.model != None:
            self.model.setColor(color)

    def setPaintColor(self, paintColor):
        self.paintColor = paintColor
        if self.model != None:
            self.model.setPaintColor(paintColor)

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
