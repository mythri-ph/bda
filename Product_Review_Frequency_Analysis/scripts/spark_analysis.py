"""Optional distributed product frequency analysis using PySpark.
Run: spark-submit scripts/spark_analysis.py data/product_reviews.csv outputs/spark
"""
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg, col

input_path = sys.argv[1] if len(sys.argv) > 1 else "data/product_reviews.csv"
output_path = sys.argv[2] if len(sys.argv) > 2 else "outputs/spark"

spark = SparkSession.builder.appName("ProductReviewFrequencyAnalysis").getOrCreate()
reviews = spark.read.option("header", True).option("inferSchema", True).csv(input_path)
required = {"review_id", "product_id", "product_name", "rating", "review_date"}
missing = required - set(reviews.columns)
if missing:
    raise ValueError("Missing columns: " + ", ".join(sorted(missing)))

clean = reviews.dropna(subset=["review_id", "product_id", "rating"]).dropDuplicates(["review_id"])
result = (clean.groupBy("product_id", "product_name")
          .agg(count("*").alias("review_count"),
               avg(col("rating").cast("double")).alias("average_rating"))
          .orderBy(col("review_count").desc()))
result.write.mode("overwrite").option("header", True).csv(output_path)
result.show(truncate=False)
spark.stop()
