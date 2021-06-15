# Modulewide
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

from processvisualisation.processvisualisation import ProcessVisualisation # nopep8
from visualiser.visualiser import Visualiser # nopep8
visualiser = Visualiser()
processVisualisation = ProcessVisualisation(db)
