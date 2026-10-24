-- ==============================================================================
-- Test Script: test_data_integrity.sql
-- Description: Kiểm tra tính toàn vẹn và kiểm thử chất lượng dữ liệu kho
-- ==============================================================================

-- Test 1: Kiểm tra khóa ngoại mồ côi (Orphan Foreign Keys) trong fact_orders
SELECT COUNT(*) AS orphan_product_keys
FROM warehouse.fact_orders fo
LEFT JOIN warehouse.dim_product dp ON fo.product_key = dp.product_key
WHERE dp.product_key IS NULL;

-- Test 2: Kiểm tra giá trị đơn hàng âm trong fact_orders
SELECT COUNT(*) AS negative_order_values
FROM warehouse.fact_orders
WHERE order_value < 0;

-- Test 3: Kiểm tra tính duy nhất của mã đơn hàng (order_id uniqueness)
SELECT order_id, COUNT(*)
FROM warehouse.fact_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- Test 4: Kiểm tra chi phí hoàn trả âm trong fact_return_costs
SELECT COUNT(*) AS negative_return_costs
FROM warehouse.fact_return_costs
WHERE cost_amount < 0;
