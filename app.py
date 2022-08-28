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
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})

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
    /api/v1.0/date/start/end <br/>
    ''')

# Precipitation Route:
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Stations Route:
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations = stations)

# Monthly Temperature Route:
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Statistics Route:
@app.route("/api/v1.0/date/<start>")
@app.route("/api/v1.0/date/<start>/<end>")
def sttenddates(start=None, end=None):
    session = Session(engine)

    """* Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    * When given the start only or the start/end date, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
    # SELECT Statement
    sel = [func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]
    print("======================")
    print(*sel)
    print("======================")
    if not end:
        # calculate min, max, avg for dates greater than start
        # results = session.query(*sel).filter(Measurement.date >= start).all()

        results = session.query(func.min(Measurement.tobs), func.avg(
            Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    else:
        # calculate min, max, avg for dates between start and stop
        results = session.query(
            func.min(Measurement.tobs), func.avg(
                Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # unravel results into a 1D array and convert to list
    temps = list(np.ravel(results))

    session.close
    return jsonify(temps=temps)

if __name__ == "__main__":
    app.run(debug=True)