# catas48925@perceint.com
# apikey 25lxwtagzTqogQQ58PFwv4:31OBfGTU3paM7pqEFvLe8I

import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# API isteği
url = "https://api.collectapi.com/economy/hisseSenedi"
headers = {
    "authorization": "apikey 25lxwtagzTqogQQ58PFwv4:31OBfGTU3paM7pqEFvLe8I",  # API anahtarını buraya koy
    "content-type": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # Verileri işleyelim
    hisse_listesi = []
    for item in data['result']:
        hisse_listesi.append({
            "Hisse Kodu": item["code"],          # Hisse sembolü
            "Şirket Adı": item["text"],          # Şirket adı
            "Son Fiyat": item["lastprice"],      # Güncel fiyat
            "Değişim (%)": item["rate"],         # Yüzdesel değişim
            "Günlük En Düşük": item["min"],      # Günlük minimum fiyat
            "Günlük En Yüksek": item["max"],     # Günlük maksimum fiyat
            "Hacim (₺)": item["hacim"],          # Hacim bilgisi
            "Saat": item["time"]                 # Son güncelleme saati
        })
    
    # Pandas DataFrame ile tablo oluştur
    df = pd.DataFrame(hisse_listesi)

    # Tabloyu terminalde göster
    print(df)

    

else:
    print("Hata! API isteği başarısız. HTTP Kodu:", response.status_code)

# En yüksek hacme sahip ilk 10 hisseyi al
df_sorted = df.sort_values(by="Hacim (₺)", ascending=False).head(10)

# Grafik çizimi
plt.figure(figsize=(12, 6))
plt.bar(df_sorted["Hisse Kodu"], df_sorted["Son Fiyat"], color="blue")

# Başlık ve etiketler
plt.xlabel("Hisse Kodu")
plt.ylabel("Son Fiyat (₺)")
plt.title("Borsa İstanbul En Yüksek Hacimli 10 Hisse")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Grafiği göster
plt.show()

# Örnek olarak en yüksek hacimli hisseyi seçelim
hisse_kodu = df_sorted.iloc[0]["Hisse Kodu"]  # İlk hisseyi al
print(f"RSI hesaplanıyor: {hisse_kodu}")

# Rasgele kapanış fiyatları oluşturalım (Gerçek fiyat verilerini API'den tarihsel olarak çekmek gerekir)
np.random.seed(42)
prices = np.random.uniform(low=50, high=300, size=30)  # 30 günlük fiyat üretelim

# RSI hesaplama fonksiyonu
def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    rsi_list = []
    for i in range(period, len(prices)):
        avg_gain = (avg_gain * (period - 1) + gains[i - 1]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i - 1]) / period

        rs = avg_gain / avg_loss if avg_loss != 0 else np.inf
        rsi = 100 - (100 / (1 + rs))
        rsi_list.append(rsi)

    return np.array(rsi_list)

# RSI hesapla
rsi_values = calculate_rsi(prices)

# Grafik çizelim
plt.figure(figsize=(12, 5))
plt.plot(rsi_values, label=f"{hisse_kodu} RSI", color="purple")
plt.axhline(70, linestyle="--", color="red", label="Aşırı Alım (70)")
plt.axhline(30, linestyle="--", color="green", label="Aşırı Satım (30)")

plt.title(f"{hisse_kodu} RSI Grafiği")
plt.xlabel("Gün")
plt.ylabel("RSI Değeri")
plt.legend()
plt.grid()
plt.show()


