# 🎵 Chinook SQL Sales Analysis

> **Task 5 — SQL-Based Analysis of Product Sales**  
> End-to-end business intelligence project using the Chinook music store database.

---

## 📋 Project Overview

This project demonstrates how to use SQL and Python to extract actionable business insights from a relational database. Using the industry-standard **Chinook Database** (a digital music store), we answer eight key business questions through SQL queries, Python automation, and professional visualizations.

---

## 🗂️ Repository Structure

```
chinook-sql-analysis/
│
├── data/
│   ├── create_chinook_db.py      # Script to build the SQLite DB
│   └── chinook.db                # SQLite database (generated)
│
├── queries/                      # Pure SQL files (one per question)
│   ├── 01_top_selling_tracks.sql
│   ├── 02_revenue_per_region.sql
│   ├── 03_monthly_performance.sql
│   ├── 04_genre_revenue.sql
│   ├── 05_top_customers.sql
│   ├── 06_artist_performance.sql
│   ├── 07_sales_rep_performance.sql
│   └── 08_customer_cohort.sql
│
├── notebooks/
│   └── chinook_analysis.ipynb    # Jupyter notebook walkthrough
│
├── outputs/                      # CSV results (auto-generated)
│   ├── 01_top_selling_tracks.csv
│   ├── 02_revenue_per_region.csv
│   └── ...
│
├── visualizations/               # PNG charts (auto-generated)
│   ├── 00_dashboard.png
│   ├── 01_top_tracks.png
│   └── ...
│
├── analysis.py                   # Main Python runner script
├── requirements.txt
└── README.md
```

---

## 🧱 Database Schema

The Chinook database models a digital music store with the following tables:

```
Artist ──< Album ──< Track >── InvoiceLine >── Invoice >── Customer
                  ↑                                              ↑
               Genre                                         Employee
            MediaType
```

| Table         | Rows (approx) | Description                          |
|---------------|--------------|--------------------------------------|
| Artist        | 30           | Music artists                        |
| Album         | 30           | Albums linked to artists             |
| Track         | 350          | Songs with genre, price, duration    |
| Genre         | 20           | Music genres                         |
| MediaType     | 5            | File formats (MP3, AAC, etc.)        |
| Playlist      | 18           | User playlists                       |
| PlaylistTrack | ~800         | Track–playlist mapping               |
| Customer      | 59           | Customers across 20+ countries       |
| Employee      | 8            | Staff (sales reps, IT, management)   |
| Invoice       | 412          | Purchase transactions                |
| InvoiceLine   | ~1,865       | Individual items on each invoice     |

---

## ❓ Business Questions Answered

| # | Question | SQL Technique |
|---|----------|---------------|
| 1 | What are the top-selling tracks? | JOIN 4 tables + GROUP BY + ORDER BY |
| 2 | Which countries generate the most revenue? | Aggregation + window function (%) |
| 3 | How does revenue trend month-over-month? | DATE functions + LAG window function |
| 4 | Which music genres earn the most? | Multi-table JOIN + aggregation |
| 5 | Who are our highest-value customers? | 3-table JOIN + lifetime value calc |
| 6 | Which artists drive the most revenue? | 4-table JOIN + GROUP BY |
| 7 | How do sales reps compare? | Employee–Customer–Invoice chain JOIN |
| 8 | How do customer segments differ? | CTE + CASE segmentation |

---

## 🔑 Key SQL Concepts Used

### JOINs
```sql
-- 4-table JOIN: Track → Album → Artist → Genre
SELECT ar.Name, al.Title, t.Name, g.Name
FROM InvoiceLine il
JOIN Track   t  ON il.TrackId  = t.TrackId
JOIN Album   al ON t.AlbumId   = al.AlbumId
JOIN Artist  ar ON al.ArtistId = ar.ArtistId
JOIN Genre   g  ON t.GenreId   = g.GenreId;
```

