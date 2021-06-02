"""
Filename: processvisualisation.py
Version name: 0.1, 2021-05-31
Short description: Module for handling processvisualisation

(C) 2003-2021 IAS, Universitaet Stuttgart

"""

from threading import Thread
import sys
import requests
sys.path.append('.')
sys.path.append('..')

from carrierdetection.carrierdetection import CarrierDetection  # nopep8
from visualiser.visualiser import Visualiser  # nopep8
#from api.settings import IP_MES  # nopep8


class ProcessVisualisation(object):

    def __init__(self, db):
        self.db = db
        self.assignedWorkingPiece = 0
        # visualisation params
        self.isAssembled = True
        self.isPackaged = False
        self.color = '#CCCCCC'
        self.paintColor = "#000000"
        self.task = "package"
        self.model = "IAS-Logo"
        self.baseLevelHeight = 0.0
        self.visualiser = None

    def executeOrder(self):
        from api.models import StateModel, StateWorkingPieceModel, VisualisationTaskModel  # nopep8
        from api.settings import IP_MES

        # get parameter for task and setup visualiser
        self.updateOrder()
        self.visualiser = Visualiser()
        # wait for carrier
        self._updateStateWorkingPiece()
        self._updateState("waiting")
        self.visualiser.displayIdle()
        if CarrierDetection().detectCarrier('entrance', self.baseLevelHeight):
            self._updateState("playing")
            displayIncomingThread = Thread(
                target=self.visualiser.displayIncomingCarrier)
            displayIncomingThread.start()
            displayIncomingThread.join()
        elif not CarrierDetection().detectCarrier('entrance', self.baseLevelHeight):
            # TODO error
            pass

        # display process
        self._updateStateWorkingPiece()
        displayProcess = Thread(
            target=self.visualiser.displayProcessVisualisation)
        displayProcess.start()
        displayProcess.join()
        self._updateState("finished")
        # update parameter if task is finished
        workingPiece = StateWorkingPieceModel.query.filter_by(id=1).first()
        if self.task == "color":
            self.color = self.paintColor
            workingPiece.color = self.color
        elif self.task == "assemble":
            self.isAssembled = True
            workingPiece.isAssembled = self.isAssembled
        elif self.task == "package":
            self.isPackaged = True
        elif self.task == "unpackage":
            self.isPackaged == False
            workingPiece.isPackaged = self.isPackaged
        self.db.session.add(workingPiece)
        self.db.session.commit()
        # update stateworkingpiece in mes
        data = {
            "isPackaged": workingPiece.isPackaged,
            "isAssembled": workingPiece.isAssenbled,
            "color": workingPiece.color,
        }
        request = requests.patch(
            IP_MES + ":8000/api/StateVisualisationUnit/" + workingPiece.id, data=data)
        if not request.ok:
            pass

        # display outgoing carrier
        self._updateStateWorkingPiece()
        self._updateState("finished")
        if CarrierDetection().detectCarrier('exit', self.baseLevelHeight):
            displayOutgoingThread = Thread(
                target=self.visualiser.displayProcessVisualisation)
            displayOutgoingThread.start()
            displayOutgoingThread.join()
        elif not CarrierDetection().detectCarrier('exit', self.baseLevelHeight):
            # TODO error
            pass

        self._updateState("idle")
        task = VisualisationTaskModel.query.filter_by(id=1).first()
        self.db.session.delete(task)
        self.db.session.commit()
        workingPiece = StateWorkingPieceModel.query.filter_by(id=1).first()
        self.db.session.delete(workingPiece)
        self.db.session.commit()

    def updateOrder(self):
        from api.models import StateModel, StateWorkingPieceModel, VisualisationTaskModel  # nopep8
        # update task data
        task = VisualisationTaskModel.query.filter_by(id=1).first()
        self.id = task.id
        self.task = task.task
        self.assignedWorkingPiece = task.assignedWorkingPiece
        self.paintColor = task.paintColor

        # update state of workingpiece
        workingPiece = StateWorkingPieceModel.query.filter_by(id=1).first()
        self.model = workingPiece.model
        self.isAssemled = workingPiece.isAssembled
        self.isPackaged = workingPiece.isPackaged
        self.color = workingPiece.color

        state = StateModel.query.filter_by(id=1).first()
        self.baseLevelHeight = state.baseLevelHeight

    def _updateStateWorkingPiece(self):
        from api.models import StateModel, StateWorkingPieceModel, VisualisationTaskModel  # nopep8
        self.visualiser.setColor(self.color)
        self.visualiser.setPaintColor(self.paintColor)
        self.visualiser.setIsAssembled(self.isAssemled)
        self.visualiser.setIsPackaged(self.isAssemled)
        self.visualiser.setModelName(self.model)

    def _updateState(self, newState):
        from api.models import StateModel, StateWorkingPieceModel, VisualisationTaskModel  # nopep8
        from api.settings import IP_MES
        state = StateModel.query.filter_by(id=1).first()
        state.state = newState
        self.db.session.add(state)
        self.db.session.commit()

        # send update to mes
        data = {
            "state": newState
        }
        request = requests.patch(
            IP_MES + ":8000/api/StateVisualisationUnit/" + str(state.boundToResourceID), data=data)
        if not request.ok:
            pass
