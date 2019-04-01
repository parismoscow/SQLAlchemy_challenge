import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, distinct
from flask import Flask, jsonify
import datetime as dt

import pandas as pd
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
           f"Available Routes:<br/>"
           f"/api/v1.0/precipitation<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/start_date<br/>"
           f"/api/v1.0/start_date/end_date"
       )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    sel = [
       
       (Measurement.date).label("Date"), 
       (Measurement.prcp).label("Percipitation"), 
       ]
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date_dt = pd.to_datetime(max_date)
    year_ago = max_date_dt - dt.timedelta(days=365)
    year_ago_str = year_ago.strftime("%Y-%m-%d")[0]
    prcp = session.query(*sel).\
       filter(Measurement.date >= year_ago_str).\
       order_by(Measurement.date).\
       all()
    p_dict = dict(prcp)
    #print()
    #print("Results for Precipitation")
    return jsonify(p_dict)

@app.route("/api/v1.0/stations")
def station():
    
    station_totals = session.query(Station.station)\
    .order_by(Station.station).all() 
    print()
    print("Station List:")   
    for row in station_totals:
        print (row[0])
    return jsonify(station_totals)
@app.route("/api/v1.0/tobs")
def tobs():
    
    temp_obs = session.query(Measurement.tobs)\
    .order_by(Measurement.date).all()
    print()
    print("Temperature Results for All Stations")
    return jsonify(temp_obs)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
       session = Session(engine)
       
       sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
       
       result = session.query(*sel).\
              filter(Measurement.date >= '2015-06-15').\
              all()
       
       return jsonify(result)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
       session = Session(engine)
       
       sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
       
       result = session.query(*sel).\
              filter(Measurement.date >= '2015-06-15').\
              filter(Measurement.date <= '2015-06-30').\
              group_by(Measurement.date).\
              all()
       
       return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
           