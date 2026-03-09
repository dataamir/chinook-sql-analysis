-- ============================================================
-- 01_top_selling_tracks.sql
-- Top 20 best-selling tracks by total revenue
-- ============================================================

SELECT
    t.TrackId,
    t.Name                          AS TrackName,
    ar.Name                         AS Artist,
    al.Title                        AS Album,
    g.Name                          AS Genre,
    COUNT(il.InvoiceLineId)         AS TimesSold,
    SUM(il.Quantity)                AS UnitsSold,
    ROUND(SUM(il.UnitPrice * il.Quantity), 2) AS TotalRevenue
FROM InvoiceLine il
JOIN Track   t  ON il.TrackId   = t.TrackId
JOIN Album   al ON t.AlbumId    = al.AlbumId
JOIN Artist  ar ON al.ArtistId  = ar.ArtistId
JOIN Genre   g  ON t.GenreId    = g.GenreId
GROUP BY t.TrackId
ORDER BY TotalRevenue DESC
LIMIT 20;
