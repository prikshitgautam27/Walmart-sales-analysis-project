"""
Walmart Sales - Run Business Queries with DuckDB
---------------------------------------------------
Runs real SQL against the cleaned CSV directly - no database server,
no credentials, no setup. DuckDB reads the CSV as if it were a table.

Run from the project root:
    python scripts/run_queries_duckdb.py

Results are printed to the console AND saved to sql/query_results.md
so you can paste real numbers into your README's "Key Findings" section.
"""

import duckdb

DATA_PATH = "data/walmart_clean_data.csv"
OUTPUT_MD = "sql/query_results.md"

con = duckdb.connect()
con.execute(f"CREATE VIEW walmart AS SELECT * FROM read_csv_auto('{DATA_PATH}')")

queries = {
    "Q1: Payment methods - transaction count & quantity sold": """
        SELECT payment_method,
               COUNT(*) AS no_payments,
               SUM(quantity) AS no_qty_sold
        FROM walmart
        GROUP BY payment_method
        ORDER BY no_payments DESC;
    """,
    "Q2: Highest-rated category in each branch": """
        SELECT branch, category, avg_rating
        FROM (
            SELECT branch, category,
                   AVG(rating) AS avg_rating,
                   RANK() OVER (PARTITION BY branch ORDER BY AVG(rating) DESC) AS rnk
            FROM walmart
            GROUP BY branch, category
        )
        WHERE rnk = 1
        ORDER BY branch
        LIMIT 15;
    """,
    "Q3: Busiest day of the week for each branch": """
        SELECT branch, day_name, no_transactions
        FROM (
            SELECT branch,
                   strftime(date, '%A') AS day_name,
                   COUNT(*) AS no_transactions,
                   RANK() OVER (PARTITION BY branch ORDER BY COUNT(*) DESC) AS rnk
            FROM walmart
            GROUP BY branch, day_name
        )
        WHERE rnk = 1
        ORDER BY branch
        LIMIT 15;
    """,
    "Q4: Total quantity sold per payment method": """
        SELECT payment_method, SUM(quantity) AS no_qty_sold
        FROM walmart
        GROUP BY payment_method
        ORDER BY no_qty_sold DESC;
    """,
    "Q5: Min/max/avg rating per category per city (sample)": """
        SELECT city, category,
               MIN(rating) AS min_rating,
               MAX(rating) AS max_rating,
               ROUND(AVG(rating), 2) AS avg_rating
        FROM walmart
        GROUP BY city, category
        ORDER BY city
        LIMIT 15;
    """,
    "Q6: Total profit by category (highest to lowest)": """
        SELECT category, ROUND(SUM(profit), 2) AS total_profit
        FROM walmart
        GROUP BY category
        ORDER BY total_profit DESC;
    """,
    "Q7: Most common payment method per branch": """
        WITH cte AS (
            SELECT branch, payment_method,
                   COUNT(*) AS total_trans,
                   RANK() OVER (PARTITION BY branch ORDER BY COUNT(*) DESC) AS rnk
            FROM walmart
            GROUP BY branch, payment_method
        )
        SELECT branch, payment_method AS preferred_payment_method
        FROM cte WHERE rnk = 1
        ORDER BY branch
        LIMIT 15;
    """,
    "Q8: Transactions by shift (Morning/Afternoon/Evening) per branch": """
        SELECT branch,
               CASE
                   WHEN EXTRACT(HOUR FROM time) < 12 THEN 'Morning'
                   WHEN EXTRACT(HOUR FROM time) BETWEEN 12 AND 17 THEN 'Afternoon'
                   ELSE 'Evening'
               END AS shift,
               COUNT(*) AS num_invoices
        FROM walmart
        GROUP BY branch, shift
        ORDER BY branch, num_invoices DESC
        LIMIT 15;
    """,
    "Q9: Top 5 branches with highest revenue decline (2022 -> 2023, min 5 transactions/year)": """
        WITH revenue_2022 AS (
            SELECT branch, SUM(total) AS revenue, COUNT(*) AS txn_2022
            FROM walmart
            WHERE EXTRACT(YEAR FROM date) = 2022
            GROUP BY branch
            HAVING COUNT(*) >= 5
        ),
        revenue_2023 AS (
            SELECT branch, SUM(total) AS revenue, COUNT(*) AS txn_2023
            FROM walmart
            WHERE EXTRACT(YEAR FROM date) = 2023
            GROUP BY branch
            HAVING COUNT(*) >= 5
        )
        SELECT r22.branch,
               txn_2022, txn_2023,
               ROUND(r22.revenue, 2) AS last_year_revenue,
               ROUND(r23.revenue, 2) AS current_year_revenue,
               ROUND(((r22.revenue - r23.revenue) / r22.revenue) * 100, 2) AS revenue_decrease_pct
        FROM revenue_2022 r22
        JOIN revenue_2023 r23 ON r22.branch = r23.branch
        WHERE r22.revenue > r23.revenue
        ORDER BY revenue_decrease_pct DESC
        LIMIT 5;
    """,
    "Q10 (Extended): Profit per unit sold by category": """
        SELECT category,
               ROUND(SUM(profit), 2) AS total_profit,
               SUM(quantity) AS total_qty_sold,
               ROUND(SUM(profit) / SUM(quantity), 2) AS profit_per_unit
        FROM walmart
        GROUP BY category
        ORDER BY profit_per_unit DESC;
    """,
    "Q11 (Extended): Top 5 cities by total revenue": """
        SELECT city, ROUND(SUM(total), 2) AS total_revenue
        FROM walmart
        GROUP BY city
        ORDER BY total_revenue DESC
        LIMIT 5;
    """,
}


def main():
    lines = ["# Walmart Project - Query Results\n"]
    for title, sql in queries.items():
        print("=" * 80)
        print(title)
        print("=" * 80)
        result = con.execute(sql).fetchdf()
        print(result.to_string(index=False))
        print()

        lines.append(f"## {title}\n")
        lines.append(result.to_markdown(index=False))
        lines.append("\n")

    with open(OUTPUT_MD, "w") as f:
        f.write("\n".join(lines))
    print(f"All results saved to {OUTPUT_MD}")


if __name__ == "__main__":
    main()
