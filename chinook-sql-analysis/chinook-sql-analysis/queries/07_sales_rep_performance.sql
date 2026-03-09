-- ============================================================
-- 07_sales_rep_performance.sql
-- Compare sales support agent performance
-- ============================================================

SELECT
    e.EmployeeId,
    e.FirstName || ' ' || e.LastName     AS SalesRep,
    e.Title,
    e.HireDate,
    COUNT(DISTINCT c.CustomerId)         AS CustomersSupported,
    COUNT(DISTINCT i.InvoiceId)          AS TotalSales,
    ROUND(SUM(i.Total), 2)               AS TotalRevenue,
    ROUND(AVG(i.Total), 2)               AS AvgDealSize,
    ROUND(SUM(i.Total) /
          COUNT(DISTINCT c.CustomerId), 2) AS RevenuePerCustomer
FROM Employee e
JOIN Customer c ON e.EmployeeId   = c.SupportRepId
JOIN Invoice  i ON c.CustomerId   = i.CustomerId
WHERE e.Title LIKE '%Sales%'
GROUP BY e.EmployeeId
ORDER BY TotalRevenue DESC;
