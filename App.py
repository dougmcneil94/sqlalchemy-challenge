import numpy as np
import pandas as pd
import datetime as dt
import sqlite3

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#print(Base.classes.keys())
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#create variable to store date as start_date - 1 year
prev_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
print("Date from 1 year - prev year date", prev_year_date)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/Welcome")
def welcome():
   return (
       f"Welcome to the Hawaii Climate Analysis API!<br/>"
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/temp/start<br/>"
       f"/api/v1.0/temp/start/end"
   )


@app.route("/api/v1.0/precipitation")
def precipitation():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    # Return the JSON representation of your dictionary.
    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)
   

@app.route("/api/v1.0/stations")
def stations():

    station_name = session.query(Station.station).all()
    stations = list(np.ravel(station_name))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the tobs
    ObsTemp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year).all()
    # Return the JSON representation of your dictionary.
    Temp = {date: tobs for date, tobs in ObsTemp}
    return jsonify(Temp)


@app.route("/api/v1.0/temp/<start>")
def start(start=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # calculate TMIN, TAVG, TMAX for dates greater than start
    StartTemp = session.query(*sel).filter(Measurement.date >= start).all()
    # Unravel StartTemp and convert to a list
    temps1 = list(np.ravel(StartTemp))
    return jsonify(temps1)


@app.route("/api/v1.0/temp/<start>/<end>")
def start_end(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # calculate TMIN, TAVG, TMAX for dates greater than start
    Start_EndTemp = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Unravel Start_EndTemp and convert to a list
    temps2 = list(np.ravel(Start_EndTemp))
    print(temps2)
    return jsonify(temps2)


if __name__ == "__main__":
    app.run(debug=True)
