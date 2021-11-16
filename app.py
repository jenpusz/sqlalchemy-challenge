import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, json, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

##################################################
# Flask Routes
##################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes below:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[satrt_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[satrt_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
        f" Please put dates in 'YYYY-MM-DD' format <br/>"

    )

    @app.route("/api/v1.0/precipitation")
def precipitation():
    #Create a session from python to db
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()
    

    session.close()

    # Convert results to dictionary
    # Return the JSON representation of your dictionary

    all_precip = []
    for date,prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)   

    # Return a JSON list of stations from the dataset

    @app.route("/api/v1.0/stations")
    def station():
        session = Session(engine)

        results_station = session.query(Station.station, Station.name).all()

        return jsonify(results_station)

        session.close()

    # Query the dates and temperature observations of the most active station for the last year of data
    @app.route("/api/v1.0/tobs")
    def tobs():
        session = Session(engine)
        
        recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
        last_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)

        query_results = session.query(Measurement.tobs,Measurement.date ).\
        filter(Measurement.date >=last_year_date).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date <=recent_date).\
            order_by(Measurement.date).all()

        session.close()

    # Create Dictionary
    all_tobs = []
    for row in query_results:
       tobs_dict = {}
       tobs_dict["tobs"] = row.tobs
       tobs_dict["Date"] = row.date
       all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature
    # for a given start or start-end range

    @app.route("/api/v1.0/<start_date>")
    def temp_start_date(start_date):
        session = Session(engine)
        temp_min_max_avg = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start_date).all()

        session.close()
        all_tobs = []
        for row in min_max_avg_temp:
            tobs_temp_dict = {}
            tobs_temp_dict["min_tobs"] = row[0]
            tobs_temp_dict["max_tobs"] = row[1]
            tobs_temp_dict["avg_tobs"] = row[2]
            all_tobs.append(tobs_temp_dict)

       
    return jsonify(all_tobs)

    @app.route("/api/v1.0/<start_date>/<end_date>")
    def temp_start_end_date(start_date,end_date):
        session = Session(engine)
        temp_min_max_avg = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start_date)\
        .filter(Measurement.date <= end_date).all()
        session.close()
        all_tobs_range = []
        for row in min_max_avg_temp:
            tobs_range_dict = {}
            tobs_range_dict["min_tobs"] = row[0]
            tobs_range_dict["max_tobs"] = row[1]
            tobs_range_dict["avg_tobs"] = row[2]
            all_tobs_range.append(tobs_range_dict)

    return jsonify(all_tobs_range)

if __name__ == '__main__':
    app.run(debug=True)












