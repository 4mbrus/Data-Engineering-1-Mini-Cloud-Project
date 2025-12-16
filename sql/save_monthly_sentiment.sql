CREATE TABLE "ambrus"."monthly_combined_sentiments"
WITH (
    format = 'JSON',
    external_location = 's3://business-news-sentiments/news_sentiments_monthly/combined_networks/'
) AS
WITH cnn_monthly AS (
    SELECT
        date_trunc('month', "date") AS month_start,
        SUM("sentiment") AS cnn_score
    FROM "ambrus"."cnn_sentiment"
    GROUP BY 1
),
fox_monthly AS (
    SELECT
        date_trunc('month', "date") AS month_start,
        SUM("sentiment") AS fox_score
    FROM "ambrus"."fox_sentiment"
    GROUP BY 1
)
SELECT
    -- Use date from whichever table has data for that month
    date_format(COALESCE(c.month_start, f.month_start), '%Y-%m') AS month_year,
    
    -- Use 0 if there is no data for that month
    COALESCE(c.cnn_score, 0) AS cnn_sentiment,
    COALESCE(f.fox_score, 0) AS fox_sentiment
FROM cnn_monthly c
FULL OUTER JOIN fox_monthly f ON c.month_start = f.month_start
ORDER BY 1 DESC;