"""
Filename: processvisualisationapi.py
Version name: 0.1, 2021-05-31
Short description: data models

(C) 2003-2021 IAS, Universitaet Stuttgart

"""


import sys
sys.path.append('.')
sys.path.append('..')
from settings import db  # nopep8


class VisualisationTaskModel(db.Model):
    __table_args__ = {'extend_existing': True}
    # internal id. There can be only one instance of the model at each time
    id = db.Column(db.Integer, primary_key=True)
    # task which the unit should execute
    task = db.Column(db.String(20), nullable=False)
    # id of workingpiece with which the task gets executed
    assignedWorkingPiece = db.Column(db.Integer, nullable=True)
    # painting color if task is color
    paintColor = db.Column(db.String(7), nullable=True)

    def __repr__(self):
        return f"VisualisationTask(id = {str(id)}, task = {task}, assignedWorkingPiece = {str(assignedWorkingPiece)})"


class StateModel(db.Model):
    __table_args__ = {'extend_existing': True}
     # internal id. There can be only one instance of the model at each time
    id = db.Column(db.Integer, primary_key=True)
    # state of the unit. can be "idle", "waiting", "playing" and "finished"
    state = db.Column(db.String(20), nullable=False)
    # id of the resource where the unit is mounted on. is also id of the unit in the mes
    boundToResourceID = db.Column(db.Integer)
    # ip adress of the unit
    ipAdress = db.Column(db.String(20), nullable=False)
    # baselevel of the ultrasonic sensors. baselevel gets measured each time the unit starts up
    baseLevelHeight = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"VisualisationUnit(state= {state}, bound to ressource = {str(boundToResourceID)}, ipAdress = {ipAdress}, baseLevelHeight = {baseLevelHeight})"


class StateWorkingPieceModel(db.Model):
    __table_args__ = {'extend_existing': True}
     # internal id. There can be only one instance of the model at each time
    id = db.Column(db.Integer, primary_key=True)
    # id of the workingpiece
    pieceID = db.Column(db.Integer, nullable=False)
    # current color of the workingpiece
    color = db.Column(db.String(7), nullable=True)
    # if workingpiece is assembled
    isAssembled = db.Column(db.Boolean, nullable=False)
    # if workingpiece is packaged
    isPackaged = db.Column(db.Boolean, nullable=False)
    # id of carrier where the workingpiece is located
    carrierID = db.Column(db.Integer, nullable=True)
    # name of the 3D-Model of the workingpiece as which its displayed
    model = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"StateWorkingPiece(state = {state}, color = {color}, assembled = {str(assembled)}, packaged = {str(packaged)}, model = {model},carrierID = {str(carrierID)})"
