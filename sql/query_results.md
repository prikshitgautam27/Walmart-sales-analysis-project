# Walmart Project - Query Results

## Q1: Payment methods - transaction count & quantity sold

| payment_method   |   no_payments |   no_qty_sold |
|:-----------------|--------------:|--------------:|
| Credit card      |          4256 |          9567 |
| Ewallet          |          3881 |          8932 |
| Cash             |          1832 |          4984 |


## Q2: Highest-rated category in each branch

| branch   | category               |   avg_rating |
|:---------|:-----------------------|-------------:|
| WALM001  | Electronic accessories |      7.45    |
| WALM002  | Food and beverages     |      8.25    |
| WALM003  | Sports and travel      |      7.5     |
| WALM004  | Food and beverages     |      9.3     |
| WALM005  | Health and beauty      |      8.36667 |
| WALM006  | Fashion accessories    |      6.79706 |
| WALM007  | Food and beverages     |      7.55    |
| WALM008  | Food and beverages     |      7.4     |
| WALM009  | Sports and travel      |      9.6     |
| WALM010  | Electronic accessories |      9       |
| WALM011  | Food and beverages     |      7       |
| WALM012  | Health and beauty      |      7.45    |
| WALM013  | Health and beauty      |      7.6     |
| WALM014  | Electronic accessories |      6.83333 |
| WALM015  | Home and lifestyle     |      6.22308 |


## Q3: Busiest day of the week for each branch

| branch   | day_name   |   no_transactions |
|:---------|:-----------|------------------:|
| WALM001  | Sunday     |                18 |
| WALM002  | Saturday   |                16 |
| WALM003  | Sunday     |                30 |
| WALM004  | Sunday     |                16 |
| WALM005  | Thursday   |                15 |
| WALM006  | Thursday   |                17 |
| WALM007  | Saturday   |                16 |
| WALM008  | Wednesday  |                13 |
| WALM009  | Saturday   |                41 |
| WALM010  | Friday     |                15 |
| WALM011  | Tuesday    |                12 |
| WALM012  | Monday     |                14 |
| WALM013  | Monday     |                12 |
| WALM013  | Saturday   |                12 |
| WALM014  | Wednesday  |                10 |


## Q4: Total quantity sold per payment method

| payment_method   |   no_qty_sold |
|:-----------------|--------------:|
| Credit card      |          9567 |
| Ewallet          |          8932 |
| Cash             |          4984 |


## Q5: Min/max/avg rating per category per city (sample)

| city    | category               |   min_rating |   max_rating |   avg_rating |
|:--------|:-----------------------|-------------:|-------------:|-------------:|
| Abilene | Health and beauty      |          9.7 |          9.7 |         9.7  |
| Abilene | Electronic accessories |          7.1 |          8.8 |         7.97 |
| Abilene | Food and beverages     |          6   |          8.9 |         6.95 |
| Abilene | Fashion accessories    |          4   |          9   |         6.24 |
| Abilene | Home and lifestyle     |          4   |          9   |         6.1  |
| Alamo   | Fashion accessories    |          3   |          9   |         6.87 |
| Alamo   | Health and beauty      |          7.7 |          8.2 |         7.95 |
| Alamo   | Food and beverages     |          5.2 |          5.2 |         5.2  |
| Alamo   | Sports and travel      |          5   |         10   |         7.3  |
| Alamo   | Home and lifestyle     |          3   |          9   |         6.3  |
| Alice   | Electronic accessories |          7.3 |          7.3 |         7.3  |
| Alice   | Home and lifestyle     |          4   |          9   |         6.04 |
| Alice   | Sports and travel      |          6.5 |          7.9 |         6.93 |
| Alice   | Food and beverages     |          5   |          9.2 |         7.68 |
| Alice   | Fashion accessories    |          3   |          9   |         5.93 |


## Q6: Total profit by category (highest to lowest)

| category               |   total_profit |
|:-----------------------|---------------:|
| Fashion accessories    |       192315   |
| Home and lifestyle     |       192214   |
| Electronic accessories |        30772.5 |
| Food and beverages     |        21552.8 |
| Sports and travel      |        20613.9 |
| Health and beauty      |        18671.7 |


## Q7: Most common payment method per branch

| branch   | preferred_payment_method   |
|:---------|:---------------------------|
| WALM001  | Ewallet                    |
| WALM002  | Ewallet                    |
| WALM003  | Credit card                |
| WALM004  | Ewallet                    |
| WALM005  | Ewallet                    |
| WALM006  | Ewallet                    |
| WALM007  | Ewallet                    |
| WALM008  | Ewallet                    |
| WALM009  | Credit card                |
| WALM010  | Ewallet                    |
| WALM011  | Ewallet                    |
| WALM012  | Ewallet                    |
| WALM013  | Ewallet                    |
| WALM014  | Ewallet                    |
| WALM015  | Ewallet                    |


## Q8: Transactions by shift (Morning/Afternoon/Evening) per branch

| branch   | shift     |   num_invoices |
|:---------|:----------|---------------:|
| WALM001  | Afternoon |             36 |
| WALM001  | Evening   |             30 |
| WALM001  | Morning   |              8 |
| WALM002  | Afternoon |             29 |
| WALM002  | Evening   |             21 |
| WALM002  | Morning   |             15 |
| WALM003  | Afternoon |             95 |
| WALM003  | Morning   |             50 |
| WALM003  | Evening   |             41 |
| WALM004  | Afternoon |             27 |
| WALM004  | Evening   |             24 |
| WALM004  | Morning   |              9 |
| WALM005  | Evening   |             35 |
| WALM005  | Afternoon |             34 |
| WALM005  | Morning   |             15 |


## Q9: Top 5 branches with highest revenue decline (2022 -> 2023, min 5 transactions/year)

| branch   |   txn_2022 |   txn_2023 |   last_year_revenue |   current_year_revenue |   revenue_decrease_pct |
|:---------|-----------:|-----------:|--------------------:|-----------------------:|-----------------------:|
| WALM054  |          9 |          7 |             1372    |                 673    |                  50.95 |
| WALM025  |          7 |          5 |              791    |                 396.95 |                  49.82 |
| WALM074  |         11 |         12 |             1517.44 |                1064.89 |                  29.82 |
| WALM003  |          5 |          5 |              491    |                 385    |                  21.59 |
| WALM099  |          8 |          5 |              479    |                 383    |                  20.04 |


## Q10 (Extended): Profit per unit sold by category

| category               |   total_profit |   total_qty_sold |   profit_per_unit |
|:-----------------------|---------------:|-----------------:|------------------:|
| Food and beverages     |        21552.8 |              952 |             22.64 |
| Sports and travel      |        20613.9 |              920 |             22.41 |
| Health and beauty      |        18671.7 |              854 |             21.86 |
| Electronic accessories |        30772.5 |             1494 |             20.6  |
| Home and lifestyle     |       192214   |             9610 |             20    |
| Fashion accessories    |       192315   |             9653 |             19.92 |


## Q11 (Extended): Top 5 cities by total revenue

| city        |   total_revenue |
|:------------|----------------:|
| Weslaco     |         46351.8 |
| Waxahachie  |         40703.3 |
| Plano       |         25688.3 |
| San Antonio |         24950.6 |
| Port Arthur |         24524.4 |

