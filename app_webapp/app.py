#%%
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.sql import func
app = Flask(__name__)

#debug
print('printing env POSTGRES_HOST:', os.getenv('POSTGRES_HOST'), ' : done.')

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')


# Set up Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Trips model
class Trips(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, nullable=False)
    trip_id = db.Column(db.Integer, nullable=False)
    measurement_sequence = db.Column(db.Integer, nullable=False)
    measurement_time = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    fuel_capacity = db.Column(db.Integer, nullable=False)
    distance_traveled = db.Column(db.Float, nullable=False)
    fuel_remaining_percent = db.Column(db.Integer, nullable=False)
    fuel_remaining_gallon = db.Column(db.Float, nullable=False)
    color = db.Column(db.String, nullable=False)

# @app.route('/')
# def index():
#     # Retrieve all trips from the database
#     data = Trips.query.all()
#     return render_template('index.html', data=data)

@app.route('/')
def index():
    # Query the database for the latest data for each vehicle
    latest_trips_subquery = db.session.query(
    Trips.vehicle_id,
    func.max(Trips.measurement_time).label('max_measurement_time')
    ).group_by(Trips.vehicle_id).subquery()

    latest_trips = db.session.query(Trips).join(
        latest_trips_subquery,
        (Trips.vehicle_id == latest_trips_subquery.c.vehicle_id) &
        (Trips.measurement_time == latest_trips_subquery.c.max_measurement_time)
    ).all()
    return render_template('index.html', data=latest_trips)


@app.route('/submit', methods=['POST'])
def submit():
    # Insert a new trip into the database
    trip_data = {
        "vehicle_id": request.form['vehicle_id'],
        "trip_id": request.form['trip_id'],
        "measurement_sequence": request.form['measurement_sequence'],
        "measurement_time": request.form['measurement_time'],
        "latitude": request.form['latitude'],
        "longitude": request.form['longitude'],
        "fuel_capacity": request.form['fuel_capacity'],
        "distance_traveled": request.form['distance_traveled'],
        "fuel_remaining_percent": request.form['fuel_remaining_percent'],
        "fuel_remaining_gallon": request.form['fuel_remaining_gallon'],
        "color": request.form['color']
    }

    new_trip = Trips(**trip_data)

    with app.app_context():
        db.session.add(new_trip)
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables before running the app
    app.run( host='0.0.0.0', debug=True, port=5000)

#%%