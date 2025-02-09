from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

API_KEY = "apikey 7acbJT29LG3ZdrBrp48FF7:2BawyPAiOIkAxkAsn2VmoU"
BASE_URL = "https://api.collectapi.com/economy"


def fetch_data(endpoint):
    headers = {
        "authorization": f"apikey {API_KEY}",
        "content-type": "application/json"
    }
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    
    if response.status_code != 200:
        return {"error": "API'den veri alınamadı", "status": response.status_code}
    
    return response.json()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/bist100", methods=["GET"])
def get_bist100():
    bist_data = fetch_data("/borsaIstanbul")

    # Hata kontrolü
    if "error" in bist_data:
        return jsonify(bist_data)

    # API'nin "result" alanı bir liste içeriyorsa ilk elemanı al
    bist_result = bist_data.get("result", [])
    if isinstance(bist_result, list) and len(bist_result) > 0:
        bist_result = bist_result[0]  # İlk elemanı al

    bist100_info = {
        "name": "BIST 100",
        "current": bist_result.get("current", "Veri Yok"),
        "change": bist_result.get("changerate", "Veri Yok"),
        "min": bist_result.get("min", "Veri Yok"),
        "max": bist_result.get("max", "Veri Yok"),
        "opening": bist_result.get("opening", "Veri Yok"),
        "closing": bist_result.get("closing", "Veri Yok"),
        "time": bist_result.get("time", "Veri Yok"),
        "date": bist_result.get("date", "Veri Yok")
    }

    return jsonify(bist100_info)


@app.route("/hisseler", methods=["GET"])
def get_hisseler():
    stocks = fetch_data("/hisseSenedi")

    if "error" in stocks:
        return jsonify(stocks)

    return jsonify(stocks.get("result", []))


@app.route("/goldPrice", methods=["GET"])
def get_gold_price():
    gold_prices = fetch_data("/goldPrice")

    if "error" in gold_prices:
        return jsonify(gold_prices)

    return jsonify(gold_prices.get("result", []))


if __name__ == "__main__":
    app.run(debug=True)
