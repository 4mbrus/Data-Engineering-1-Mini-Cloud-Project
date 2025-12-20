CREATE EXTERNAL TABLE
ambrus.fox_sentiment (
    title STRING,
    link STRING,          
    date DATE,
    is_economy BOOLEAN,
    sentiment INT,
    topic_inflation INT,
    topic_taxes INT,
    topic_stocks INT,
    topic_jobs INT,
    topic_housing INT,
    topic_energy INT,
    topic_crypto INT)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://business-news-sentiments/news_sentiments/fox';

CREATE EXTERNAL TABLE ambrus.cnn_sentiment (
    title STRING,
    link STRING,          
    date STRING,
    is_economy BOOLEAN,         
    sentiment INT,
    topic_inflation INT,
    topic_taxes INT,
    topic_stocks INT,
    topic_jobs INT,
    topic_housing INT,
    topic_energy INT,
    topic_crypto INT
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://business-news-sentiments/news_sentiments/cnn';

CREATE OR REPLACE VIEW ambrus.cnn_sentiment_clean AS
SELECT 
    title,
    try_cast(date as DATE) as clean_date, -- Optional: Convert string to real date here
    sentiment,
    topic_inflation,
    topic_taxes,
    topic_stocks,
    topic_jobs,
    topic_housing,
    topic_energy,
    topic_crypto
FROM ambrus.cnn_sentiment
WHERE link NOT LIKE '%cnn-underscored%'
  AND link LIKE '%/20__/%'
  AND sentiment IS NOT NULL; 

CREATE OR REPLACE VIEW ambrus.fox_sentiment_clean AS
SELECT 
    title,
    try_cast(date as DATE) as clean_date, -- Optional: Convert string to real date here
    sentiment,
    topic_inflation,
    topic_taxes,
    topic_stocks,
    topic_jobs,
    topic_housing,
    topic_energy,
    topic_crypto
FROM ambrus.fox_sentiment
WHERE sentiment IS NOT NULL; 