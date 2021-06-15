"""
Filename: processvisualisation.py
Version name: 0.1, 2021-05-31
Short description: Module for handling processvisualisation

(C) 2003-2021 IAS, Universitaet Stuttgart

"""

from api.mesrequests import sendError, getStateWorkingPiece, updateStateVisualisationUnit, updateStateWorkingPiece
from threading import Thread, Event
import pygame
import time
import sys
import requests
sys.path.append('.')
sys.path.append('..')

from carrierdetection.carrierdetection import CarrierDetection  # nopep8
from visualiser.visualiser import Visualiser  # nopep8
from api.constants import IP_MES  # nopep8


class ProcessVisualisation(object):

    def __init__(self, db):
        self.db = db
        self.assignedWorkingPiece = 0
        # visualisation params
        self.isAssembled = True
        self.isPackaged = False
        self.color = '#CCCCCC'
        self.paintColor = "#000000"
        self.task = "assemble"
        self.model = "IAS-Logo"
        self.baseLevelHeight = 0.0
        self.boundToResource = 0
        self.pvStopFlag = Event()
        self.pvStopFlag.clear()

    # Handles the process of executing a visualisation task
    def executeOrder(self):
        from api.settings import visualiser

        # get parameter for task and setup visualiser
        print("[PROCESSVISUALISATION] Visualisation startet.")
        self.updateOrder()
        visualiser.killVisualiser()
        self.pvStopFlag.clear()
        pygame.quit()
        if not pygame.get_init():
            visualiser.initPygame()
        visualiser.reviveVisualiser()

        """
        Incoming carrier
        """
        print(self.pvStopFlag.is_set())
        if not self.pvStopFlag.is_set():
            self._updateStateWorkingPiece()
            Thread(target=self._updateState, args=["waiting"]).start()
            visualiser.displayIdleStill()
        else:
            visualiser.displayIdleStill()
            Thread(target=self._idleAnimation).start()
            self.pvStopFlag.clear()
            return
        errorCounter = 0
        while True:
            print(self.pvStopFlag.is_set())
            if not self.pvStopFlag.is_set():
                if CarrierDetection().detectCarrier('entrance', self.baseLevelHeight):
                    # display incoming carrier
                    Thread(target=self._updateState, args=["playing"]).start()
                    # update state of workingpiece
                    getStateWorkingPiece(self.assignedWorkingPiece)
                    print(
                        "[PROCESSVISUALISATION] Carrier entered the unit. Display animations")
                    visualiser.displayIncomingCarrier()
                    break
                else:
                    errorCounter += 1
                    if errorCounter <= 3:
                        # repeating carrierdetection
                        print(
                            "[PROCESSVISUALISATION] Detected Carrier in exit, but expected it on entrance")
                        sendError(
                            msg="Detected Carrier in exit, but expected it on entrance. Resetting carrierdetection")
                    else:
                        # aborting visualisation task cause it detected too often the carrier on the exit
                        print(
                            "[PROCESSVISUALISATION] Detected carrier in exit multiple times, but expected it on entrance. Aborting processVisualisation on unit:" + str(self.boundToResource))
                        sendError(level="[ERROR]",
                                  msg="[PROCESSVISUALISATION] Detected carrier in exit multiple times, but expected it on entrance. Aborting processVisualisation on unit:" + str(self.boundToResource))
                        self._cleanup()
                        return
            else:
                visualiser.displayIdleStill()
                Thread(target=self._idleAnimation).start()
                self.pvStopFlag.clear()
                return

        """
        process itself
        """
        print(self.pvStopFlag.is_set())
        if not self.pvStopFlag.is_set():
            self.updateOrder()
            Thread(target=self._updateStateWorkingPiece).start()
            visualiser.displayProcessVisualisation()
            Thread(target=self._updateState, args=["finished"]).start()
            # update parameter if task is finished
            Thread(target=self._updatePar).start()
        else:
            visualiser.displayIdleStill()
            Thread(target=self._idleAnimation).start()
            self.pvStopFlag.clear()
            return
        """
        outgoing carrier
        """
        Thread(target=self._updateState, args=["finished"]).start()
        errorCounter = 0
        while True:
            if not self.pvStopFlag.is_set():
                if CarrierDetection().detectCarrier('exit', self.baseLevelHeight):
                    visualiser.displayOutgoingCarrier()
                    break
                else:
                    errorCounter += 1
                    if errorCounter <= 3:
                        # repeating carrierdetection
                        print(
                            "[PROCESSVISUALISATION] Detected Carrier in entrance, but expected it on exit")
                        sendError(
                            msg="Detected Carrier in entrance, but expected it on exit. Resetting carrierdetection")
                    else:
                        # aborting visualisation task cause it detected too often the carrier on the entrance
                        print(
                            "[PROCESSVISUALISATION] Detected Carrier in entrance multiple times, but expected it on exit. Aborting processvisualisation on unit:" + str(self.boundToResource))
                        sendError(level="[ERROR]",
                                  msg="Detected Carrier in entrance multiple times, but expected it on exit. Aborting processvisualisation on unit:" + str(self.boundToResource))
                        self._cleanup()
                        return
            else:
                visualiser.displayIdleStill()
                Thread(target=self._idleAnimation).start()
                self.pvStopFlag.clear()
                return

        """
        Cleanup
        """
        Thread(target=self._updateState, args=["idle"]).start()
        self._cleanup()
        visualiser.reviveVisualiser()

        """
        display idle
        """
        displayIdleThread = Thread(target=self._idleAnimation)
        displayIdleThread.start()
        print("[PROCESSVISUALISATION] Carrier leaved the unit. Visualisation ended.")

    def updateOrder(self):
        from api.models import StateModel, StateWorkingPieceModel, VisualisationTaskModel  # nopep8
        # update task data
        task = VisualisationTaskModel.query.filter_by(id=1).first()
        self.id = task.id
        self.task = task.task
        self.assignedWorkingPiece = task.assignedWorkingPiece
        self.paintColor = task.paintColor

        # update state of workingpiece
        workingPiece = StateWorkingPieceModel.query.filter_by(id=1)
        if workingPiece.count() == 1:
            workingPiece = workingPiece.first()
            self.model = workingPiece.model
            self.isAssembled = workingPiece.isAssembled
            self.isPackaged = workingPiece.isPackaged
            self.color = workingPiece.color
        else:
            self.model = "IAS-Logo"
            self.isAssembled = False
            self.isPackaged = False
            self.color = "#000000"

        state = StateModel.query.filter_by(id=1).first()
        self.baseLevelHeight = state.baseLevelHeight
        self.boundToResource = state.boundToResourceID

    def kill(self):
        self.pvStopFlag.set()

    def _updateStateWorkingPiece(self):
        from api.settings import visualiser

        visualiser.setColor(self.color)
        visualiser.setPaintColor(self.paintColor)
        visualiser.setIsAssembled(self.isAssembled)
        visualiser.setIsPackaged(self.isPackaged)
        visualiser.setModelName(self.model)
        visualiser.setTask(self.task)

    def _updateState(self, newState):
        from api.models import StateModel  # nopep8
        # update stateworkingpiece
        state = StateModel.query.filter_by(id=1).first()
        state.state = newState
        self.db.session.add(state)
        self.db.session.commit()

        # send update to mes
        if newState != "idle":
            task = self.task
        else:
            task = "None"
        data = {
            "state": newState,
            "assignedTask": task
        }
        updateStateVisualisationUnit(state.boundToResourceID, data)

    def _idleAnimation(self):
        from api.settings import visualiser

        visualiser.displayIdle()

    def _updatePar(self):
        from api.models import StateWorkingPieceModel  # nopep8
        workingPiece = StateWorkingPieceModel.query.filter_by(id=1).first()
        if self.task == "color":
            self.color = self.paintColor
            workingPiece.color = self.color
        elif self.task == "assemble":
            self.isAssembled = True
            workingPiece.isAssembled = self.isAssembled
        elif self.task == "package":
            self.isPackaged = True
            workingPiece.isPackaged = self.isPackaged
        elif self.task == "unpackage":
            self.isPackaged = False
            workingPiece.isPackaged = self.isPackaged
        elif self.task == "generic":
            self.isAssembled = False
            workingPiece.isAssembled = self.isAssembled
        self.db.session.add(workingPiece)
        self.db.session.commit()
        # update stateworkingpiece in mes
        data = {
            "isPackaged": workingPiece.isPackaged,
            "isAssembled": workingPiece.isAssembled,
            "color": workingPiece.color,
            "storageLocation": 0,
        }
        updateStateWorkingPiece(workingPiece.pieceID, data)

    # cleanup local database

    def _cleanup(self):
        from api.models import StateWorkingPieceModel, VisualisationTaskModel  # nopep8
        # delete visualisation task from local database
        task = VisualisationTaskModel.query.filter_by(id=1).first()
        self.db.session.delete(task)
        self.db.session.commit()
        # delete stateworkingpiece from local database
        workingPiece = StateWorkingPieceModel.query.filter_by(id=1).first()
        self.db.session.delete(workingPiece)
        self.db.session.commit()
