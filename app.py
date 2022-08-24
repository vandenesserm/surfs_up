#Import Dependencies:
import datetime as dt
import numpy as np
import pandas as pd

#Import dependencies from SQLAlchemy:
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import dependencies for Flask:
from flask import Flask, jsonify


#Set Up the Db:
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references & session link:
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Set Up Flask:
app = Flask(__name__)

# welcome route:
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes: <br/>
    /api/v1.0/precipitation <br/>
    /api/v1.0/stations <br/>
    /api/v1.0/tobs <br/>
    /api/v1.0/temp/start/end <br/>
    ''')

if __name__ == '__main__':
   app.run()