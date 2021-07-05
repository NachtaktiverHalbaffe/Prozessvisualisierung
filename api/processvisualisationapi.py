"""
Filename: processvisualisationapi.py
Version name: 0.1, 2021-05-20
Short description: Module for providing the REST Interface

(C) 2003-2021 IAS, Universitaet Stuttgart

"""

import socket
import sys
sys.path.append('.')
sys.path.append('..')

from models import *  # nopep8
from resources import *  # nopep8
from carrierdetection.carrierdetection import CarrierDetection  # nopep8 # nopep8
from settings import db, app, api  # nopep8
from mesrequests import updateStateVisualisationUnit  # nopep8
from constants import BASE_LEVEL_HEIGHT  # nopep8

api.add_resource(APIOverview, '/api')
api.add_resource(StateUnit, '/api/StateUnit')
api.add_resource(VisualisationTask, '/api/VisualisationTask')
api.add_resource(BindToResource, '/api/StateUnit/bind/<int:bindToResource>')
api.add_resource(StateWorkingPiece, '/api/StateWorkingPiece')


if __name__ == "__main__":
    # update or create state at startup
    # db.create_all()

    # update state
    state = StateModel.query.filter_by(id=1).first()
    # use dummy socket and connect to non existing ip to ensure to get right ip adress
    testSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    testSock.connect(("10.255.255.255", 1))
    ipAdress = testSock.getsockname()[0]
    if not state:
        state = StateModel(
            id=1,
            ipAdress=ipAdress,
            baseLevelHeight=BASE_LEVEL_HEIGHT,
            boundToResourceID=0,
            state="idle")
    else:
        state.id = 1
        state.ipAdress = ipAdress
        state.baseLevelHeight = BASE_LEVEL_HEIGHT
        state.state= "idle"
    db.session.add(state)
    db.session.commit()

    # delete unfinished visualisation task from local database for initial state
    task = VisualisationTaskModel.query.filter_by(id=1)
    if task.count() == 1:
        db.session.delete(task.first())
        db.session.commit()
    # delete stateworkingpiece from local database for initial state
    workingPiece = StateWorkingPieceModel.query.filter_by(id=1)
    if workingPiece.count() == 1:
        db.session.delete(workingPiece.first())
        db.session.commit()

    # send initial state to mes
    if VisualisationTaskModel.query.filter_by(id=1).first():
        assignedTask = VisualisationTaskModel.query.filter_by(
            id=1).first().task
    else:
        assignedTask = "None"
    data = {
        "state": state.state,
        "ipAdress": state.ipAdress,
        "boundToRessource": state.boundToResourceID,
        "baseLevelHeight": state.baseLevelHeight,
        "assignedTask": assignedTask,
    }
    # send request to mes
    Thread(target=updateStateVisualisationUnit,args=[state.boundToResourceID, data]).start()

    # ! In production change debug to false
    app.run(debug=False, host="0.0.0.0")