### Aggregations
```sql
SELECT
    BillingCountry,
    COUNT(DISTINCT InvoiceId)  AS TotalOrders,
    ROUND(SUM(Total), 2)       AS TotalRevenue,
    ROUND(AVG(Total), 2)       AS AvgOrderValue
FROM Invoice
GROUP BY BillingCountry
ORDER BY TotalRevenue DESC;
```

### Window Functions
```sql
-- Month-over-month change
SELECT
    strftime('%Y-%m', InvoiceDate) AS YearMonth,
    SUM(Total)                     AS Revenue,
    SUM(Total) - LAG(SUM(Total))
        OVER (ORDER BY strftime('%Y-%m', InvoiceDate)) AS MoM_Change
FROM Invoice
GROUP BY YearMonth;
```

### CTEs (Common Table Expressions)
```sql
WITH CustomerOrders AS (
    SELECT CustomerId, COUNT(*) AS OrderCount, SUM(Total) AS Spent
    FROM Invoice GROUP BY CustomerId
)
SELECT
    CASE WHEN OrderCount = 1 THEN 'One-Time'
         WHEN OrderCount < 5 THEN 'Occasional'
         ELSE 'Loyal' END AS Segment,
    COUNT(*), AVG(Spent)
FROM CustomerOrders
GROUP BY Segment;
```

---

## 📊 Key Findings

| Insight | Value |
|---------|-------|
| 🏆 Top Market | USA (17.5% of revenue) |
| 🎸 Top Genre | Bossa Nova (9.0% of revenue) |
| 👑 Top Artist Revenue | Alice In Chains |
| 📈 Loyal Customers (10+ orders) | 23% of revenue from just 8 customers |
| 💼 Best Sales Rep | Steve Johnson (by total revenue) |

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### 1. Build the Database
```bash
python data/create_chinook_db.py
```

### 2. Run the Full Analysis
```bash
python analysis.py
```

### 3. Or use individual SQL files
```bash
sqlite3 data/chinook.db < queries/01_top_selling_tracks.sql
```

### 4. Jupyter Notebook
```bash
jupyter notebook notebooks/chinook_analysis.ipynb
```

---

## 📦 Requirements

```
pandas>=1.5.0
matplotlib>=3.6.0
seaborn>=0.12.0
jupyter>=1.0.0
```

---

## 📁 What to Upload to GitHub

When uploading this project to GitHub, include these files:

| File/Folder | Upload? | Notes |
|-------------|---------|-------|
| `README.md` | ✅ Yes | Always include |
| `requirements.txt` | ✅ Yes | Dependency list |
| `analysis.py` | ✅ Yes | Main script |
| `data/create_chinook_db.py` | ✅ Yes | DB builder script |
| `queries/*.sql` | ✅ Yes | All SQL files |
| `notebooks/*.ipynb` | ✅ Yes | Notebook |
| `visualizations/*.png` | ✅ Yes | Charts |
| `outputs/*.csv` | ✅ Yes | Result CSVs |
| `data/chinook.db` | ⚠️ Optional | SQLite file (~1MB), add to `.gitignore` if large |
| `__pycache__/` | ❌ No | Add to `.gitignore` |
| `.env` | ❌ No | Never upload secrets |

### Recommended `.gitignore`
```
__pycache__/
*.pyc
.DS_Store
.env
*.egg-info/
```

---

## 🗃️ Extending to PostgreSQL / MySQL

The SQL queries are ANSI-compatible. To use with PostgreSQL:
```python
import psycopg2
conn = psycopg2.connect("postgresql://user:password@host/dbname")
```

To use with MySQL:
```python
import mysql.connector
conn = mysql.connector.connect(host="...", user="...", password="...", database="...")
```

Replace `strftime('%Y-%m', date)` with `DATE_FORMAT(date, '%Y-%m')` for MySQL.

---

## 📜 License

MIT License — free to use for learning and portfolios.
