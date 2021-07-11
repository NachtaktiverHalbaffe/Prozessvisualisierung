"""
Filename: skybox.py
Version name: 1.0, 2021-07-10
Short description: Skybox model. Shows the conveyor belt of branch

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from api.constants import CWP_DIR
import sys
sys.path.append('.')
sys.path.append('..')


class Skybox(object):

    def __init__(self):
        pass

    # ground model
    def ground(self):
        matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        x = matrix[3][0]
        vertices = (
            (-10-x, -0.1, 2.5),
            (10-x, -0.1, 2.5),
            (10-x, -0.1, -8.5),
            (-10-x, -0.1, -8.5),
        )

        glDisable(GL_BLEND)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_TEXTURE_2D)

        # draw ground (maps texture coordinates to coordinates of the surface)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3fv(vertices[0])
        glTexCoord2f(1, 0)
        glVertex3fv(vertices[1])
        glTexCoord2f(1, 1)
        glVertex3fv(vertices[2])
        glTexCoord2f(0, 1)
        glVertex3fv(vertices[3])
        glEnd()

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glDisable(GL_COLOR_MATERIAL)

    # load texture from storage into ram
    # @return:
    #   id: id of the loaded texture
    def loadTexture(self):
        PATH_TEXTURE = CWP_DIR + '/visualiser/3dmodels/tex.bmp'
        # loading texture
        image = pygame.image.load(PATH_TEXTURE)
        data = pygame.image.tostring(image, 'RGB', True)
        id = glGenTextures(1)
        width, height = image.get_rect().size
        # store texture to opengl enviroment
        glBindTexture(GL_TEXTURE_2D, id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,  # First mip-level
            3,  # Bytes per pixel, 4 for RGBA
            width,
            height,
            0,  # Texture border
            GL_RGB,
            GL_UNSIGNED_BYTE,
            data)

        # return the id og the texture which identifies the texture
        return id
