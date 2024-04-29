

-- CREATE TABLE drivers (
--     driver_id SERIAL PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     license_number VARCHAR(50) NOT NULL UNIQUE,
--     title VARCHAR(255),
--     id VARCHAR(255)
-- );



-- CREATE TABLE vehicles (
--     vehicle_id SERIAL PRIMARY KEY,
--     registration_number VARCHAR(50) NOT NULL UNIQUE,
--     make VARCHAR(50),
--     model VARCHAR(50),
--     year INT,
--     capacity INT CHECK (capacity >= 0),
--     driver_id INT,
--     FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
-- );


CREATE TABLE trips (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER NOT NULL,
    trip_id INTEGER NOT NULL,
    measurement_sequence INTEGER NOT NULL,
    measurement_time TIMESTAMP NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    fuel_capacity FLOAT NOT NULL,
    distance_traveled FLOAT NOT NULL,
    fuel_remaining_percent FLOAT NOT NULL,
    fuel_remaining_gallon FLOAT NOT NULL,
    color VARCHAR(50) NOT NULL
);


ALTER TABLE public."trips" REPLICA IDENTITY FULL;


drop view if exists latest_locations;
CREATE VIEW latest_locations AS
SELECT *
FROM trips AS t
WHERE (t.vehicle_id, t.trip_id, t.measurement_sequence) IN (
    SELECT vehicle_id, trip_id, MAX(measurement_sequence)
    FROM trips
    GROUP BY vehicle_id, trip_id
);



-- ALTER TABLE public."drivers" REPLICA IDENTITY FULL; -- This is necessary for kafka streaming to work
-- ALTER TABLE public."vehicles" REPLICA IDENTITY FULL;

