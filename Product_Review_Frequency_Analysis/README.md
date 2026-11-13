# Product Review Frequency Analysis

A runnable Big Data Analytics mini-project that analyses product reviews, calculates review frequency, extracts common terms, estimates sentiment, and displays results in a Flask dashboard.

## Important dataset note
`data/product_reviews.csv` contains **synthetic demonstration data** so the project runs immediately. It is not scraped Amazon data and should not be described as real customer data. You can replace it with a permitted/public product-review dataset using the column format below.

Required CSV columns:
- `review_id`
- `product_id`
- `product_name`
- `review_text`
- `rating` (1–5)
- `review_date` (YYYY-MM-DD)

Optional: `reviewer_id`

## 1. Run locally (Windows / Linux)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Ubuntu/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

If `python` is not recognised, try `py` on Windows or `python3` on Ubuntu.

## 2. Run analysis without the website
```bash
python analysis.py
```
Outputs are saved under `outputs/`.

## 3. Use your own dataset
Replace `data/product_reviews.csv` with your dataset, keeping the required headers. Then run `python analysis.py` and refresh the dashboard.

## 4. Optional PySpark job
Install/configure Java and Spark, install PySpark, then:
```bash
spark-submit scripts/spark_analysis.py data/product_reviews.csv outputs/spark
```
This job calculates product review counts and rating summaries using Spark. Local mode works when PySpark and Java are configured.

## 5. Optional Hadoop HDFS commands
See `hadoop/hdfs_commands.sh`. These commands assume Hadoop is installed and HDFS services are running.

## 6. Optional Hive queries
See `hive/product_review_analysis.hql`. Create the database/table and load a CSV file placed in HDFS at the path specified in the script.

## Project modules
1. Data loading and validation
2. Data cleaning
3. Product-wise review frequency
4. Rating distribution and average rating
5. Lexicon-based sentiment estimate
6. Frequent review terms
7. Monthly review trend
8. Flask dashboard
9. Optional Spark, HDFS and Hive integration

## Limitations
- The included sentiment analysis is a transparent rule-based baseline, not a trained machine-learning model.
- Word frequency is a simple token count; it does not understand context or negation perfectly.
- The local pandas analysis is intended for demonstration/small-to-medium files. Use the Spark job for distributed processing.
