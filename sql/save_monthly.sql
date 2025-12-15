CREATE TABLE "ambrus"."fox_monthly_export_json"
WITH (
    format = 'JSON',
    external_location = 's3://business-news-sentiments/news_sentiments_monthly/fox/'
) AS
SELECT
    date_format("date", '%Y-%m') AS month_year,
    SUM("sentiment") AS total_sentiment
FROM
    "ambrus"."fox_sentiment"
GROUP BY
    1
ORDER BY
    1 DESC;

CREATE TABLE "ambrus"."cnn_monthly_export_json"
WITH (
    format = 'JSON',
    external_location = 's3://business-news-sentiments/news_sentiments_monthly/cnn/'
) AS
SELECT
    date_format("date", '%Y-%m') AS month_year,
    SUM("sentiment") AS total_sentiment
FROM
    "ambrus"."cnn_sentiment"
GROUP BY
    1
ORDER BY
    1 DESC;