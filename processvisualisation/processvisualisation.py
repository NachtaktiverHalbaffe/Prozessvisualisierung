"""
Filename: processvisualisation.py
Version name: 1.0, 2021-07-10
Short description: Module for handling processvisualisation

(C) 2003-2021 IAS, Universitaet Stuttgart

"""

from threading import Thread, Event
import logging
import pygame
import sys
import time
sys.path.append('.')
sys.path.append('..')

from api.mesrequests import sendError, getStateWorkingPiece, updateStateVisualisationUnit, updateStateWorkingPiece, getStatePLC  # nopep8
from carrierdetection.carrierdetection import CarrierDetection  # nopep8
from visualiser.visualiser import Visualiser  # nopep8
from api.constants import FILE_HANDLER_PV, STREAM_HANDLER, FILE_HANDLER_ERROR  # nopep8


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
        # setup carrierdetection
        self.carrierDetection = CarrierDetection()

        # setup logging
        self.logger = logging.getLogger("processvisualisation")
        self.errorLogger = logging.getLogger("error")
        self.logger.setLevel(logging.INFO)
        self.errorLogger.setLevel(logging.WARNING)
        # add logger handler to logger
        self.logger.handlers = []
        self.logger.addHandler(STREAM_HANDLER)
        self.logger.addHandler(FILE_HANDLER_PV)
        self.errorLogger.handlers = []
        self.errorLogger.addHandler(STREAM_HANDLER)
        self.errorLogger.addHandler(FILE_HANDLER_ERROR)

    # Handles the process of executing a visualisation task
    def executeOrder(self):
        from api.settings import visualiser

        # get parameter for task and setup visualiser
        pygame.quit()
        self.carrierDetection.killCarrierDetection()
        self.logger.info("[PROCESSVISUALISATION] Visualisation startet.")
        self.updateOrder()
        self.pvStopFlag.clear()
        if not pygame.get_init():
            visualiser.initPygame()
        visualiser.reviveVisualiser()
        # start carrierdetection
        Thread(target=self.carrierDetection.detectCarrier,
               args=[self.baseLevelHeight]).start()

        """
        Incoming carrier
        """
        # check if processvisualisation got aborted
        if not self.pvStopFlag.is_set():
            self._updateVisualiser()
            Thread(target=self._updateState, args=["waiting"]).start()
            visualiser.displayIdleStill()
        # visualisation task got aborted
        else:
            visualiser.displayIdleStill()
            Thread(target=self._idleAnimation).start()
            self.pvStopFlag.clear()
            return

        while True:
            # check if processvisualisation got aborted
            if not self.pvStopFlag.is_set():
                if self.carrierDetection.detectedOnEntrance:
                    # display incoming carrier
                    Thread(target=self._updateState, args=["playing"]).start()
                    # get final state of workingpiece from mes and
                    # update everything that needs to be updated
                    getStateWorkingPiece(self.assignedWorkingPiece)
                    self.updateOrder()
                    self._updateVisualiser()
                    self.logger.info(
                        "[PROCESSVISUALISATION] Carrier entered the unit. Display animations")
                    visualiser.displayIncomingCarrier()
                    break
            # visualisation task got aborted
            else:
                Thread(target=self._idleAnimation).start()
                self.pvStopFlag.clear()
                return

        """
        process itself
        """
        # check if processvisualisation got aborted
        if not self.pvStopFlag.is_set():
            while True:
                # check if workingstation is busy
                data = getStatePLC(self.boundToResource)
                # only display visualisation if bound resource is also busy
                if data["state"] == "busy":
                    if self._validateTask():
                        Thread(target=self._updateVisualiser).start()
                        if visualiser.displayProcessVisualisation(self.carrierDetection):
                            Thread(target=self._updateState,
                                   args=["finished"]).start()
                            # update parameter if task is finished
                            Thread(target=self._updatePar).start()
                            break
                    else:
                        # workingpiece is in wrong state => dont execute task
                        self.errorLogger.error(
                            "[PROCESSVISUALISATION] Visualisation task isnt executable because workingpiece is in wrong state. Aborting processVisualisation on unit:" + str(self.boundToResource))
                        sendError(level="[ERROR]",
                                  msg="Visualisation task isnt executable because workingpiece is in wrong state. Aborting processVisualisation on unit:" + str(self.boundToResource))
                        break
                elif self.carrierDetection.detectedOnExit:
                    # detects carrier leaving the unit => carrier was only driving through unit
                    self.errorLogger.error(
                        "[PROCESSVISUALISATION] Bound resource under unit isnt executing a task and carrier leaved the unit. Assuming detected carrier hasnt a assigned task")
                    sendError(
                        level="[WARNING]", msg="Bound resource under unit isnt executing a task and carrier leaved the unit. Assuming detected carrier hasnt a assigned task")
                    Thread(target=self._updateState,
                           args=["finished"]).start()
                    visualiser.displayOutgoingCarrier()
                    self.carrierDetection.killCarrierDetection()
                    return self.executeOrder()
                else:
                    time.sleep(0.5)
        # visualisation task got aborted
        else:
            Thread(target=self._idleAnimation).start()
            self.pvStopFlag.clear()
            return

        """
        outgoing carrier
        """
        Thread(target=self._updateState, args=["finished"]).start()
        while True:
            if not self.pvStopFlag.is_set():
                if self.carrierDetection.detectedOnExit:
                    visualiser.displayOutgoingCarrier()
                    break
            # visualisation task got aborted
            else:
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
        self.logger.info(
            "[PROCESSVISUALISATION] Carrier leaved the unit. Visualisation ended.")

    # loads the states of the visualisationtask, workingpiece and state of unit and applies them to
    # the processvisualisation and all components in it
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

        # update intern params of processvisualisation
        state = StateModel.query.filter_by(id=1).first()
        self.baseLevelHeight = state.baseLevelHeight
        self.boundToResource = state.boundToResourceID

    # stop executing processvisualisation
    def kill(self):
        self.pvStopFlag.set()

    # update params of visualiser
    def _updateVisualiser(self):
        from api.settings import visualiser

        visualiser.setColor(self.color)
        visualiser.setPaintColor(self.paintColor)
        visualiser.setIsAssembled(self.isAssembled)
        visualiser.setIsPackaged(self.isPackaged)
        visualiser.setModelName(self.model)
        visualiser.setTask(self.task)

    # update state of unit internally and also on mes
    # @params:
    #   newState: String of new state for the attribute state in the state of unit
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
        Thread(target=updateStateVisualisationUnit, args=[
               state.boundToResourceID, data]).start()

    # display idle animation
    def _idleAnimation(self):
        from api.settings import visualiser
        visualiser.displayIdleStill()
        visualiser.displayIdle()

    # update parameter after finishing the task
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
        Thread(target=updateStateWorkingPiece, args=[
               workingPiece.pieceID, data]).start()

    # cleanup local database and kill carrierDetection
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
        # kill ultrasonic sensors measurements threads
        self.carrierDetection.killCarrierDetection()

    # validate if task is executable depending on state of workingpiece
    def _validateTask(self):
        if self.task == "assemble":
            # for assembly the workingpiece needs to be not assembled and not packaged
            if self.isAssembled or self.isPackaged:
                return False
            elif not self.isAssembled and not self.isPackaged:
                return True
        elif self.task == "package":
            # for packaging the workingpiece needs to be not packaged
            if not self.isPackaged:
                return True
            elif self.isPackaged:
                return False
        elif self.task == "unpackage":
            # for unpackaging the workingpiece needs to be packaged
            if self.isPackaged:
                return True
            elif not self.isPackaged:
                return False
        elif self.task == "color":
            # for coloring the workingpiece needs to be not packaged
            if not self.isPackaged:
                return True
            elif self.isPackaged:
                return False
        elif self.task == "generic":
            # each model has unique generic task, so validation
            # depends on model
            if self.model == "IAS-Logo":
                # for disassembly the workingpiece needs to be assembled and not packaged
                if self.isAssembled and not self.isPackaged:
                    return True
                elif not self.isAssembled or self.isPackaged:
                    return False
