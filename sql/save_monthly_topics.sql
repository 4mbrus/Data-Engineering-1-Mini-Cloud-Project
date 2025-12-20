CREATE OR REPLACE VIEW "ambrus"."monthly_topic_breakdown"
WITH combined_data AS (
    -- 1. Select CNN data and tag it
    SELECT *, 'CNN' AS news_site 
    FROM "ambrus"."cnn_sentiment_clean"
    
    UNION ALL
    
    -- 2. Select FOX data and tag it
    SELECT *, 'FOX' AS news_site 
    FROM "ambrus"."fox_sentiment_clean"
)
SELECT
    -- Group by Month (YYYY-MM)
    date_format("date", '%Y-%m') AS month_year,
    
    -- Group by Site
    news_site,
    
    -- Sum specific topics
    SUM(topic_inflation)*100/COUNT(*)  AS topic_inflation_sum,
    SUM(topic_taxes)*100/COUNT(*)      AS topic_taxes_sum,  
    SUM(topic_stocks)*100/COUNT(*)     AS topic_stocks_sum,
    SUM(topic_jobs)*100/COUNT(*)       AS topic_jobs_sum,
    SUM(topic_housing)*100/COUNT(*)    AS topic_housing_sum,
    SUM(topic_energy)*100/COUNT(*)     AS topic_energy_sum,
    SUM(topic_crypto)*100/COUNT(*)     AS topic_crypto_sum
FROM combined_data
GROUP BY 1, 2;