CREATE OR REPLACE VIEW "monthly_combined_sentiments" AS 
WITH
  cnn_monthly AS (
   SELECT
     date_trunc('month', "clean_date") month_start
   , (((COUNT(*) - SUM("sentiment")) * 100) / COUNT(*)) cnn_score
   FROM
     "ambrus"."cnn_sentiment_clean"
   GROUP BY 1
) 
, fox_monthly AS (
   SELECT
     date_trunc('month', "clean_date") month_start
   , (((COUNT(*) - SUM("sentiment")) * 100) / COUNT(*)) fox_score
   FROM
     "ambrus"."fox_sentiment_clean"
   GROUP BY 1
) 
SELECT
  date_format(COALESCE(c.month_start, f.month_start), '%Y-%m') month_year
, COALESCE(c.cnn_score, 0) cnn_sentiment
, COALESCE(f.fox_score, 0) fox_sentiment
FROM
  (cnn_monthly c
FULL JOIN fox_monthly f ON (c.month_start = f.month_start))
ORDER BY 1 DESC
