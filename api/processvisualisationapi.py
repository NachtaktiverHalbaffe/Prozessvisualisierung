"""
Filename: processvisualisationapi.py
Version name: 0.1, 2021-05-20
Short description: Module for providing the REST Interface

(C) 2003-2021 IAS, Universitaet Stuttgart

"""


from flask_restful import Resource, reqparse, fields, marshal_with, abort
import socket
import sys
sys.path.append('.')
sys.path.append('..')

from models import *  # nopep8
from resources import *  # nopep8
from carrierdetection.carrierdetection import CarrierDetection  # nopep8
from settings import db, app, api  # nopep8

api.add_resource(APIOverview, '/api')
api.add_resource(StateUnit, '/api/StateUnit')
api.add_resource(VisualisationTask, '/api/VisualisationTask')
api.add_resource(BindToResource, '/api/StateUnit/bind/<int:bindToResource>')
api.add_resource(StateWorkingPiece, '/api/StateWorkingPiece')


if __name__ == "__main__":
    # update or create state at startup
    # db.create_all()

    state = StateModel.query.filter_by(id=1).first()
    if not state:
        state = StateModel(
            id=1,
            ipAdress=socket.gethostbyname(socket.gethostname()),
            baseLevelHeight=CarrierDetection().calibrate(),
            boundToResourceID=0,
            state="idle")
    else:
        state.id = 1
        state.ipAdress = socket.gethostbyname(socket.gethostname())
        state.baseLevelHeight = CarrierDetection().calibrate()
    db.session.add(state)
    db.session.commit()
    # TODO send initial request to mes
    # ! In production change debug to false
    app.run(debug=True)
