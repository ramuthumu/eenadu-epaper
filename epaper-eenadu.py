import urllib

from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route("/")
def index():
    # Retrieve the latest date
    max_date_url = "https://epaper.eenadu.net/Home/GetMaxdateJson"
    max_date_response = requests.get(max_date_url)
    latest_date = max_date_response.text.replace("\"", "")
    edition_id = 1
    # Retrieve the pages for the latest date and edition ID
    pages_url = f"https://epaper.eenadu.net/Home/GetAllpages?editionid={edition_id}&editiondate={urllib.parse.quote(latest_date)}"

    pages_response = requests.get(pages_url).json()

    print(pages_response)

    return render_template("index.html", pages=pages_response)


if __name__ == "__main__":
    app.run()