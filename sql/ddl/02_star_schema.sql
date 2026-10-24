-- ==============================================================================
-- SLADSS DDL Script 02: Analytical Data Warehouse Star Schema
-- Smart Logistics Analytics & Decision Support System
-- Target: PostgreSQL 16+
-- Governance: Section 4.2 (Grain Definitions BẤT BIẾN)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Dimension Tables (warehouse schema)
-- ------------------------------------------------------------------------------

-- 1.1 dim_date (Chiều thời gian)
CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key INT PRIMARY KEY,               -- Format: YYYYMMDD
    date DATE NOT NULL UNIQUE,
    day INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    day_of_week INT NOT NULL,               -- 1 (Thứ hai) - 7 (Chủ nhật)
    day_name VARCHAR(20) NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL DEFAULT FALSE
);

COMMENT ON TABLE warehouse.dim_date IS 'Chiều ngày chuẩn hóa phục vụ phân tích theo thời gian';

-- 1.2 dim_product (Chiều sản phẩm)
CREATE TABLE IF NOT EXISTS warehouse.dim_product (
    product_key SERIAL PRIMARY KEY,         -- Khóa đại diện (Surrogate Key)
    product_id VARCHAR(50) NOT NULL UNIQUE, -- Khóa nghiệp vụ (Business Key)
    category VARCHAR(100) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE warehouse.dim_product IS 'Chiều sản phẩm và danh mục ngành hàng';

-- 1.3 dim_region (Chiều khu vực địa lý)
CREATE TABLE IF NOT EXISTS warehouse.dim_region (
    region_key SERIAL PRIMARY KEY,
    region_id VARCHAR(50) NOT NULL UNIQUE,
    region_name VARCHAR(100) NOT NULL,
    province_or_area VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE warehouse.dim_region IS 'Chiều khu vực địa lý giao hàng';

-- 1.4 dim_carrier (Chiều đơn vị vận chuyển)
CREATE TABLE IF NOT EXISTS warehouse.dim_carrier (
    carrier_key SERIAL PRIMARY KEY,
    carrier_id VARCHAR(50) NOT NULL UNIQUE,
    carrier_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE warehouse.dim_carrier IS 'Chiều đơn vị vận chuyển (3PL / logistics)';

-- 1.5 dim_return_reason (Chiều lý do hoàn hàng)
CREATE TABLE IF NOT EXISTS warehouse.dim_return_reason (
    reason_key SERIAL PRIMARY KEY,
    return_reason VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE warehouse.dim_return_reason IS 'Chiều danh mục lý do trả hàng chuẩn hóa';

-- ------------------------------------------------------------------------------
-- 2. Fact Tables (Bảo toàn mức chi tiết Grain - BẤT BIẾN)
-- ------------------------------------------------------------------------------

-- 2.1 fact_orders
-- GRAIN: 1 dòng = 1 đơn hàng (1 row per order)
CREATE TABLE IF NOT EXISTS warehouse.fact_orders (
    order_key SERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL UNIQUE,   -- Business Key
    order_date_key INT NOT NULL REFERENCES warehouse.dim_date(date_key),
    customer_key VARCHAR(100) NOT NULL,     -- Synthetic Mock UUID
    product_key INT NOT NULL REFERENCES warehouse.dim_product(product_key),
    region_key INT NOT NULL REFERENCES warehouse.dim_region(region_key),
    carrier_key INT NOT NULL REFERENCES warehouse.dim_carrier(carrier_key),
    order_value NUMERIC(14, 2) NOT NULL CHECK (order_value >= 0),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fact_orders_date ON warehouse.fact_orders(order_date_key);
CREATE INDEX IF NOT EXISTS idx_fact_orders_carrier ON warehouse.fact_orders(carrier_key);
CREATE INDEX IF NOT EXISTS idx_fact_orders_product ON warehouse.fact_orders(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_orders_region ON warehouse.fact_orders(region_key);

COMMENT ON TABLE warehouse.fact_orders IS 'Fact đơn hàng (Grain: 1 dòng / 1 order)';

-- 2.2 fact_shipments
-- GRAIN: 1 dòng = 1 lần giao hàng (1 row per shipment attempt/event)
CREATE TABLE IF NOT EXISTS warehouse.fact_shipments (
    shipment_key SERIAL PRIMARY KEY,
    shipment_id VARCHAR(50) NOT NULL UNIQUE,
    order_key INT NOT NULL REFERENCES warehouse.fact_orders(order_key),
    carrier_key INT NOT NULL REFERENCES warehouse.dim_carrier(carrier_key),
    shipped_date_key INT REFERENCES warehouse.dim_date(date_key),
    delivered_date_key INT REFERENCES warehouse.dim_date(date_key),
    delivery_status VARCHAR(50) NOT NULL,   -- e.g. 'delivered', 'delivery_failed', 'in_transit'
    delivery_attempts INTEGER NOT NULL DEFAULT 1 CHECK (delivery_attempts >= 1),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fact_shipments_order ON warehouse.fact_shipments(order_key);
CREATE INDEX IF NOT EXISTS idx_fact_shipments_carrier ON warehouse.fact_shipments(carrier_key);
CREATE INDEX IF NOT EXISTS idx_fact_shipments_status ON warehouse.fact_shipments(delivery_status);

COMMENT ON TABLE warehouse.fact_shipments IS 'Fact vận chuyển (Grain: 1 dòng / 1 shipment)';

-- 2.3 fact_returns
-- GRAIN: 1 dòng = 1 sự kiện hoàn hàng (1 row per return event)
CREATE TABLE IF NOT EXISTS warehouse.fact_returns (
    return_key SERIAL PRIMARY KEY,
    return_id VARCHAR(50) NOT NULL UNIQUE,
    order_key INT NOT NULL REFERENCES warehouse.fact_orders(order_key),
    return_date_key INT NOT NULL REFERENCES warehouse.dim_date(date_key),
    reason_key INT NOT NULL REFERENCES warehouse.dim_return_reason(reason_key),
    return_status VARCHAR(50) NOT NULL,     -- e.g. 'completed', 'processing', 'rejected'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fact_returns_order ON warehouse.fact_returns(order_key);
CREATE INDEX IF NOT EXISTS idx_fact_returns_date ON warehouse.fact_returns(return_date_key);
CREATE INDEX IF NOT EXISTS idx_fact_returns_reason ON warehouse.fact_returns(reason_key);

COMMENT ON TABLE warehouse.fact_returns IS 'Fact hoàn hàng (Grain: 1 dòng / 1 return event)';

-- 2.4 fact_return_costs
-- GRAIN: 1 dòng = 1 khoản chi phí phát sinh từ hoàn hàng (1 row per cost line)
CREATE TABLE IF NOT EXISTS warehouse.fact_return_costs (
    cost_key SERIAL PRIMARY KEY,
    cost_id VARCHAR(50) NOT NULL UNIQUE,
    return_key INT NOT NULL REFERENCES warehouse.fact_returns(return_key) ON DELETE CASCADE,
    cost_type VARCHAR(100) NOT NULL,
    cost_amount NUMERIC(14, 2) NOT NULL CHECK (cost_amount >= 0),
    currency VARCHAR(10) NOT NULL DEFAULT 'VND',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fact_return_costs_return ON warehouse.fact_return_costs(return_key);
CREATE INDEX IF NOT EXISTS idx_fact_return_costs_type ON warehouse.fact_return_costs(cost_type);

COMMENT ON TABLE warehouse.fact_return_costs IS 'Fact chi phí hoàn trả (Grain: 1 dòng / 1 cost item)';
