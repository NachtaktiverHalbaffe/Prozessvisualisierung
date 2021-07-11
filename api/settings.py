"""
Filename: settings.py
Version name: 1.0, 2021-07-10
Short description: system wide settings and instances

(C) 2003-2021 IAS, Universitaet Stuttgart

"""


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# Flask settings
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# setup systemwide objects of processvisualisation and visualiser
# with which each visualisation task gets executed
from processvisualisation.processvisualisation import ProcessVisualisation  # nopep8
from visualiser.visualiser import Visualiser  # nopep8
visualiser = Visualiser()
processVisualisation = ProcessVisualisation(db)
