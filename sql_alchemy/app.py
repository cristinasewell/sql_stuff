from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
Station = Base.classes.station

#################################################
# Database Setup
# #################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a dictionary
    # using date as the key and prcp as the value.
    # Return the JSON representation of your dictionary.

    # Calculate the date one year from the last date in data set.
    # lastest date found above
    # 2017-08-23
    # find the date of an year ago from last date
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    precipitation = (session.query(Measurement.date, Measurement.prcp
                                ).filter(Measurement.date >= query_date, Measurement.prcp != None
                                        ).order_by(Measurement.date).all())
    session.close()
    return jsonify(dict(precipitation))

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    total = session.query(Station.station).count()
    most_active = session.query(Measurement.station, func.count(Measurement.station)).\
                        group_by(Measurement.station).\
                        order_by(func.count(Measurement.station).desc()).all()
    session.close()
    return jsonify(dict(most_active)) 

@app.route("/api/v1.0/tobs")
def tobs():
    # lastest date found above
    # 2017-08-23
    # find the date of an year ago from last date
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    session = Session(engine)
    temps = session.query(Measurement.tobs).\
      filter(Measurement.date >= query_date, Measurement.station == 'USC00519281').\
      order_by(Measurement.tobs).all()

    session.close()

    results_list = []
    for t in temps:
        results_dict = {"tobs": t.tobs}
        results_list.append(results_dict)
    return jsonify(results_list)


@app.route("/api/v1.0/<start>")
def calc_temps(start):
    session = Session(engine)
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    temps = list(np.ravel(temps))
    session.close()
    print(temps)
    temp_dict = {"Min": temps[0], "Max": temps[1], "Avg": temps[2]}
    return jsonify(temp_dict)
    

@app.route("/api/v1.0/<start>/<end>")
def calc_temps_start_end(start, end):
    session = Session(engine)
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    temps = list(np.ravel(temps))
    session.close()
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)