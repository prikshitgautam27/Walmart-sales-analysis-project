-- =========================================================
-- Walmart Sales Analysis - Business Questions (PostgreSQL)
-- =========================================================
-- Assumes the 'walmart' table has been loaded via scripts/load_to_db.py
-- Columns: invoice_id, branch, city, category, unit_price, quantity,
--          date, time, payment_method, rating, profit_margin, total, profit

-- Quick sanity checks
SELECT COUNT(*) FROM walmart;
SELECT * FROM walmart LIMIT 5;


-- ============================
-- ORIGINAL BUSINESS QUESTIONS
-- ============================

-- Q1: Payment methods - transaction count and quantity sold per method
SELECT
    payment_method,
    COUNT(*) AS no_payments,
    SUM(quantity) AS no_qty_sold
FROM walmart
GROUP BY payment_method;

-- Q2: Highest-rated category in each branch
SELECT branch, category, avg_rating
FROM (
    SELECT
        branch,
        category,
        AVG(rating) AS avg_rating,
        RANK() OVER (PARTITION BY branch ORDER BY AVG(rating) DESC) AS rnk
    FROM walmart
    GROUP BY branch, category
) ranked
WHERE rnk = 1;

-- Q3: Busiest day of the week for each branch
SELECT branch, day_name, no_transactions
FROM (
    SELECT
        branch,
        TO_CHAR(TO_DATE(date, 'DD/MM/YY'), 'Day') AS day_name,
        COUNT(*) AS no_transactions,
        RANK() OVER (PARTITION BY branch ORDER BY COUNT(*) DESC) AS rnk
    FROM walmart
    GROUP BY branch, day_name
) ranked
WHERE rnk = 1;

-- Q4: Total quantity sold per payment method
SELECT
    payment_method,
    SUM(quantity) AS no_qty_sold
FROM walmart
GROUP BY payment_method;

-- Q5: Min / max / avg rating per category, per city
SELECT
    city,
    category,
    MIN(rating) AS min_rating,
    MAX(rating) AS max_rating,
    AVG(rating) AS avg_rating
FROM walmart
GROUP BY city, category;

-- Q6: Total profit per category, ranked highest to lowest
SELECT
    category,
    SUM(profit) AS total_profit
FROM walmart
GROUP BY category
ORDER BY total_profit DESC;

-- Q7: Most common payment method per branch
WITH cte AS (
    SELECT
        branch,
        payment_method,
        COUNT(*) AS total_trans,
        RANK() OVER (PARTITION BY branch ORDER BY COUNT(*) DESC) AS rnk
    FROM walmart
    GROUP BY branch, payment_method
)
SELECT branch, payment_method AS preferred_payment_method
FROM cte
WHERE rnk = 1;

-- Q8: Transactions by shift (Morning / Afternoon / Evening) per branch
SELECT
    branch,
    CASE
        WHEN EXTRACT(HOUR FROM time::time) < 12 THEN 'Morning'
        WHEN EXTRACT(HOUR FROM time::time) BETWEEN 12 AND 17 THEN 'Afternoon'
        ELSE 'Evening'
    END AS shift,
    COUNT(*) AS num_invoices
FROM walmart
GROUP BY branch, shift
ORDER BY branch, num_invoices DESC;

-- Q9: Top 5 branches with the highest revenue decline (2022 -> 2023)
WITH revenue_2022 AS (
    SELECT branch, SUM(total) AS revenue
    FROM walmart
    WHERE EXTRACT(YEAR FROM TO_DATE(date, 'DD/MM/YY')) = 2022
    GROUP BY branch
),
revenue_2023 AS (
    SELECT branch, SUM(total) AS revenue
    FROM walmart
    WHERE EXTRACT(YEAR FROM TO_DATE(date, 'DD/MM/YY')) = 2023
    GROUP BY branch
)
SELECT
    r22.branch,
    r22.revenue AS last_year_revenue,
    r23.revenue AS current_year_revenue,
    ROUND(((r22.revenue - r23.revenue) / r22.revenue) * 100, 2) AS revenue_decrease_ratio
FROM revenue_2022 r22
JOIN revenue_2023 r23 ON r22.branch = r23.branch
WHERE r22.revenue > r23.revenue
ORDER BY revenue_decrease_ratio DESC
LIMIT 5;


-- =========================================================
-- EXTENDED QUESTIONS (added beyond the original tutorial)
-- =========================================================

-- Q10: Profit PER UNIT sold, by category - not just total profit.
-- Purpose: total profit can be misleading if a category sells huge volume
-- at thin margins. This finds which category is most efficient per unit sold,
-- which is a stronger signal for where to focus marketing/restocking.
SELECT
    category,
    SUM(profit) AS total_profit,
    SUM(quantity) AS total_qty_sold,
    ROUND(SUM(profit) / SUM(quantity), 2) AS profit_per_unit
FROM walmart
GROUP BY category
ORDER BY profit_per_unit DESC;

-- Q11: Top 5 cities by total revenue.
-- Purpose: city-level revenue ranking to guide where Walmart might expand
-- or invest more marketing spend (complements the branch-level Q9 analysis).
SELECT
    city,
    SUM(total) AS total_revenue
FROM walmart
GROUP BY city
ORDER BY total_revenue DESC
LIMIT 5;

-- Q12: Does customer rating correlate with how much they buy?
-- Purpose: tests whether happier customers (higher rating) also buy more,
-- which would justify investing in customer satisfaction as a revenue lever.
-- (Correlation coefficients aren't native to SQL aggregates in a simple form,
-- so this is intentionally done in Python/pandas instead - see notebook.)
