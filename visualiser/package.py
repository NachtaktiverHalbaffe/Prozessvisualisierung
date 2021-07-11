"""
Filename: package.py
Version name: 1.0, 2021-07-10
Short description: model object of package

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
from .model import Model
import pywavefront
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from api.constants import CWP_DIR
import sys
sys.path.append('.')
sys.path.append('..')


class PackageModel(Model):
    def __init__(self):
        # static color(s) of parts of the 3d model (brown)
        self.staticColor = (0.62740, 0.3215, 0.176)
        # state of workingpiece which is passed down from
        # processvisualisation
        self.isAssembled = True
        self.isPackaged = False

        self.color = '#cd853f'
        self.paintColor = '#000000'
        self.alpha = 1
        # path to the .obj-files of the model
        cwd = CWP_DIR
        self.modelNames = [
            cwd+'/visualiser/3dmodels/PACKAGE_TOP_FINAL.obj',
            cwd+'/visualiser/3dmodels/PACKAGE_BOX_FINAL.obj'
        ]
        # "master" scale to all models
        self.scaledSize = 7
        self.models = []
        for model in self.modelNames:
            self.models.append(pywavefront.Wavefront(
                model, collect_faces=True))

    """
    Drawing models and costum animations
    """

    def drawModel(self):
        for i in range(len(self.models)):
            if i == 0:
                # correcting position. Be shure to encapsulate all corrections
                # beetween glPushMatrix() amd glPopMatrix() so the corrections
                # are applied to the model and not to the whole scene
                glPushMatrix()
                glTranslated(-1.5, -0.5, 0)
                glScaled(1.1, 0.5, 1.45)
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            if i == 1:
                # correcting position. Be shure to encapsulate all corrections
                # beetween glPushMatrix() amd glPopMatrix() so the corrections
                # are applied to the model and not to the whole scene
                glPushMatrix()
                glTranslated(-1.5, 0, 0)
                glScaled(1.1, 0.4, 1.5)
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()

    # animate the assemble task
    def package(self, time):
        for i in range(len(self.models)):
            if i == 0:
                glPushMatrix()
                glTranslated(-1.5, -0.5, 0)
                glScaled(1.1, 0.5, 1.5)
                glRotated(90, -1, 0, 0)
                # rotate the top cover of the top of the box
                glRotated(18 * time, 1, 0, 0)
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            if i == 1:
                glPushMatrix()
                glTranslated(-1.5, 0, 0)
                # scale up the box on the y-axis until it is flat
                glScaled(1.1, 0.08 * time, 1.5)
                glEnable(GL_COLOR_MATERIAL)
                self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
        return True

    # animates the generic task
    def unpackage(self, time):
        for i in range(len(self.models)):
            if i == 0:
                glPushMatrix()
                glTranslated(-1.5, -0.5, 0)
                glScaled(1.1, 0.5, 1.5)
                # rotate the top cover of the top of the box
                glRotated(18 * time, -1, 0, 0)
                glEnable(GL_COLOR_MATERIAL)
                if time < 5:
                    self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
            if i == 1:
                glPushMatrix()
                glTranslated(-1.5, 0, 0)
                # scale down the box on the y-axis until it is flat
                glScaled(1.1, 0.38 - 0.08 * time, 1.5)
                glEnable(GL_COLOR_MATERIAL)
                if time < 5:
                    self._drawModel(self.models[i], self.staticColor)
                glDisable(GL_COLOR_MATERIAL)
                glPopMatrix()
        return True
