Edited: 2021-09-28

# Basic stats with MySQL

You'll probably never need this, as aggregation (math operations) is not the strongest suit of any database system - in fact, aggregation should be best left to programming.

However, there are cases when aggregation with SQL is necessary, convenient, or required.

This guide is for that rare occasion.



## Database Version

I said MySQL, but I'm actually using MariaDB.

`10.4.16-MariaDB-1:10.4.16+maria~focal`

Check the MySQL versus MariaDB compatibility documentation if you really want to - [link](https://mariadb.com/kb/en/mariadb-vs-mysql-compatibility/)



## Data

I'm using RFM data at work, but for sake of convenient, I will refer to the table as `mydataset` and its single column as `mydata`.

| index | data |
| :---: | :--: |
|   1   |  45  |
|   2   |  32  |
|   3   |  74  |
|  ..   |  ..  |



## Aggregate Functions

Aggregate functions official documentation - [link](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html)

It's easy to get total number, total sum, minimum, maximum, mean, standard deviation, and variance - they are all functions provided by MySQL.

As such,

```mariadb
SELECT
  COUNT(mydata) AS total_number,
  SUM(mydata) AS total_sum,
  MIN(mydata) AS minimum_value,
  MAX(mydata) AS maximum_value,
  AVG(mydata) AS mean,
  STD(mydata) AS standard_variation,
  VARIANCE(mydata) AS variance
FROM mydataset;
```



## Mode

Apparently, there's no such thing as `MODE`.

Since mode is the value that is repeated most often, the query below simply gets count of each value in `mydata` and from the result in descending order, the first value is returned.

```mariadb
SELECT
  mydata AS mode_value, COUNT(mydata) AS group_count
FROM mydataset
GROUP BY mydata
ORDER BY group_count DESC LIMIT 1;
```

There are other ways to go about this, but this is my limit.



## Median

This sort of gets me angry.

1. StackOverflow was not at all helpful - they came up with overly complicated answers that I could not replicate (without using `PERCENTILE_CONT`).
2. There is no `MEDIAN` function, but there is `PERCENTILE_CONT(0.5)`, a window function that pretty much returns the median. It is available since version 10.3, so it _is_ available on 10.4.
3. DataGrip, the tool I use to manage databases, totally DERPED and its inspection told me `PERCENTILE_CONT` is an `Unknown database function`.
   ![mariadb_no_percentile_cont](https://user-images.githubusercontent.com/44990492/135028905-6e25e15b-3342-405d-be33-5aafd7b50442.PNG)
   WHYYYYYYYY.
4. DataGrip takes it further when it acts like `WITHIN GROUP` is not a thing.
   ![mariadb_expected_not_group](https://user-images.githubusercontent.com/44990492/135029490-2c12dc9c-afcc-4cc0-89a2-5508ec318984.PNG)
5. I only executed the query out of frustration, only to find out that __IT ACTUALLY WORKS__.
6. By the time I found that `PERCENTILE_CONT` works, I had nearly completed a complicated query that returns a median.



Here's the simple and neat way to get a median:

```mariadb
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mydata) OVER () AS median_value FROM mydataset LIMIT 1;
```



Here's the overly complex way to get a median that I am weirdly, slightly proud of:

```mariadb
SELECT
  # 4. Gets average of median value(s)
  (SUM(t3.lower_median_value) + SUM(t3.upper_median_value))/COUNT(*) AS true_median
FROM (
  # 3. From data, retrieves value from the median row(s)
  SELECT DISTINCT
    NTH_VALUE(t2.mydata, t1.lower_middle_row) OVER (ORDER BY t2.mydata) AS lower_median_value,
    NTH_VALUE(t2.mydata, t1.upper_middle_row) OVER (ORDER BY t2.mydata) AS upper_median_value
  FROM (
    # 1. Gets row number(s) of median
    SELECT
      FLOOR(COUNT(mydata) / 2) AS lower_middle_row,
      CEIL(COUNT(mydata) / 2)  AS upper_middle_row
    FROM mydataset
  ) AS t1, (
    # 2. Gets data
    SELECT mydata
    FROM mydataset
  ) AS t2
) AS t3;
```

Since I put so much effort in it, I feel the need to explain the overly complex query.

1. Count total number of rows
2. Half the total count and you get an integer if there are even number of rows, or float if there are odd number of rows (i.e. if 10, then 5. if 9, then 4.5). `FLOOR` will round down, `CEIL` will round up. If total count is even, I get two of the same number. If total count is odd, I get two different values (i.e. if 10, then 5 and 5. if 9, then 4 and 5). These are row number(s) of median.
3. Retrieve values at median rows, and average them - that's the median value.



# Note on complex stats

This guide won't cover how to do complex statistics, but here are some notes on how you could go about it:

1. Find a SQL Cookbook, or a Practical SQL guide. In fact, _Practical SQL by Anthony DeBarros_ is recommended. Chapter 5 and chapter 10 covers statistics.
2. Learn from my mistake, don't rely too much on code inspection on your db tool.
3. Stored procedure is definitely not the way to go about it. Trust me, I've tried (it's very slow from some reason).
4. Check first to see if a function that you need is available in Aggregate Functions and/or Window Functions.
5. If the result of a function is not what you expect, you might need to refer to documentation. I mean, who _knew_ skewness can be calculated in so many different ways?

