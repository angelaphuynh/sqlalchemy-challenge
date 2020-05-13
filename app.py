from flask import Flask, jsonify
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# reflect database into ORM clases
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session
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
        f"Avalable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end></br>"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
# Query for the dates and precipitation from the last year.
    results_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
# Convert the query results to a Dictionary using date as the key and prcp as the value.
    prcp_dict = dict(results_prcp)
# Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations(): 
    # Query stations
    results_stations =  session.query(Measurement.station).group_by(Measurement.station).all()
    # Return a JSON list of stations from the dataset.
    stations_list = list(np.ravel(results_stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def temperature():
# Query for the dates and temperature observations from a year from the last data point.
    results_tobs = session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
# Return a JSON list of Temperature Observations (tobs) for the previous year.
    tobs_list = list(results_tobs)
    return jsonify(tobs_list)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

@app.route("/api/v1.0/<start>")
def start(start=None):
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    from_start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2016-06-03').group_by(Measurement.date).all()
    from_start_list=list(from_start)
    return jsonify(from_start_list) 

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    between_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2016-06-03').filter(Measurement.date <= '2016-06-13').group_by(Measurement.date).all()
    between_dates_list=list(between_dates)
    return jsonify(between_dates_list)

if __name__ == '__main__':
    app.run(debug=True)
