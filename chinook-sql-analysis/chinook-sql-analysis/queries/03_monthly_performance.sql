-- ============================================================
-- 03_monthly_performance.sql
-- Revenue and order volume by year-month
-- ============================================================

SELECT
    strftime('%Y', InvoiceDate)          AS Year,
    strftime('%m', InvoiceDate)          AS Month,
    strftime('%Y-%m', InvoiceDate)       AS YearMonth,
    COUNT(InvoiceId)                     AS TotalOrders,
    COUNT(DISTINCT CustomerId)           AS UniqueCustomers,
    ROUND(SUM(Total), 2)                 AS MonthlyRevenue,
    ROUND(AVG(Total), 2)                 AS AvgOrderValue,
    ROUND(SUM(Total) - LAG(SUM(Total))
          OVER (ORDER BY strftime('%Y-%m', InvoiceDate)), 2) AS MoM_Change
FROM Invoice
GROUP BY strftime('%Y-%m', InvoiceDate)
ORDER BY YearMonth;
