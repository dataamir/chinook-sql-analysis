-- ============================================================
-- 05_top_customers.sql
-- Highest-value customers with lifetime spend and order count
-- ============================================================

SELECT
    c.CustomerId,
    c.FirstName || ' ' || c.LastName           AS CustomerName,
    c.Country,
    c.City,
    e.FirstName || ' ' || e.LastName           AS SupportRep,
    COUNT(DISTINCT i.InvoiceId)                AS TotalOrders,
    ROUND(SUM(i.Total), 2)                     AS LifetimeValue,
    ROUND(AVG(i.Total), 2)                     AS AvgOrderValue,
    MIN(DATE(i.InvoiceDate))                   AS FirstPurchase,
    MAX(DATE(i.InvoiceDate))                   AS LastPurchase
FROM Customer c
JOIN Invoice  i ON c.CustomerId  = i.CustomerId
JOIN Employee e ON c.SupportRepId = e.EmployeeId
GROUP BY c.CustomerId
ORDER BY LifetimeValue DESC
LIMIT 20;
