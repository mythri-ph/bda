from flask import Flask, render_template
from pathlib import Path
import json
from analysis import run_analysis

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

@app.route("/")
def dashboard():
    try:
        _, products, ratings, sentiments, monthly, words, summary = run_analysis()
        return render_template(
            "index.html",
            summary=summary,
            products=products.to_dict(orient="records"),
            ratings=ratings.to_dict(orient="records"),
            sentiments=sentiments.to_dict(orient="records"),
            monthly=monthly.to_dict(orient="records"),
            words=words.to_dict(orient="records"),
            error=None
        )
    except Exception as exc:
        return render_template("index.html", error=str(exc), summary=None,
                               products=[], ratings=[], sentiments=[], monthly=[], words=[])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
