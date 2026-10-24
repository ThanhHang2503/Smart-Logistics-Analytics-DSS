-- ==============================================================================
-- SLADSS Data Marts: Analytical KPI Views for Power BI & Executive Reports
-- Governance:
--   1. Hard Constraint #1: Grain Integrity & Anti-Fanout (Pre-aggregation before JOIN)
--   2. Hard Constraint: Zero Division Protection via NULLIF(denominator, 0)
-- Target: PostgreSQL 16+ / Analytical Marts
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- View 1: marts.v_carrier_performance
-- Description: Đánh giá hiệu suất đơn vị vận chuyển theo tháng (Tỷ lệ thất bại, hoàn, chi phí)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW marts.v_carrier_performance AS
WITH carrier_orders AS (
    -- Grain: 1 dòng / carrier_key, year, month
    SELECT
        fo.carrier_key,
        d.year,
        d.month,
        COUNT(fo.order_key) AS total_orders,
        SUM(fo.order_value) AS total_gross_value
    FROM warehouse.fact_orders fo
    JOIN warehouse.dim_date d ON fo.order_date_key = d.date_key
    GROUP BY fo.carrier_key, d.year, d.month
),
carrier_shipments AS (
    -- Grain: 1 dòng / carrier_key, year, month
    SELECT
        fs.carrier_key,
        d.year,
        d.month,
        COUNT(fs.shipment_key) AS total_shipments,
        COUNT(CASE WHEN fs.delivery_status = 'delivered' THEN 1 END) AS delivered_shipments,
        COUNT(CASE WHEN fs.delivery_status = 'delivery_failed' THEN 1 END) AS failed_shipments,
        ROUND(AVG(fs.delivery_attempts), 2) AS avg_delivery_attempts
    FROM warehouse.fact_shipments fs
    JOIN warehouse.dim_date d ON COALESCE(fs.delivered_date_key, fs.shipped_date_key) = d.date_key
    GROUP BY fs.carrier_key, d.year, d.month
),
carrier_returns_and_costs AS (
    -- Pre-aggregate costs to order level first to prevent fanout!
    -- Step 1: Total cost per return event
    -- Step 2: Rollup to carrier and date grain
    SELECT
        fo.carrier_key,
        d.year,
        d.month,
        COUNT(DISTINCT fr.order_key) AS returned_orders,
        COALESCE(SUM(frc.cost_amount), 0) AS total_return_cost
    FROM warehouse.fact_returns fr
    JOIN warehouse.fact_orders fo ON fr.order_key = fo.order_key
    JOIN warehouse.dim_date d ON fr.return_date_key = d.date_key
    LEFT JOIN warehouse.fact_return_costs frc ON fr.return_key = frc.return_key
    GROUP BY fo.carrier_key, d.year, d.month
)
SELECT
    co.year,
    co.month,
    dc.carrier_id,
    dc.carrier_name,
    -- Volume metrics
    co.total_orders,
    COALESCE(cs.total_shipments, 0) AS total_shipments,
    COALESCE(cs.delivered_shipments, 0) AS delivered_shipments,
    COALESCE(cs.failed_shipments, 0) AS failed_shipments,
    COALESCE(crc.returned_orders, 0) AS returned_orders,
    
    -- Quality & KPI Metrics (Safe Division)
    ROUND(
        (COALESCE(cs.failed_shipments, 0) * 100.0 / NULLIF(cs.total_shipments, 0)),
        2
    ) AS failure_rate_pct,
    ROUND(
        (COALESCE(crc.returned_orders, 0) * 100.0 / NULLIF(co.total_orders, 0)),
        2
    ) AS return_rate_pct,
    COALESCE(cs.avg_delivery_attempts, 1.0) AS avg_delivery_attempts,

    -- Financial Metrics
    co.total_gross_value,
    COALESCE(crc.total_return_cost, 0) AS total_return_cost,
    ROUND(
        COALESCE(crc.total_return_cost, 0) * 1.0 / NULLIF(crc.returned_orders, 0),
        2
    ) AS avg_cost_per_return,
    ROUND(
        (COALESCE(crc.total_return_cost, 0) * 100.0 / NULLIF(co.total_gross_value, 0)),
        2
    ) AS return_cost_to_value_pct

FROM carrier_orders co
JOIN warehouse.dim_carrier dc ON co.carrier_key = dc.carrier_key
LEFT JOIN carrier_shipments cs 
    ON co.carrier_key = cs.carrier_key 
    AND co.year = cs.year 
    AND co.month = cs.month
LEFT JOIN carrier_returns_and_costs crc 
    ON co.carrier_key = crc.carrier_key 
    AND co.year = crc.year 
    AND co.month = crc.month;

