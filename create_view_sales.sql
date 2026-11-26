USE Sales_ETL_DB;
GO

CREATE VIEW sales.vw_SalesSummary AS
SELECT 
    o.order_id,
    o.order_date,
    c.full_name AS customer_name,
    c.city,
    p.product_name,
    p.category,
    p.unit_price,
    o.quantity,
    (o.quantity * p.unit_price) AS total_sales
FROM sales.Orders o
JOIN sales.Customers c ON o.customer_id = c.customer_id
JOIN sales.Products p ON o.product_id = p.product_id;
GO

SELECT TOP 5 * FROM sales.vw_SalesSummary;

