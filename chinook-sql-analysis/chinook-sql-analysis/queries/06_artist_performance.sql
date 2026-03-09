-- ============================================================
-- 06_artist_performance.sql
-- Revenue and sales by artist using multi-table JOINs
-- ============================================================

SELECT
    ar.ArtistId,
    ar.Name                                    AS Artist,
    COUNT(DISTINCT al.AlbumId)                 AS AlbumCount,
    COUNT(DISTINCT t.TrackId)                  AS TrackCount,
    COUNT(il.InvoiceLineId)                    AS TimesSold,
    ROUND(SUM(il.UnitPrice * il.Quantity), 2)  AS TotalRevenue,
    ROUND(AVG(il.UnitPrice * il.Quantity), 2)  AS AvgSaleValue
FROM Artist    ar
JOIN Album     al ON ar.ArtistId  = al.ArtistId
JOIN Track     t  ON al.AlbumId   = t.AlbumId
JOIN InvoiceLine il ON t.TrackId  = il.TrackId
GROUP BY ar.ArtistId
ORDER BY TotalRevenue DESC
LIMIT 20;
