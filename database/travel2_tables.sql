CREATE TABLE IF NOT EXISTS "aircrafts_data" (
"aircraft_code" TEXT,
  "model" TEXT,
  "range" INTEGER
);
CREATE TABLE IF NOT EXISTS "airports_data" (
"airport_code" TEXT,
  "airport_name" TEXT,
  "city" TEXT,
  "coordinates" TEXT,
  "timezone" TEXT
);
CREATE TABLE IF NOT EXISTS "boarding_passes" (
"ticket_no" TEXT,
  "flight_id" INTEGER,
  "boarding_no" INTEGER,
  "seat_no" TEXT
);
CREATE TABLE IF NOT EXISTS "bookings" (
"book_ref" TEXT,
  "book_date" TIMESTAMP,
  "total_amount" INTEGER
);
CREATE TABLE IF NOT EXISTS "flights" (
"flight_id" INTEGER,
  "flight_no" TEXT,
  "scheduled_departure" TIMESTAMP,
  "scheduled_arrival" TIMESTAMP,
  "departure_airport" TEXT,
  "arrival_airport" TEXT,
  "status" TEXT,
  "aircraft_code" TEXT,
  "actual_departure" TIMESTAMP,
  "actual_arrival" TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "seats" (
"aircraft_code" TEXT,
  "seat_no" TEXT,
  "fare_conditions" TEXT
);
CREATE TABLE IF NOT EXISTS "ticket_flights" (
"ticket_no" TEXT,
  "flight_id" INTEGER,
  "fare_conditions" TEXT,
  "amount" INTEGER
);
CREATE TABLE IF NOT EXISTS "tickets" (
"ticket_no" TEXT,
  "book_ref" TEXT,
  "passenger_id" TEXT
);
CREATE TABLE IF NOT EXISTS "car_rentals" (
"id" INTEGER,
  "name" TEXT,
  "location" TEXT,
  "price_tier" TEXT,
  "start_date" TEXT,
  "end_date" TEXT,
  "booked" INTEGER
);
CREATE TABLE IF NOT EXISTS "hotels" (
"id" INTEGER,
  "name" TEXT,
  "location" TEXT,
  "price_tier" TEXT,
  "checkin_date" TEXT,
  "checkout_date" TEXT,
  "booked" INTEGER
);
CREATE TABLE IF NOT EXISTS "trip_recommendations" (
"id" INTEGER,
  "name" TEXT,
  "location" TEXT,
  "keywords" TEXT,
  "details" TEXT,
  "booked" INTEGER
);