-- Run in Hive after ensuring the CSV is available in HDFS.
CREATE DATABASE IF NOT EXISTS product_review_db;
USE product_review_db;

DROP TABLE IF EXISTS product_reviews;
CREATE EXTERNAL TABLE product_reviews (
  review_id STRING,
  product_id STRING,
  product_name STRING,
  reviewer_id STRING,
  review_text STRING,
  rating INT,
  review_date STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = "\""
)
STORED AS TEXTFILE
LOCATION '/product_reviews/input'
TBLPROPERTIES ("skip.header.line.count"="1");

-- Most reviewed products
SELECT product_id, product_name, COUNT(*) AS review_frequency
FROM product_reviews
GROUP BY product_id, product_name
ORDER BY review_frequency DESC;

-- Average rating by product
SELECT product_id, product_name, ROUND(AVG(rating), 2) AS average_rating
FROM product_reviews
GROUP BY product_id, product_name
ORDER BY average_rating DESC;

-- Rating distribution
SELECT rating, COUNT(*) AS total_reviews
FROM product_reviews
GROUP BY rating
ORDER BY rating;
