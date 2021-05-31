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
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(20), nullable=False)
    assignedWorkingPiece = db.Column(db.Integer, nullable=True)
    paintColor = db.Column(db.String(7), nullable=True)
    # stateWorkingPiece = db.relationship(
    #     'StateWorkingPieceModel', backref="tblVisualisationTaskModel", uselist=False)

    def __repr__(self):
        return f"VisualisationTask(id = {str(id)}, task = {task}, assignedWorkingPiece = {str(assignedWorkingPiece)})"


class StateModel(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20), nullable=False)
    boundToResourceID = db.Column(db.Integer)
    ipAdress = db.Column(db.String(20), nullable=False)
    baseLevelHeight = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"VisualisationUnit(state= {state}, bound to ressource = {str(boundToResourceID)}, ipAdress = {ipAdress}, baseLevelHeight = {baseLevelHeight})"


class StateWorkingPieceModel(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20), nullable=True)
    pNo = db.Column(db.Integer, nullable=True)
    resourceID = db.Column(db.Integer)
    color = db.Column(db.String(7), nullable=True)
    isAssembled = db.Column(db.Boolean, nullable=False)
    isPackaged = db.Column(db.Boolean, nullable=False)
    model = db.Column(db.String(100), nullable=True)
    carrierID = db.Column(db.Integer, primary_key=True)
    # assignedTask = db.Column(
    #     db.Integer, db.ForeignKey('tblVisualisationTaskModel.id'))

    def __repr__(self):
        return f"StateWorkingPiece(state = {state}, color = {color}, assembled = {str(assembled)}, packaged = {str(packaged)}, model = {model},carrierID = {str(carrierID)})"
