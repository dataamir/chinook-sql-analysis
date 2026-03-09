-- ============================================================
-- 04_genre_revenue.sql
-- Revenue breakdown by music genre
-- ============================================================

SELECT
    g.Name                                     AS Genre,
    COUNT(DISTINCT t.TrackId)                  AS TrackCount,
    COUNT(il.InvoiceLineId)                    AS TimesSold,
    ROUND(SUM(il.UnitPrice * il.Quantity), 2)  AS TotalRevenue,
    ROUND(AVG(il.UnitPrice), 2)                AS AvgTrackPrice,
    ROUND(SUM(il.UnitPrice * il.Quantity) * 100.0 /
          (SELECT SUM(UnitPrice * Quantity) FROM InvoiceLine), 2) AS RevenueSharePct
FROM InvoiceLine il
JOIN Track t ON il.TrackId = t.TrackId
JOIN Genre g ON t.GenreId  = g.GenreId
GROUP BY g.GenreId
ORDER BY TotalRevenue DESC;
