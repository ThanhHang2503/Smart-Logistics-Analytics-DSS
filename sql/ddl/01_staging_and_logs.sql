-- ==============================================================================
-- SLADSS DDL Script 01: Staging Tables & Audit Logs
-- Smart Logistics Analytics & Decision Support System
-- Target: PostgreSQL 16+
-- Governance: Section 4.1, 5.2, 5.3 (.specify/memory/constitution.md)
-- ==============================================================================

-- 1. Create Dedicated Schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS marts;

-- ------------------------------------------------------------------------------
-- 2. Audit & Observability Tables (Section 5.2 & 5.3)
-- ------------------------------------------------------------------------------

-- 2.1 pipeline_run: Ghi nhận lịch sử mỗi chu trình thực thi pipeline
CREATE TABLE IF NOT EXISTS staging.pipeline_run (
    run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file TEXT,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED')),
    rows_read INTEGER DEFAULT 0,
    rows_valid INTEGER DEFAULT 0,
    rows_rejected INTEGER DEFAULT 0,
    rows_loaded INTEGER DEFAULT 0,
    error_detail TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE staging.pipeline_run IS 'Nhật ký thực thi chu trình ETL phục vụ giám sát và truy vết';

-- 2.2 data_quality_log: Lưu trữ chi tiết bản ghi lỗi, không âm thầm drop (Zero Silent Drop)
CREATE TABLE IF NOT EXISTS staging.data_quality_log (
    log_id BIGSERIAL PRIMARY KEY,
    run_id UUID REFERENCES staging.pipeline_run(run_id) ON DELETE CASCADE,
    source_file VARCHAR(100) NOT NULL,
    row_number INTEGER,
    rule_code VARCHAR(10) NOT NULL,    -- e.g. QC-001 -> QC-007
    column_name VARCHAR(100),
    raw_value TEXT,
    message TEXT NOT NULL,             -- Mô tả chi tiết lỗi vi phạm
    logged_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dq_log_run_id ON staging.data_quality_log(run_id);
CREATE INDEX IF NOT EXISTS idx_dq_log_rule ON staging.data_quality_log(rule_code);

COMMENT ON TABLE staging.data_quality_log IS 'Lưu trữ toàn bộ vi phạm chất lượng dữ liệu được phát hiện trong quá trình validation';

-- ------------------------------------------------------------------------------
-- 3. Staging Operational Tables (Raw Replication Layer)
-- ------------------------------------------------------------------------------

-- 3.1 staging.orders (Đơn hàng)
CREATE TABLE IF NOT EXISTS staging.orders (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_key VARCHAR(100) NOT NULL, -- Mã giả lập / Encrypted Mock
    product_id VARCHAR(50) NOT NULL,
    region_id VARCHAR(50) NOT NULL,
    carrier_id VARCHAR(50) NOT NULL,
    order_value NUMERIC(14, 2) NOT NULL,
    loaded_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3.2 staging.shipments (Lần giao hàng)
CREATE TABLE IF NOT EXISTS staging.shipments (
    shipment_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    carrier_id VARCHAR(50) NOT NULL,
    shipped_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    delivery_status VARCHAR(50) NOT NULL,
    delivery_attempts INTEGER DEFAULT 1,
    loaded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stg_shipments_order ON staging.shipments(order_id);

-- 3.3 staging.returns (Sự kiện hoàn trả)
CREATE TABLE IF NOT EXISTS staging.returns (
    return_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    return_date DATE NOT NULL,
    return_reason VARCHAR(255),
    return_status VARCHAR(50) NOT NULL,
    loaded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stg_returns_order ON staging.returns(order_id);

-- 3.4 staging.return_costs (Khoản chi phí phát sinh từ hoàn hàng)
CREATE TABLE IF NOT EXISTS staging.return_costs (
    cost_id VARCHAR(50) PRIMARY KEY,
    return_id VARCHAR(50) NOT NULL,
    cost_type VARCHAR(100) NOT NULL,
    amount NUMERIC(14, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'VND',
    loaded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stg_return_costs_return ON staging.return_costs(return_id);

-- 3.5 staging.products (Danh mục sản phẩm)
CREATE TABLE IF NOT EXISTS staging.products (
    product_id VARCHAR(50) PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    loaded_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3.6 staging.regions (Khu vực địa lý)
CREATE TABLE IF NOT EXISTS staging.regions (
    region_id VARCHAR(50) PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL,
    province_or_area VARCHAR(255),
    loaded_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3.7 staging.carriers (Đơn vị vận chuyển)
CREATE TABLE IF NOT EXISTS staging.carriers (
    carrier_id VARCHAR(50) PRIMARY KEY,
    carrier_name VARCHAR(100) NOT NULL,
    loaded_at TIMESTAMPTZ DEFAULT NOW()
);
