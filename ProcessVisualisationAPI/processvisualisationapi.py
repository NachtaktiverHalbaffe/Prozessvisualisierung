"""
Filename: processvisualisationapi.py
Version name: 0.1, 2021-05-20
Short description: Module for providing the REST Interface

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
import socket
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask import Flask
import sys
sys.path.append('.')
sys.path.append('..')


# Flask initialisation
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


"""
Models
"""


class VisualisationTaskModel(db.Model):
    __tablename__ = 'tblVisualisationTaskModel'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(20), nullable=False)
    assignedWorkingPiece = db.Column(db.Integer, nullable=True)
    stateWorkingPiece = db.relationship(
        'StateWorkingPieceModel', backref="tblVisualisationTaskModel", uselist=False)

    def __repr__(self):
        return f"VisualisationTask(id = {str(id)}, task = {task}, assignedWorkingPiece = {str(assignedWorkingPiece)})"


class StateModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20), nullable=False)
    boundToResourceID = db.Column(db.Integer)
    ipAdress = db.Column(db.String(20), nullable=False)
    baseLevelHeight = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"VisualisationUnit(state= {state}, bound to ressource = {str(boundToResourceID)}, ipAdress = {ipAdress}, baseLevelHeight = {baseLevelHeight})"


class StateWorkingPieceModel(db.Model):
    state = db.Column(db.String(20), nullable=False)
    pNo = db.Column(db.Integer, nullable=True)
    ressourceID = db.Column(db.Integer)
    color = db.Column(db.String(7), nullable=True)
    assembled = db.Column(db.Boolean, nullable=False)
    packaged = db.Column(db.Boolean, nullable=False)
    carrierID = db.Column(db.Integer, primary_key=True)
    assignedTask = db.Column(
        db.Integer, db.ForeignKey('tblVisualisationTaskModel.id'))

    def __repr__(self):
        return f"StateWorkingPiece(state = {state}, color = {color}, assembled = {str(assembled)}, packaged = {str(packaged)}, carrierID = {str(carrierID)})"


"""
Defining resources with necessary CRUD-Operations
"""


class StateUnit(Resource):
    resourceFields = {
        'id': fields.Integer,
        'state': fields.String,
        'boundToResourceID': fields.Integer,
        'ipAdress': fields.String,
        'baseLevelHeight': fields.Float
    }

    @marshal_with(resourceFields)
    def get(self):
        response = StateModel.query.first()
        if not response:
            abort(404, message="No state available")
        return response, 201


class APIOverview(Resource):
    def get(self):
        return {
            "/api": {
                "description": "Overview of all API endpoints",
                "options": "GET"
            },
            "/api/StateUnit": {
                "description": "Current state of the visualisationunit",
                "options": "GET"
            },
            "/api/VisualisationTask": {
                "description": "Current visualisationtask of the unit",
                "options": "GET, PUT, DELETE"
            },
        }


class VisualisationTask(Resource):
    resourceFields = {
        'id': fields.Integer,
        'task': fields.String,
        'assignedWorkingPiece': fields.Integer
    }

    def __init__(self):
        # Arguments for the put request
        self.putArgs = reqparse.RequestParser()
        self.putArgs.add_argument(
            "task", type=str, help="Task which should be executed", required=True)
        self.putArgs.add_argument("assignedWorkingPiece", type=int,
                                  help="Ressource ID of the workingpiece with which the task should be run")
        self.patchArgs = reqparse.RequestParser()
        self.patchArgs.add_argument(
            "task", type=str, help="Task which should be executed")
        self.patchArgs.add_argument("assignedWorkingPiece", type=int,
                                    help="Ressource ID of the workingpiece with which the task should be run")
        self.DEFINED_TASKS = [
            "assemble",
            "package",
            "unpackage",
            "color",
            "generic",
            "store",
            "unstore",
        ]

    # handle put request
    @marshal_with(resourceFields)
    def put(self):
        # parse arguments from the request
        args = self.putArgs.parse_args()
        if not args["tasks"] in self.DEFINED_TASKS:
            abort(
                409, message="No valid task name. Valid task names: assemble, package, unpackage, color, generic, store, unstore")
        task = VisualisationTaskModel(
            id=1, task=args['task'], assignedWorkingPiece=args['assignedWorkingPiece'])
        # save object to databse
        if VisualisationTaskModel.query.filter_by(id=1).first():
            abort(
                409, message="Visualisation unit already executes task, update or wait until it got executed")
        db.session.add(task)
        db.session.commit()
        return task, 201

    def delete(self):
        task = VisualisationTaskModel.query.filter_by(id=1).first()
        if not task:
            abort(404, message="No task found")
        db.session.delete(task)
        db.session.commit()
        return "", 204

    @marshal_with(resourceFields)
    def get(self):
        response = VisualisationTaskModel.query.filter_by(id=1).first()
        if not response:
            abort(404, message="No task assigned to visualisation unit")
        return response, 201

    @marshal_with(resourceFields)
    def patch(self):
        # parse arguments from the request
        args = self.patchArgs.parse_args()
        task = VisualisationTaskModel.query.filter_by(id=1).first()
        if not task:
            abort(
                404, message="No task to update")

        # update argument
        if args["task"]:
            task.task = args["task"]
        if args["assignedWorkingPiece"]:
            task.assignedWorkingPiece = args['assignedWorkingPiece']

        # save object to databse
        db.session.add(task)
        db.session.commit()
        return task, 202


"""
Adding urls to endpoints
"""

api.add_resource(APIOverview, '/api')
api.add_resource(StateUnit, '/api/StateUnit')
api.add_resource(VisualisationTask, '/api/VisualisationTask')
# example for request with params
# api.add_resource(StateUnit, '/StateUnit/<string: state>')

if __name__ == "__main__":
    from carrierdetection.carrierdetection import CarrierDetection
    db.create_all()
    # update or create state at startup
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
