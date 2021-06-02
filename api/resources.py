"""
Filename: resources.py
Version name: 0.1, 2021-05-31
Short description: resources for flask api

(C) 2003-2021 IAS, Universitaet Stuttgart

"""
from api.models import StateWorkingPieceModel
from models import *
from settings import IP_MES, processVisualisation, processVisualisation_thread
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from multiprocessing import Process
import requests
from threading import Thread


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
        'assignedWorkingPiece': fields.Integer,
        'paintColor': fields.String
    }

    def __init__(self):
        # Arguments for the put request
        self.putArgs = reqparse.RequestParser()
        self.putArgs.add_argument(
            "task", type=str, help="Task which should be executed", required=True)
        self.putArgs.add_argument("assignedWorkingPiece", type=int,
                                  help="Ressource ID of the workingpiece with which the task should be run")
        self.putArgs.add_argument("paintColor", type=str,
                                  help="Color for painting if task is color")
        self.putArgs.add_argument("paintColor", type=str,
                                  help="Color for painting if task is color")

        self.patchArgs = reqparse.RequestParser()
        self.patchArgs.add_argument(
            "task", type=str, help="Task which should be executed")
        self.patchArgs.add_argument("assignedWorkingPiece", type=int,
                                    help="Ressource ID of the workingpiece with which the task should be run")
        self.patchArgs.add_argument("paintColor", type=str,
                                    help="Color for painting if task is color")
        self.DEFINED_TASKS = [
            "assemble",
            "package",
            "unpackage",
            "color",
            "generic",
        ]

    # handle put request
    @marshal_with(resourceFields)
    def put(self):
        # parse arguments from the request
        args = self.putArgs.parse_args()
        if not args["task"] in self.DEFINED_TASKS:
            abort(
                409, message="No valid task name. Valid task names: assemble, package, unpackage, color, generic, store, unstore")
        task = VisualisationTaskModel(
            id=1, task=args['task'], assignedWorkingPiece=args['assignedWorkingPiece'], paintColor=args['paintColor'])
        # save object to databse
        if VisualisationTaskModel.query.filter_by(id=1).first():
            abort(
                409, message="Visualisation unit already executes task, update or wait until it got executed")
        db.session.add(task)
        db.session.commit()

        # get StateWorkingPiece
        request = requests.get(
            IP_MES + ":8000/api/StateWorkingPiece/" + str(task.assignedWorkingPiece))
        if request.ok:
            data = request.json()
            stateWorkingPiece = StateWorkingPieceModel(
                id=1,
                pieceID=data["id"],
                color=data["color"],
                isAssembled=data["isAssembled"],
                isPackaged=data["isPackaged"],
                model=data["model"]
            )
            if StateWorkingPieceModel.query.filter_by(id=1).count() == 1:
                db.session.delete(
                    StateWorkingPieceModel.query.filter_by(id=1).first())
            db.session.add(stateWorkingPiece)
            db.session.commit()

        # start visualisation task

        try:
            processVisualisation.reviveVisualiser()
            processVisualisation_thread.start()
        except Exception as e:
            print(e)
        # processVisualisation.executeOrder()

        return task, 201

    def delete(self):
        task = VisualisationTaskModel.query.filter_by(id=1).first()
        if not task:
            abort(404, message="No task found")
        db.session.delete(task)

        # change state
        state = StateModel.query.filter_by(id=1).first()
        state.state = "idle"
        db.session.add(state)
        db.session.commit()

        data = {
            "state": state.state,
            "ipAdress": state.ipAdress,
            "boundToRessource": state.boundToResourceID,
            "baseLevelHeight": state.baseLevelHeight,
            "assignedTask": "None",
        }
        # inform mes and quit processvisualisation
        processVisualisation.killVisualiser()
        request = requests.post(
            IP_MES+":8000/api/StateVisualisationUnit/", data=data)
        if not request.ok:
            # already exists => update it
            request = requests.patch(
                IP_MES+":8000/api/StateVisualisationUnit/" + str(state.boundToResourceID), data=data)
            if not request.ok:
                # error
                pass
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
        if args['paintColor']:
            task.paintColor = args['paintColor']

        # save object to databse
        db.session.add(task)
        db.session.commit()

        # update processvisualisation
        processVisualisation.updateOrder()
        return task, 202


