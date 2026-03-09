-- ============================================================
-- 08_customer_cohort.sql
-- Purchase frequency segmentation (one-time vs repeat buyers)
-- ============================================================

WITH CustomerOrders AS (
    SELECT
        CustomerId,
        COUNT(InvoiceId)       AS OrderCount,
        ROUND(SUM(Total), 2)   AS TotalSpent,
        MIN(DATE(InvoiceDate)) AS FirstOrder,
        MAX(DATE(InvoiceDate)) AS LastOrder
    FROM Invoice
    GROUP BY CustomerId
),
Segmented AS (
    SELECT *,
        CASE
            WHEN OrderCount = 1       THEN '1 - One-Time'
            WHEN OrderCount BETWEEN 2 AND 4 THEN '2 - Occasional (2-4)'
            WHEN OrderCount BETWEEN 5 AND 9 THEN '3 - Regular (5-9)'
            ELSE                           '4 - Loyal (10+)'
        END AS Segment
    FROM CustomerOrders
)
SELECT
    Segment,
    COUNT(*)                       AS CustomerCount,
    ROUND(AVG(OrderCount), 1)      AS AvgOrders,
    ROUND(AVG(TotalSpent), 2)      AS AvgLifetimeValue,
    ROUND(SUM(TotalSpent), 2)      AS SegmentRevenue,
    ROUND(SUM(TotalSpent) * 100.0 /
          (SELECT SUM(Total) FROM Invoice), 2) AS RevenueSharePct
FROM Segmented
GROUP BY Segment
ORDER BY Segment;
