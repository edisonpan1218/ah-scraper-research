import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.ah.nl"

START_URLS = {
    "beef": "https://www.ah.nl/producten/merk/ah/1479/rundvlees?page=1", # 54
    "chicken": "https://www.ah.nl/producten/merk/ah/1226/kip?page=2", # 97
    "pork": "https://www.ah.nl/producten/merk/ah/1643/varkensvlees?page=2", # 89
    "meat_substitutes": "https://www.ah.nl/producten/merk/ah/18041/vleesvervangers", # 4
    "vegetarian_vegetable_meat": "https://www.ah.nl/producten/merk/ah/4743/vegetarische-en-plantaardige-vleeswaren", # 1
    "fresh_fish": "https://www.ah.nl/producten/merk/ah/6539/verse-vis?page=1", # 70
    "frozen_fish": "https://www.ah.nl/producten/merk/ah/6360/diepvries-vis", # 23
    "sweet_vegetables": "https://www.ah.nl/producten/merk/ah/5159/snoepgroente", # 24
    "salad": "https://www.ah.nl/producten/merk/ah/1302/salades?page=1", # 57
    "milk": "https://www.ah.nl/producten/merk/ah/1319/melk", #22
    "yogurt_skyr": "https://www.ah.nl/producten/merk/ah/20878/yoghurt-en-skyr", #27
    "pieces_of_cheese": "https://www.ah.nl/producten/merk/ah/8572/stukken-kaas?page=1", #43
    "spredable_cheese_cream_cheese_cottage_cheese": "https://www.ah.nl/producten/merk/ah/18549/smeerkaas-roomkaas-cottage-cheese", #31
    "fruit_juices_fruit_drinks": "https://www.ah.nl/producten/merk/ah/1677/vruchtensappen-en-fruitdrank?page=2", #85
    "coffee_milk_coffee_cream": "https://www.ah.nl/producten/merk/ah/2765/koffiemelk-koffieroom-koffiecreamer", #11
    "tea": "https://www.ah.nl/producten/merk/ah/2120/thee", #34
    "coke": "https://www.ah.nl/producten/merk/ah/5586/cola", #17
    "fruits_nuts_oats_bars": "https://www.ah.nl/producten/merk/ah/11642/fruit-noten-haver-mueslirepen", #25
    "chips": "https://www.ah.nl/producten/merk/ah/997/chips", #35
    "ready_meals": "https://www.ah.nl/producten/merk/ah/10994/kant-en-klaar-maaltijden?page=1" #37
}

OUTPUT_FILE = "ah_products.csv"


def get_soup(url: str) -> BeautifulSoup:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def crawl_listing(start_url: str) -> list[str]:
    soup = get_soup(start_url)
    urls: list[str] = []

    cards = soup.select("[data-testhook='product-card'], article, a")
    for c in cards:
        a = c.find("a", href=True)
        if a:
            link = urljoin(BASE_URL, a["href"])
            urls.append(link)
    return urls


if __name__ == "__main__":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for category, url in START_URLS.items():
            print(f"Fetch {category}: {url}")
            urls = crawl_listing(url)

            f.write(category + "\n")

            for u in urls:
                f.write(u + "\n")

            print(f"Found {len(urls)} products in category {category}")

    print(f"Saved results to {OUTPUT_FILE}")
