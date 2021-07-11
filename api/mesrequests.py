"""
Filename: mesrequests.py
Version name: 1.0, 2021-07-10
Short description: Common http requests to or from the mes

(C) 2003-2021 IAS, Universitaet Stuttgart

"""


import requests
from constants import IP_MES, STREAM_HANDLER,  FILE_HANDLER_ERROR
import logging
# setup logger
errorLogger = logging.getLogger("error")
errorLogger.setLevel(logging.WARNING)
# add logger handler to logger
errorLogger.handlers = []
errorLogger.addHandler(STREAM_HANDLER)
errorLogger.addHandler(FILE_HANDLER_ERROR)


# send error to mes
# @params:
#   msg: message of error
#   level: level of error
#   category: category of error
def sendError(msg, level="[WARNING]", category="Operational issue"):
    data = {
        "msg": msg,
        "category": category,
        "level": level,
        "isSolved": True
    }
    try:
        request = requests.post(IP_MES+":8000/api/Error/", data=data)
        if not request.ok:
            errorLogger.warning("[MESREQUESTS] " + request.status_code)
    except Exception as e:
        errorLogger.warning(
            "[MESREQUESTS] Couldn't send error to MES. Check Connection")


# get the state of an specific workingpiece
# @params:
#   id: id of requested workingpiece
def getStateWorkingPiece(id):
    from models import StateWorkingPieceModel
    from settings import db
    try:
        request = requests.get(
            IP_MES + ":8000/api/StateWorkingPiece/" + str(id))
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
    except Exception as e:
        errorLogger.warning(
            "[MESREQUESTS] Couldn't get StateWorkingPiece from MES. Check Connection")


# get the state of an specific resource
# @params:
#   id: id of requested resource
def getStatePLC(id):
    try:
        request = requests.get(
            IP_MES + ":8000/api/StatePLC/" + str(id))
        if request.ok:
            data = request.json()
            return data
    except Exception as e:
        errorLogger.warning(
            "[MESREQUESTS] Couldn't get StatePLC from MES. Check Connection")


# update state of the visualisation unit in mes
# @params:
#   id: id of the visualisation unit
#   data: data to send. Must be an dictionary
def updateStateVisualisationUnit(id, data):
    try:
        request = requests.post(
            IP_MES+":8000/api/StateVisualisationUnit/", data=data)
        if not request.ok:
            # already exists => update it
            try:
                request = requests.patch(
                    IP_MES+":8000/api/StateVisualisationUnit/" + str(id), data=data)
                if not request.ok:
                    errorLogger.warning("[MESREQUESTS] " + request.status_code)
            except Exception as e:
                errorLogger.warning(
                    "[MESREQUESTS] Couldn't update StateVisualisationUnit in MES. Check Connection")
    except Exception as e:
        pass


# delete state of a visualisation unit in mes
# @params:
#   id: id of the visualisation unit
def deleteStateVisualisationUnit(id):
    try:
        request = requests.delete(
            IP_MES+":8000/api/StateVisualisationUnit/" + str(id))
        if not request.ok:
            errorLogger.warning("[MESREQUESTS] " + request.status_code)
    except Exception as e:
        errorLogger.warning(e)


# update state of an workingpiece in mes
# @params:
#   id: id of the workingpiece
#   data: data to send. must be an dicitionary
def updateStateWorkingPiece(id, data):
    try:
        request = requests.patch(
            IP_MES + ":8000/api/StateWorkingPiece/" + str(id), data=data)
        if not request.ok:
            errorLogger.warning("[MESREQUESTS] " + request.status_code)
    except Exception as e:
        errorLogger.warning(
            "[MESREQUESTS] Couldn't update StateWorkingPiece in MES. Check Connection")
