from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route("/")
def today_editions():
    default_details_endpoint = "https://epaper.eenadu.net/Home/GetDefaultDetails?edid=0"
    res = requests.get(default_details_endpoint)
    default_details = res.json()

    date = default_details["MxDate"] + " " + default_details["DefaultDate"]
    editions_endpoint = f"https://epaper.eenadu.net/Login/GetMailEditionPages?Date={default_details['DefaultDate']}"
    res = requests.get(editions_endpoint)
    editions = res.json()

    return render_template("today_editions.html", date=date, editions=editions)


if __name__ == "__main__":
    app.run()
