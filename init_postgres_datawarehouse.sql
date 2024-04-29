
CREATE SCHEMA schema_datawarehouse_landingzone;


drop table if exists schema_datawarehouse_landingzone.raw_trips CASCADE;

CREATE TABLE schema_datawarehouse_landingzone.raw_trips (
	id int4 NOT NULL,
	vehicle_id int4 NOT NULL,
	trip_id int4 NOT NULL,
	measurement_sequence int4 NOT NULL,
	measurement_time timestamp NOT NULL,
	latitude float8 NOT NULL,
	longitude float8 NOT NULL,
	fuel_capacity float8 NOT NULL,
	distance_traveled float8 NOT NULL,
	fuel_remaining_percent float8 NOT NULL,
	fuel_remaining_gallon float8 NOT NULL,
	color varchar(50) NOT NULL,
	loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

drop view if exists schema_datawarehouse_landingzone.latest_locations CASCADE;

CREATE VIEW schema_datawarehouse_landingzone.latest_locations AS
SELECT *
FROM schema_datawarehouse_landingzone.raw_trips AS t
WHERE (t.vehicle_id, t.trip_id, t.measurement_sequence) IN (
    SELECT vehicle_id, trip_id, MAX(measurement_sequence)
    FROM schema_datawarehouse_landingzone.raw_trips
    GROUP BY vehicle_id, trip_id
);