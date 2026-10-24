-- ==============================================================================
-- View: marts.v_kpi_return_rates
-- Description: Aggregate return rate and return costs by month and carrier.
-- Governance: Section 4.3 (Fanout Protection & Grain Compliance)
-- ==============================================================================

CREATE OR REPLACE VIEW marts.v_kpi_return_rates AS
WITH order_summary AS (
    -- Grain: 1 row per order_date_key and carrier_key
    SELECT
        fo.order_date_key,
        fo.carrier_key,
        COUNT(fo.order_key) AS total_orders,
        SUM(fo.order_value) AS total_gross_value
    FROM warehouse.fact_orders fo
    GROUP BY fo.order_date_key, fo.carrier_key
),
return_summary AS (
    -- Grain: 1 row per order_key aggregate to avoid fanout before combining
    -- First aggregate return costs to return_key grain
    SELECT
        fr.order_key,
        COUNT(DISTINCT fr.return_key) AS return_count,
        COALESCE(SUM(frc.cost_amount), 0) AS total_return_cost
    FROM warehouse.fact_returns fr
    LEFT JOIN warehouse.fact_return_costs frc ON fr.return_key = frc.return_key
    GROUP BY fr.order_key
),
order_return_grain AS (
    -- Grain: Combine to order level
    SELECT
        fo.order_date_key,
        fo.carrier_key,
        COUNT(rs.order_key) AS total_returned_orders,
        SUM(rs.total_return_cost) AS total_return_cost
    FROM warehouse.fact_orders fo
    INNER JOIN return_summary rs ON fo.order_key = rs.order_key
    GROUP BY fo.order_date_key, fo.carrier_key
)
SELECT
    d.year,
    d.month,
    c.carrier_id,
    c.carrier_name,
    COALESCE(os.total_orders, 0) AS total_orders,
    COALESCE(org.total_returned_orders, 0) AS returned_orders,
    ROUND(
        (COALESCE(org.total_returned_orders, 0)::NUMERIC / NULLIF(os.total_orders, 0)) * 100,
        2
    ) AS return_rate_pct,
    COALESCE(os.total_gross_value, 0) AS total_gross_value,
    COALESCE(org.total_return_cost, 0) AS total_return_cost
FROM order_summary os
JOIN warehouse.dim_date d ON os.order_date_key = d.date_key
JOIN warehouse.dim_carrier c ON os.carrier_key = c.carrier_key
LEFT JOIN order_return_grain org 
    ON os.order_date_key = org.order_date_key 
    AND os.carrier_key = org.carrier_key;
