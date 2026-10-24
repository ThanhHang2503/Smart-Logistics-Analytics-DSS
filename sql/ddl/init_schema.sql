-- ==============================================================================
-- SLADSS Database Schema Initialization
-- Smart Logistics Analytics & Decision Support System
-- Target: PostgreSQL / Relational Data Warehouse
-- Governance: Section 4 (.specify/memory/constitution.md)
-- ==============================================================================

-- 1. Create Schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS marts;

-- ------------------------------------------------------------------------------
-- 2. Staging Tables (Operational Raw Replica)
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS staging.stg_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_key VARCHAR(100) NOT NULL, -- Encrypted/synthetic mock identifier
    product_id VARCHAR(50) NOT NULL,
    region_id VARCHAR(50) NOT NULL,
    carrier_id VARCHAR(50) NOT NULL,
    order_value NUMERIC(12, 2) NOT NULL CHECK (order_value >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.stg_shipments (
    shipment_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    carrier_id VARCHAR(50) NOT NULL,
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP,
    delivery_status VARCHAR(50) NOT NULL,
    delivery_attempts INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.stg_returns (
    return_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    return_date DATE NOT NULL,
    return_reason VARCHAR(100),
    return_status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.stg_return_costs (
    cost_id VARCHAR(50) PRIMARY KEY,
    return_id VARCHAR(50) NOT NULL,
    cost_type VARCHAR(50) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount >= 0),
    currency VARCHAR(10) DEFAULT 'VND',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.stg_products (
    product_id VARCHAR(50) PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.stg_regions (
    region_id VARCHAR(50) PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL,
    province_or_area VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.stg_carriers (
    carrier_id VARCHAR(50) PRIMARY KEY,
    carrier_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pipeline & Data Quality Tracking
CREATE TABLE IF NOT EXISTS staging.data_quality_log (
    log_id SERIAL PRIMARY KEY,
    run_id VARCHAR(50),
    source_file VARCHAR(100),
    row_number INT,
    rule_code VARCHAR(50),
    message TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.pipeline_run (
    run_id SERIAL PRIMARY KEY,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    rows_read INT DEFAULT 0,
    rows_loaded INT DEFAULT 0
);

-- ------------------------------------------------------------------------------
-- 3. Star Schema Dimension Tables (warehouse schema)
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key INT PRIMARY KEY,
    date DATE NOT NULL,
    day INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouse.dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    category VARCHAR(100) NOT NULL,
    product_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouse.dim_carrier (
    carrier_key SERIAL PRIMARY KEY,
    carrier_id VARCHAR(50) NOT NULL,
    carrier_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouse.dim_region (
    region_key SERIAL PRIMARY KEY,
    region_id VARCHAR(50) NOT NULL,
    region_name VARCHAR(100) NOT NULL,
    province_or_area VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS warehouse.dim_return_reason (
    reason_key SERIAL PRIMARY KEY,
    return_reason VARCHAR(100) NOT NULL
);

-- ------------------------------------------------------------------------------
-- 4. Star Schema Fact Tables (Grain Enforced)
-- ------------------------------------------------------------------------------

-- Grain: 1 row = 1 order
CREATE TABLE IF NOT EXISTS warehouse.fact_orders (
    order_key SERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL UNIQUE,
    order_date_key INT REFERENCES warehouse.dim_date(date_key),
    customer_key VARCHAR(100) NOT NULL, -- Synthetic Mock
    product_key INT REFERENCES warehouse.dim_product(product_key),
    region_key INT REFERENCES warehouse.dim_region(region_key),
    carrier_key INT REFERENCES warehouse.dim_carrier(carrier_key),
    order_value NUMERIC(12, 2) NOT NULL CHECK (order_value >= 0)
);

-- Grain: 1 row = 1 shipment event
CREATE TABLE IF NOT EXISTS warehouse.fact_shipments (
    shipment_key SERIAL PRIMARY KEY,
    shipment_id VARCHAR(50) NOT NULL UNIQUE,
    order_key INT REFERENCES warehouse.fact_orders(order_key),
    carrier_key INT REFERENCES warehouse.dim_carrier(carrier_key),
    delivery_status VARCHAR(50) NOT NULL,
    delivery_attempts INT DEFAULT 1
);

-- Grain: 1 row = 1 return event
CREATE TABLE IF NOT EXISTS warehouse.fact_returns (
    return_key SERIAL PRIMARY KEY,
    return_id VARCHAR(50) NOT NULL UNIQUE,
    order_key INT REFERENCES warehouse.fact_orders(order_key),
    return_date_key INT REFERENCES warehouse.dim_date(date_key),
    reason_key INT REFERENCES warehouse.dim_return_reason(reason_key),
    return_status VARCHAR(50) NOT NULL
);

-- Grain: 1 row = 1 return cost item
CREATE TABLE IF NOT EXISTS warehouse.fact_return_costs (
    cost_key SERIAL PRIMARY KEY,
    cost_id VARCHAR(50) NOT NULL UNIQUE,
    return_key INT REFERENCES warehouse.fact_returns(return_key),
    cost_type VARCHAR(50) NOT NULL,
    cost_amount NUMERIC(12, 2) NOT NULL CHECK (cost_amount >= 0),
    currency VARCHAR(10) DEFAULT 'VND'
);
