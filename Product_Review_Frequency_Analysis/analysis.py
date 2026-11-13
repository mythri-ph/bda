"""Local analysis pipeline for Product Review Frequency Analysis."""
from pathlib import Path
import re
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "product_reviews.csv"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

REQUIRED = ["review_id", "product_id", "product_name", "review_text", "rating", "review_date"]
POSITIVE = {
    "excellent", "great", "good", "amazing", "love", "fast", "comfortable",
    "useful", "perfectly", "recommend", "reliable", "accurate", "helpful",
    "sturdy", "stable", "clear", "nice", "decent", "quality"
}
NEGATIVE = {
    "poor", "bad", "disappointing", "stopped", "drains", "quickly", "unstable",
    "average", "stiff", "not", "worth", "broken", "slow", "issue", "problem"
}
STOPWORDS = {
    "the", "and", "is", "a", "an", "for", "to", "of", "with", "but", "it",
    "my", "on", "at", "in", "after", "very", "this", "that", "i", "me",
    "was", "are", "be", "by", "long", "use", "your", "its", "its"
}

def load_reviews(path=DATA_FILE):
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing required CSV columns: " + ", ".join(missing))
    df = df[REQUIRED + (["reviewer_id"] if "reviewer_id" in df.columns else [])].copy()
    df["review_text"] = df["review_text"].fillna("").astype(str).str.strip()
    df["product_name"] = df["product_name"].fillna("Unknown product").astype(str)
    df["product_id"] = df["product_id"].fillna("UNKNOWN").astype(str)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    df = df.dropna(subset=["rating", "review_date"])
    df = df[df["rating"].between(1, 5)]
    df = df.drop_duplicates(subset=["review_id"])
    return df

def sentiment(text):
    tokens = re.findall(r"[a-zA-Z']+", str(text).lower())
    score = sum(t in POSITIVE for t in tokens) - sum(t in NEGATIVE for t in tokens)
    if score > 0:
        return "Positive"
    if score < 0:
        return "Negative"
    return "Neutral"

def token_counts(texts):
    counts = {}
    for text in texts:
        for token in re.findall(r"[a-zA-Z]{3,}", str(text).lower()):
            if token not in STOPWORDS:
                counts[token] = counts.get(token, 0) + 1
    return counts

def run_analysis():
    df = load_reviews()
    if df.empty:
        raise ValueError("No valid reviews found in the dataset.")
    df["sentiment"] = df["review_text"].apply(sentiment)
    df["month"] = df["review_date"].dt.to_period("M").astype(str)

    product = (df.groupby(["product_id", "product_name"], as_index=False)
                 .agg(review_count=("review_id", "count"),
                      average_rating=("rating", "mean"),
                      positive_reviews=("sentiment", lambda s: (s == "Positive").sum()),
                      negative_reviews=("sentiment", lambda s: (s == "Negative").sum()),
                      neutral_reviews=("sentiment", lambda s: (s == "Neutral").sum()))
                 .sort_values("review_count", ascending=False))
    product["average_rating"] = product["average_rating"].round(2)

    ratings = df.groupby("rating").size().reindex([1, 2, 3, 4, 5], fill_value=0).rename("count").reset_index()
    sentiments = df["sentiment"].value_counts().reindex(["Positive", "Neutral", "Negative"], fill_value=0).rename_axis("sentiment").reset_index(name="count")
    monthly = df.groupby("month").size().rename("review_count").reset_index()
    words = token_counts(df["review_text"])
    word_df = pd.DataFrame(sorted(words.items(), key=lambda x: (-x[1], x[0]))[:20], columns=["word", "frequency"])

    product.to_csv(OUT_DIR / "product_frequency.csv", index=False)
    ratings.to_csv(OUT_DIR / "rating_distribution.csv", index=False)
    sentiments.to_csv(OUT_DIR / "sentiment_distribution.csv", index=False)
    monthly.to_csv(OUT_DIR / "monthly_trend.csv", index=False)
    word_df.to_csv(OUT_DIR / "top_words.csv", index=False)
    df.to_csv(OUT_DIR / "cleaned_reviews.csv", index=False)

    summary = {
        "total_reviews": int(len(df)),
        "unique_products": int(df["product_id"].nunique()),
        "average_rating": round(float(df["rating"].mean()), 2),
        "most_reviewed_product": str(product.iloc[0]["product_name"]),
        "positive_reviews": int((df["sentiment"] == "Positive").sum()),
        "negative_reviews": int((df["sentiment"] == "Negative").sum()),
        "neutral_reviews": int((df["sentiment"] == "Neutral").sum())
    }
    import json
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return df, product, ratings, sentiments, monthly, word_df, summary

if __name__ == "__main__":
    _, _, _, _, _, _, summary = run_analysis()
    print("Analysis completed.")
    print(summary)
    print(f"Output files saved in: {OUT_DIR}")
