# Hissenin yerini değiştirdikten sonra fiyat güncellemesi yaptıktan sonra tekrar eski yerine geçiyor
from flask import Flask, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

BASE_URL = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx"

def fetch_hisse_data(hisse_kodlari):
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        return []

    parser = BeautifulSoup(response.content, "html.parser")
    hisse_verileri = []

    for sirket in hisse_kodlari:
        try:
            fiyat = parser.find("a", {"href": f"/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={sirket.upper()}"})\
                .parent.parent.find_all("td")

            hisse_bilgisi = {
                "code": sirket.upper(),
                "text": fiyat[0].a.string.strip(),
                "lastprice": fiyat[1].string.strip(),
                "rate": fiyat[2].span.string.strip(),
                "volume_tl": fiyat[4].string.strip(),
                "volume_lot": fiyat[5].string.strip(),
                "icon": f"static/{sirket.upper()}.png" if os.path.exists(f"static/{sirket.upper()}.png") else "static/default.png"
            }
            hisse_verileri.append(hisse_bilgisi)

        except AttributeError:
            print(f"Hata: {sirket} için veri bulunamadı.")

    return hisse_verileri

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/hisseler", methods=["GET"])
def get_hisseler():
    hisse_kodu = request.args.get("hisse")
    
    if hisse_kodu:
        hisse_listesi = [hisse_kodu.upper()]
    else:
        hisse_listesi = ["THYAO", "ASELS", "KRDMD", "GARAN", "TTRAK"]

    return jsonify(fetch_hisse_data(hisse_listesi))

if __name__ == "__main__":
    app.run(debug=True)
