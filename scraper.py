import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://www.teleborsa.it/obbligazioni-titoli-di-stato/btp-valore-sc-ot32-eur-it0005672024-it0005672024-SVQwMDA1NjcyMDI0"

response = requests.get(URL, timeout=20)
soup = BeautifulSoup(response.text, "html.parser")

price_element = soup.select_one("span.valore")  # ggf. anpassen
if not price_element:
    raise Exception("Kurselement nicht gefunden!")

price = price_element.text.strip().replace(",", ".")
price_float = float(price)

try:
    with open("feed.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"currency": "EUR", "data": []}

today = datetime.today().strftime("%Y-%m-%d")
existing = {d["date"]: d for d in data["data"]}
existing[today] = {"date": today, "close": price_float}
data["data"] = list(sorted(existing.values(), key=lambda x: x["date"]))

with open("feed.json", "w") as f:
    json.dump(data, f, indent=2)

print("Feed aktualisiert:", today, price_float)
