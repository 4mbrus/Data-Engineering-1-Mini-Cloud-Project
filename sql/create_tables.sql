CREATE EXTERNAL TABLE
ambrus.fox_sentiment (
    title STRING,
    date DATE,
    sentiment INT)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://business-news-sentiments/news_sentiments/fox';

CREATE EXTERNAL TABLE
ambrus.cnn_sentiment (
    title STRING,
    date DATE,
    sentiment INT)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://business-news-sentiments/news_sentiments/cnn';