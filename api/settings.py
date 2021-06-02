# Modulewide
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

#IP_MES = "http://129.69.102.129"
IP_MES = "http://127.0.0.1"

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from processvisualisation.processvisualisation import ProcessVisualisation  # nopep8
processVisualisation = ProcessVisualisation(db)
