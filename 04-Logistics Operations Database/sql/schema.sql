-- ============================================================================
-- Logistics Operations Database — SQLite Schema
-- Three tables, three grains, one business problem per track.
-- Types are declared explicitly for readability; SQLite is dynamically typed.
-- All columns that are null in the source CSVs are declared without NOT NULL.
-- ============================================================================

DROP TABLE IF EXISTS master_driver_clean;
CREATE TABLE master_driver_clean (
    -- Identity and dates
    driver_id                 TEXT PRIMARY KEY,
    hire_date                 TEXT,
    termination_date          TEXT,      -- NULL = still employed (this is the target signal)
    driver_attrition          INTEGER,   -- TARGET (Track A): 1 = left, 0 = active

    -- Derived profile features
    hire_year                 INTEGER,
    age_at_hire               REAL,
    years_experience          INTEGER,
    cdl_class                 TEXT,
    employment_status         TEXT,
    home_terminal             TEXT,

    -- Monthly-metrics aggregates (NULL for the 26 leavers — structural property)
    n_months                  INTEGER,
    avg_on_time_rate          REAL,
    min_on_time_rate          REAL,
    avg_mpg                   REAL,
    total_trips_metered       INTEGER,
    total_miles               REAL,
    avg_idle_hours            REAL,
    n_low_ontime_months       INTEGER,
    has_low_ontime_month      INTEGER,

    -- Trip aggregates
    n_trips_assigned          INTEGER,
    total_distance            INTEGER,
    avg_idle_from_trips       REAL,
    avg_mpg_from_trips        REAL,

    -- Safety aggregates
    n_incidents               INTEGER,
    n_at_fault                INTEGER,
    n_preventable             INTEGER,
    total_claim               REAL
);


DROP TABLE IF EXISTS master_trip_clean;
CREATE TABLE master_trip_clean (
    -- Load identity
    load_id                   TEXT PRIMARY KEY,
    load_date                 TEXT,
    load_type                 TEXT,
    weight_lbs                INTEGER,
    pieces                    INTEGER,
    revenue                   REAL,
    fuel_surcharge            REAL,
    accessorial_charges       INTEGER,
    load_status               TEXT,
    booking_type              TEXT,

    -- Trip facts (driver_id/truck_id/trailer_id nullable ~2%)
    trip_id                   TEXT,
    driver_id                 TEXT,
    truck_id                  TEXT,
    trailer_id                TEXT,
    dispatch_date             TEXT,
    actual_distance_miles     INTEGER,
    actual_duration_hours     REAL,
    fuel_gallons_used         REAL,
    average_mpg               REAL,
    idle_time_hours           REAL,
    trip_status               TEXT,

    -- Route context
    route_id                  TEXT,
    origin_city               TEXT,
    destination_city          TEXT,
    typical_distance_miles    INTEGER,
    base_rate_per_mile        REAL,
    typical_transit_days      INTEGER,

    -- Customer context
    customer_id               TEXT,
    customer_type             TEXT,
    credit_terms_days         INTEGER,
    primary_freight_type      TEXT,

    -- Pickup events (features)
    pickup_on_time_flag       INTEGER,
    pickup_detention_minutes  REAL,
    pickup_late_flag          INTEGER,

    -- Delivery events
    delivery_on_time_flag     INTEGER,
    delivery_detention_minutes REAL,
    late_delivery_flag        INTEGER    -- TARGET (Track B): 1 = late, 0 = on time
);


DROP TABLE IF EXISTS master_truck_month_clean;
CREATE TABLE master_truck_month_clean (
    -- Composite identity
    truck_id                  TEXT,
    month                     TEXT,

    -- Utilization facts (all present in v1; nullable declared for safety)
    trips_completed           INTEGER,
    total_miles               INTEGER,
    total_revenue             REAL,
    average_mpg               REAL,
    maintenance_events        INTEGER,
    maintenance_cost          REAL,
    downtime_hours            REAL,
    utilization_rate          REAL,
    high_maintenance_flag     INTEGER,   -- TARGET (Track C): 1 = top quartile cost
    utilization_over_100pct   INTEGER,   -- anomaly flag

    -- Asset context
    make                      TEXT,
    model_year                INTEGER,
    acquisition_date          TEXT,
    acquisition_mileage       INTEGER,
    fuel_type                 TEXT,
    tank_capacity_gallons     INTEGER,
    status                    TEXT,
    home_terminal             TEXT,
    truck_age_years           REAL,

    -- Maintenance aggregates (nullable when no record that month)
    n_maintenance_records     INTEGER,
    n_preventive              INTEGER,
    avg_odometer              REAL,

    PRIMARY KEY (truck_id, month)
);