CREATE MATERIALIZED VIEW sales.sales_by_product
WITH (DISTRIBUTION = HASH(ProductID), CLUSTERED COLUMNSTORE INDEX)
AS
SELECT 
    ProductID,
    SUM(OrderQty) AS TotalQuantity,
    SUM(LineTotal) AS TotalAmount
FROM 
    Sales.SalesOrderDetail
GROUP BY 
    ProductID
