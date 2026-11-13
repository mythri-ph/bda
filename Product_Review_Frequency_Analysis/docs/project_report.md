# Project Report: Product Review Frequency Analysis

## Abstract
Product Review Frequency Analysis is a Big Data Analytics project that studies product-review records to identify review volume, customer rating patterns, frequently used terms and review trends. The application uses Python and pandas for a local execution path, Flask and Chart.js for dashboard presentation, and includes optional Hadoop HDFS, Apache Hive and Apache Spark components for distributed-data demonstrations.

## Problem statement
Online platforms generate large volumes of customer reviews. Manually examining this information makes it difficult to identify popular products, understand rating patterns and track customer feedback. A scalable analytical workflow is needed to organise and summarise review data.

## Objectives
1. Calculate the number of reviews for each product.
2. Identify products with high review frequency.
3. Calculate average product ratings.
4. estimate positive, negative and neutral sentiment.
5. Identify frequently occurring words in review text.
6. Analyse monthly review trends.
7. Present results in an interactive dashboard.

## System architecture
Review CSV -> Data validation and cleaning -> HDFS (optional storage) -> Spark/Hive (distributed analysis) -> Aggregated outputs -> Flask application -> Chart.js dashboard.

## Methodology
1. Load the review CSV file.
2. Validate required fields and data types.
3. Remove duplicate review IDs and invalid ratings/dates.
4. Group records by product to calculate review frequency and average rating.
5. Apply a rule-based sentiment baseline to review text.
6. Tokenise review text and count frequent words.
7. Group reviews by month.
8. Display results in the dashboard.

## Algorithms
### Product review frequency
Input: Review dataset.
1. Read the review records.
2. Validate and clean the records.
3. Group records using product ID and product name.
4. Count review IDs in each group.
5. Sort products by count in descending order.
6. Save and display the results.

### Rule-based sentiment baseline
1. Convert review text to lowercase.
2. Tokenise the text.
3. Count words in positive and negative word lists.
4. Calculate positive count minus negative count.
5. Label positive score as Positive, negative score as Negative, otherwise Neutral.

## Software and hardware requirements
Software: Python 3.10+, Flask, pandas, optional Java/Hadoop/Hive/Spark, VS Code or another editor, modern browser.
Hardware: 4 GB RAM minimum for local demonstration; more memory and distributed infrastructure are recommended for larger data. Hadoop/Spark requirements depend on deployment mode.

## Results
The included synthetic demonstration dataset contains 20 sample review rows and 5 products. Run `python analysis.py` to generate the exact aggregate results for the supplied CSV. Replace the sample with a permitted real dataset before claiming real-world findings.

## Conclusion
The system automates product review aggregation and visualises product frequency, ratings, sentiment estimates, common terms and monthly trends. The modular design supports a local demonstration and provides optional Spark, HDFS and Hive components for a Big Data lab environment.

## Future enhancement
Use a larger licensed/public dataset, train and evaluate a machine-learning sentiment classifier, add date/product filters, secure user authentication, and deploy the dashboard to a production hosting platform.
