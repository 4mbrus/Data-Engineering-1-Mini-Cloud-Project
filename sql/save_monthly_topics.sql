CREATE TABLE "ambrus"."monthly_topic_breakdown"
WITH (
    format = 'JSON',
    external_location = 's3://business-news-sentiments/news_sentiments_monthly/topic_breakdown/'
) AS
WITH combined_data AS (
    -- 1. Select CNN data and tag it
    SELECT *, 'CNN' AS news_site 
    FROM "ambrus"."cnn_sentiment"
    
    UNION ALL
    
    -- 2. Select FOX data and tag it
    SELECT *, 'FOX' AS news_site 
    FROM "ambrus"."fox_sentiment"
)
SELECT
    -- Group by Month (YYYY-MM)
    date_format("date", '%Y-%m') AS month_year,
    
    -- Group by Site
    news_site,
    
    -- Sum specific topics
    SUM(topic_inflation) AS topic_inflation_sum,
    SUM(topic_taxes)     AS topic_taxes_sum,  
    SUM(topic_stocks)    AS topic_stocks_sum,
    SUM(topic_jobs)      AS topic_jobs_sum,
    SUM(topic_housing)   AS topic_housing_sum,
    SUM(topic_energy)    AS topic_energy_sum,
    SUM(topic_crypto)    AS topic_crypto_sum
FROM combined_data
GROUP BY 1, 2;