class StateWorkingPiece(Resource):
    resourceFields = {
        'id': fields.Integer,
        'pieceID': fields.Integer,
        'color': fields.String,
        'isAssembled': fields.Boolean,
        'isPackaged': fields.Boolean,
        'model': fields.String,
        'carrierID': fields.Integer,
    }

    def __init__(self):
        # Arguments for the put request
        self.putArgs = reqparse.RequestParser()
        self.putArgs.add_argument(
            "id", type=int, help="id of the dataset")
        self.putArgs.add_argument(
            "pieceID", type=int, help="Id of the workingPiece", required=True)
        self.putArgs.add_argument(
            "color", type=str, help="Current color of the workingpiece", required=True)
        self.putArgs.add_argument(
            "isAssembled", type=bool, help="If workingpiece is assembled", required=True)
        self.putArgs.add_argument(
            "isPackaged", type=bool, help="If workingpiece is packaged", required=True)
        self.putArgs.add_argument(
            "model", type=str, help="Modelname of the 3D-Model")
        self.putArgs.add_argument(
            "carrierID", type=int, help="Id of carrier where workingpiece is located", required=False)

        self.patchArgs = reqparse.RequestParser()
        self.patchArgs.add_argument(
            "id", type=int, help="id of the dataset")
        self.patchArgs.add_argument(
            "pieceID", type=int, help="Id of the workingPiece", required=True)
        self.patchArgs.add_argument(
            "color", type=str, help="Current color of the workingpiece")
        self.patchArgs.add_argument(
            "isAssembled", type=bool, help="If workingpiece is assembled")
        self.patchArgs.add_argument(
            "isPackaged", type=bool, help="If workingpiece is packaged")
        self.patchArgs.add_argument(
            "model", type=str, help="Modelname of the 3D-Model")
        self.patchArgs.add_argument(
            "carrierID", type=int, help="Id of carrier where workingpiece is located")

    # handle put request

    @marshal_with(resourceFields)
    def put(self):
        # parse arguments from the request
        args = self.putArgs.parse_args()
        if not args["task"] in self.DEFINED_TASKS:
            abort(
                409, message="No valid task name. Valid task names: assemble, package, unpackage, color, generic, store, unstore")
        stateWorkingPieceModel = StateWorkingPieceModel(
            id=1,
            pieceID=args['pieceID'],
            color=args['color'],
            isAssembled=args['isAssembled'],
            isPackaged=args['isPackaged'],
            model=args['model'],
            carrierID=args['carrierID'])
        # save object to databse
        if StateWorkingPieceModel.query.filter_by(id=1).first():
            abort(
                409, message="WorkingPieceModel is already loaded. Please update the current one")
        db.session.add(stateWorkingPieceModel)
        db.session.commit()

        return stateWorkingPieceModel, 201

    def delete(self):
        stateWorkingPieceModel = StateWorkingPieceModel.query.filter_by(
            id=1).first()
        if not stateWorkingPieceModel:
            abort(404, message="No state of workingpiece found")
        db.session.delete(stateWorkingPieceModel)

        # change state
        state = StateModel.query.filter_by(id=1).first()
        state.state = "idle"
        db.session.add(state)
        db.session.commit()
        return "", 204

    @marshal_with(resourceFields)
    def get(self):
        response = StateWorkingPieceModel.query.filter_by(id=1).first()
        if not response:
            abort(404, message="No task assigned to visualisation unit")
        return response, 201

    @marshal_with(resourceFields)
    def patch(self):
        # parse arguments from the request
        args = self.patchArgs.parse_args()
        stateWorkingPieceModel = StateWorkingPieceModel.query.filter_by(
            id=1).first()
        if not stateWorkingPieceModel:
            abort(
                404, message="No task to update")

        # update argument
        if args["state"]:
            stateWorkingPieceModel.id = args["state"]
        if args["pNo"]:
            stateWorkingPieceModel.pNo = args['pNo']
        if args['resourceID']:
            stateWorkingPieceModel.resourceID = args['resourceID']
        if args['color']:
            stateWorkingPieceModel.color = args['color']
        if args['isAssembled']:
            stateWorkingPieceModel.isAssembled = args['isAssembled']
        if args['isPackaged']:
            stateWorkingPieceModel.isPackaged = args['isPackaged']
        if args['model']:
            stateWorkingPieceModel.model = args['model']
        if args['carrierID']:
            stateWorkingPieceModel.carrierID = args['carrierID']

        # save object to databse
        db.session.add(stateWorkingPieceModel)
        db.session.commit()

        # update processvisualisation
        processVisualisation.updateOrder()

        return stateWorkingPieceModel, 202


class BindToResource(Resource):
    resourceFields = {
        'id': fields.Integer,
        'task': fields.String,
        'assignedWorkingPiece': fields.Integer
    }

    @ marshal_with(resourceFields)
    def post(self, bindToResource):
        state = StateModel.query.first()
        if not state:
            abort(404, message="No state available")
        state.boundToResourceID = bindToResource
        db.session.add(state)
        db.session.commit()
        return state, 201

    @ marshal_with(resourceFields)
    def put(self, bindToResource):
        state = StateModel.query.first()
        if not state:
            abort(404, message="No state available")
        state.boundToResourceID = bindToResource
        db.session.add(state)
        db.session.commit()
        return state, 201

    @ marshal_with(resourceFields)
    def get(self, bindToResource):
        state = StateModel.query.first()
        if not state:
            abort(404, message="No state available")
        state.boundToResourceID = bindToResource
        db.session.add(state)
        db.session.commit()
        return state, 201


class AbortTask(Resource):
    resourceFields = {
        'id': fields.Integer,
        'state': fields.String,
        'boundToResourceID': fields.Integer,
        'ipAdress': fields.String,
        'baseLevelHeight': fields.Float
    }