-- ------------------------------------------------------------------------------
-- View 2: marts.v_monthly_product_returns
-- Description: Tỷ lệ hoàn và chi phí phát sinh theo Danh mục sản phẩm & Tháng
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW marts.v_monthly_product_returns AS
WITH product_orders AS (
    -- Grain: 1 dòng / product_key, year, month
    SELECT
        fo.product_key,
        d.year,
        d.month,
        COUNT(fo.order_key) AS total_orders,
        SUM(fo.order_value) AS total_sales
    FROM warehouse.fact_orders fo
    JOIN warehouse.dim_date d ON fo.order_date_key = d.date_key
    GROUP BY fo.product_key, d.year, d.month
),
product_returns AS (
    -- Pre-aggregate to order_key grain first
    SELECT
        fo.product_key,
        d.year,
        d.month,
        COUNT(DISTINCT fr.order_key) AS returned_orders,
        COALESCE(SUM(frc.cost_amount), 0) AS total_return_cost
    FROM warehouse.fact_returns fr
    JOIN warehouse.fact_orders fo ON fr.order_key = fo.order_key
    JOIN warehouse.dim_date d ON fr.return_date_key = d.date_key
    LEFT JOIN warehouse.fact_return_costs frc ON fr.return_key = frc.return_key
    GROUP BY fo.product_key, d.year, d.month
)
SELECT
    po.year,
    po.month,
    dp.category,
    dp.product_id,
    dp.product_name,
    po.total_orders,
    COALESCE(pr.returned_orders, 0) AS returned_orders,
    
    -- Safe division for return rate
    ROUND(
        (COALESCE(pr.returned_orders, 0) * 100.0 / NULLIF(po.total_orders, 0)),
        2
    ) AS return_rate_pct,
    
    po.total_sales,
    COALESCE(pr.total_return_cost, 0) AS total_return_cost,
    
    -- Safe division for avg return cost
    ROUND(
        COALESCE(pr.total_return_cost, 0) * 1.0 / NULLIF(pr.returned_orders, 0),
        2
    ) AS avg_return_cost,
    ROUND(
        (COALESCE(pr.total_return_cost, 0) * 100.0 / NULLIF(po.total_sales, 0)),
        2
    ) AS return_cost_ratio_pct

FROM product_orders po
JOIN warehouse.dim_product dp ON po.product_key = dp.product_key
LEFT JOIN product_returns pr 
    ON po.product_key = pr.product_key 
    AND po.year = pr.year 
    AND po.month = pr.month;

-- ------------------------------------------------------------------------------
-- View 3: marts.v_return_reason_cost_breakdown
-- Description: Phân tích cơ cấu lý do hoàn và các loại chi phí vận hành
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW marts.v_return_reason_cost_breakdown AS
SELECT
    d.year,
    d.month,
    dr.return_reason,
    frc.cost_type,
    COUNT(DISTINCT fr.return_key) AS return_events_count,
    SUM(frc.cost_amount) AS total_cost_amount,
    ROUND(
        SUM(frc.cost_amount)::NUMERIC / NULLIF(COUNT(DISTINCT fr.return_key), 0),
        2
    ) AS avg_cost_per_event
FROM warehouse.fact_returns fr
JOIN warehouse.dim_date d ON fr.return_date_key = d.date_key
JOIN warehouse.dim_return_reason dr ON fr.reason_key = dr.reason_key
JOIN warehouse.fact_return_costs frc ON fr.return_key = frc.return_key
GROUP BY d.year, d.month, dr.return_reason, frc.cost_type;

-- ------------------------------------------------------------------------------
-- View 4: marts.v_reverse_logistics_cycle_time
-- Description: Đo lường thời gian chu trình logistics ngược (Lead time từ đặt đến hoàn)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW marts.v_reverse_logistics_cycle_time AS
WITH return_cost_agg AS (
    SELECT
        return_key,
        SUM(cost_amount) AS total_cost
    FROM warehouse.fact_return_costs
    GROUP BY return_key
)
SELECT
    fr.return_id,
    fo.order_id,
    dc.carrier_name,
    dr.region_name,
    dp.category AS product_category,
    d_order.date AS order_date,
    d_return.date AS return_date,
    (d_return.date - d_order.date) AS cycle_time_days,
    COALESCE(rca.total_cost, 0) AS return_cost
FROM warehouse.fact_returns fr
JOIN warehouse.fact_orders fo ON fr.order_key = fo.order_key
JOIN warehouse.dim_date d_order ON fo.order_date_key = d_order.date_key
JOIN warehouse.dim_date d_return ON fr.return_date_key = d_return.date_key
JOIN warehouse.dim_carrier dc ON fo.carrier_key = dc.carrier_key
JOIN warehouse.dim_region dr ON fo.region_key = dr.region_key
JOIN warehouse.dim_product dp ON fo.product_key = dp.product_key
LEFT JOIN return_cost_agg rca ON fr.return_key = rca.return_key;
