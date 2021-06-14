"""
Filename: mesrequests.py
Version name: 0.1, 2021-06-14
Short description: Common http requests to or from the mes

(C) 2003-2021 IAS, Universitaet Stuttgart

"""


import requests
from constants import IP_MES


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
            print(request.status_code)
    except Exception as e:
        print("[PROCESSVISUALISATION] Couldn't send error to MES. Check Connection")


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
        print(e)

def updateStateVisualisationUnit(id, data):
    try:
        request = requests.patch(
            IP_MES + ":8000/api/StateVisualisationUnit/" + str(id), data=data)
        if not request.ok:
            print(request.status_code)
    except Exception as e:
            print(e)

def updateStateWorkingPiece(id, data):
    try:
        request = requests.patch(
            IP_MES + ":8000/api/StateWorkingPiece/" + str(id), data=data)
        if not request.ok:
            print(request.status_code)
    except Exception as e:
            print(e)
