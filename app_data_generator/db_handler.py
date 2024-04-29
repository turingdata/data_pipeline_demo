import logging
import os
import uuid
from sqlalchemy import Float, create_engine, Column, Integer, String, DateTime, Text, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from contextlib import contextmanager

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

def uuid_gen():
    return str(uuid.uuid4())


class DatabaseHandler:
    def __init__(self):
        self.DATABASE_ENGINE = os.environ.get('DATABASE_ENGINE', "postgresql")
        self.DATABASE_ROOT_PASSWORD = os.environ.get('DATABASE_ROOT_PASSWORD', "password")
        self.DATABASE_NAME = os.environ.get('DATABASE_NAME', "postgres")
        self.DATABASE_USER = os.environ.get('DATABASE_USER', "admin")
        self.DATABASE_HOST = os.environ.get('DATABASE_HOST', "localhost")
        self.DATABASE_PORT = os.environ.get('DATABASE_PORT', "5433")
        self.DATABASE_URL = f'{self.DATABASE_ENGINE}://{self.DATABASE_USER}:{self.DATABASE_ROOT_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'
        
        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(bind=self.engine)

        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def add_session(self, user_id):
        with self.get_session() as session:
            new_state = Sessions(
                user_id=user_id,
            )

            session.add(new_state)
            session.commit()


    def add_trip(self, trip_data):
        """
        Adds a row to the trips table with the provided data.
        """
        with self.get_session() as session:
            # Truncate the trips table
            # session.execute(text('TRUNCATE TABLE public.trips;'))
            # session.commit()

            # Add the new trip row
            new_trip = Trips(**trip_data)
            session.add(new_trip)
            session.commit()


    def execute(self, query):
        """
        Adds a row to the trips table with the provided data.
        """
        with self.get_session() as session:
            session.execute(text(query))
            session.commit()


    def create_view_trip(self):
        """
        Adds a row to the trips table with the provided data.
        """
        with self.get_session() as session:
            # Truncate the trips table
            session.execute(text('''drop view if exists latest_locations;
                                    CREATE VIEW latest_locations AS
                                    SELECT *
                                    FROM trips AS t
                                    WHERE (t.vehicle_id, t.trip_id, t.measurement_sequence) IN (
                                        SELECT vehicle_id, trip_id, MAX(measurement_sequence)
                                        FROM trips
                                        GROUP BY vehicle_id, trip_id
                                    );'''))
            session.commit()

class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), default=uuid_gen, nullable=False)
    user_id = Column(Integer, nullable=False)


class Trips(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, nullable=False)
    trip_id = Column(Integer, nullable=False)
    measurement_sequence = Column(Integer, nullable=False)
    measurement_time = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    fuel_capacity = Column(Integer, nullable=False)
    distance_traveled = Column(Float, nullable=False)
    fuel_remaining_percent = Column(Integer, nullable=False)
    fuel_remaining_gallon = Column(Float, nullable=False)
    color = Column(String, nullable=False)

