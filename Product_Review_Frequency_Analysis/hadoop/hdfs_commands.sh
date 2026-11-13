#!/bin/bash
# Run after starting HDFS services (e.g. start-dfs.sh).
hdfs dfs -mkdir -p /product_reviews/input
hdfs dfs -mkdir -p /product_reviews/output
hdfs dfs -put -f data/product_reviews.csv /product_reviews/input/
hdfs dfs -ls /product_reviews/input
# Optional: read the uploaded CSV
hdfs dfs -cat /product_reviews/input/product_reviews.csv | head
