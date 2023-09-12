# 1. Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
# Create an app, 

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#Define what to do when a user hits the index route

# List all available routes

@app.route("/")
def welcome():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results from your precipitation analysis
    # (i.e. retrieve only the last 12 months of data) to a dictionary 
    # using date as the key and prcp as the value.

    # Calculate the date one year from the last date in data set. 
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    date_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    # precipitation_df = pd.DataFrame(date_precip, columns=['Date', 'Precipitation'])

    session.close()

    # Convert list of tuples into normal list
    daily_precip = list(np.ravel(date_precip))

    return jsonify(daily_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))


    return jsonify(all_names)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    date_temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(date_temp))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temps(start=None, end=None):
    #Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of the minimum temperature, 
    # the average temperature, and the maximum temperature for a specified start or start-end range.
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end: 
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
                filter(Measurement.date>=start).all()
        session.close()
    

    # Convert list of tuples into normal list
        json_tob = list(np.ravel(results))



        start = dt.datetime.strptime(start, "%m%d%Y")
        end = dt.datetime.strptime(end, "%m%d%Y")

    

    results = session.query(*sel).\
        filter(Measurement.date>=start).\
        filter(Measurement.date<=end).all()
# @app.route("/api/v1.0/<start>/<end>")
# def temps_range(startend):
#     #Create our session (link) from Python to the DB
#     session = Session(engine)

#     # For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    
#     begin_end = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= startend).all()
    
    
    session.close()
    
#     # Convert list of tuples into normal list
    json_tob = list(np.ravel(results))

    return jsonify(json_tob)

if __name__ == "__main__":
    app.run(debug=True)
