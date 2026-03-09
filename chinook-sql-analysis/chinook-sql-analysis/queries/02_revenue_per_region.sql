-- ============================================================
-- 02_revenue_per_region.sql
-- Total revenue grouped by billing country (region)
-- ============================================================

SELECT
    i.BillingCountry                           AS Country,
    COUNT(DISTINCT i.InvoiceId)                AS TotalInvoices,
    COUNT(DISTINCT i.CustomerId)               AS UniqueCustomers,
    ROUND(SUM(i.Total), 2)                     AS TotalRevenue,
    ROUND(AVG(i.Total), 2)                     AS AvgOrderValue,
    ROUND(SUM(i.Total) * 100.0 /
          (SELECT SUM(Total) FROM Invoice), 2) AS RevenueSharePct
FROM Invoice i
GROUP BY i.BillingCountry
ORDER BY TotalRevenue DESC;
