from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List, Tuple
import time
import re
import csv

OUTPUT_CSV = "thesis_data.csv"


def write_header(path: str = OUTPUT_CSV):
    fieldnames = ["Category", "ProductName", "LabelStatus", "CO2 (kg C02e per kg)", "IngredientAmount", "Ingredients", "All items"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)


def append_row(category: str, title: str, label_status: int, carbonContain: float, ingredient_amount: int, ingredients: str,
               items: str,
               path: str = OUTPUT_CSV):
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([category, title, label_status, carbonContain, ingredient_amount, ingredients, items])


# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testhook='accept-cookies']")))
# button = driver.find_element(By.CSS_SELECTOR, "button[data-testhook='accept-cookies']")
# button.click()

E_CODE_RE = re.compile(r"\[E\d{3}[a-zA-Z]?\]")

def load_grouped_urls(path: str) -> Dict[str, List[str]]:
    """
    Reads a text/CSV file where category lines are followed by URL lines
    until the next category. Blank lines are ignored.

    Returns: dict {category: [urls...]} with categories in lowercase.
    """
    urls_by_cat: Dict[str, List[str]] = {}
    current_cat: str | None = None

    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue  

            if line.startswith("http://") or line.startswith("https://"):
                if current_cat is None:
                    current_cat = "uncategorized"
                    urls_by_cat.setdefault(current_cat, [])
                urls_by_cat.setdefault(current_cat, []).append(line)
            else:
                current_cat = line.strip().lower()
                urls_by_cat.setdefault(current_cat, [])

    return urls_by_cat

def get_carbon(text: str) -> float:
    match = re.search(r":\s*([\d.,]+)\s*kg", text, flags=re.IGNORECASE)
    if match:
        return float(match.group(1).replace(",", "."))
    return 0.0

def crawl_product_page(url: str):
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.product-card-header_root__c8eM5 h1 span")))

    product_title = driver.find_element(By.CSS_SELECTOR, "div.product-card-header_root__c8eM5 h1 span").text

    print("Product Title:", product_title)


    ingredients = "404NotFound"
    try: 
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='product-info-content-block'][.//h2[text()='Ingrediënten']]")))
        ingredient_block = driver.find_element(
            By.XPATH, "//div[@class='product-info-content-block'][.//h2[text()='Ingrediënten']]"
        )

        ingredients = ingredient_block.find_element(By.TAG_NAME, "p").text
        print("Ingredients:", ingredients)
    except:
        print("Ingredients not found")
    

    check = False
    carbonContain = -1.0
    try:
        klimaat_h4 = driver.find_element(By.XPATH, "//h4[text()='Klimaat']")
        klimaat_p = klimaat_h4.find_element(By.XPATH, "following-sibling::p")
        carbonContain = get_carbon(str(klimaat_p.text))
        check = True
        print("Heading:", klimaat_h4.text)
        print("CO2 info:", klimaat_p.text)
        print("carbon:", carbonContain)
    except:
        print("Heading not found")

    driver.quit()
    return product_title, ingredients, check, carbonContain


def split_ingredients_parentheses_aware(text: str) -> list[str]:
    """
    Split ingredients by commas, but if a comma is inside parentheses,
    split them out as separate items (e.g. a(b,c,d) -> b, c, d).
    """
    items, buf, depth = [], [], 0
    for ch in text:
        if ch == "(":
            depth += 1
            buf.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1)
            buf.append(ch)
        elif ch == "," and depth == 0:
            piece = "".join(buf).strip()
            if piece:
                items.append(piece)
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        items.append(tail)

    # Now expand parentheses content into separate items
    expanded = []
    for it in items:
        if "(" in it and ")" in it:
            # split into prefix + inner
            prefix, inner = it.split("(", 1)
            inner = inner.rsplit(")", 1)[0]  # remove last ")"
            parts = [p.strip() for p in inner.split(",") if p.strip()]
            expanded.extend(parts)
        else:
            expanded.append(it.strip())

    return expanded

def count_ingredients(text: str) -> int:
    """
    Return total count of ingredients from a full 'Ingredients: ...' string.
    """
    # Extract the core part after the last ":" and before the final "."
    last_colon = text.rfind(":")
    core = text[last_colon + 1:].strip() if last_colon != -1 else text.strip()
    if core.endswith("."):
        core = core[:-1]

    items = split_ingredients_parentheses_aware(core)
    return len(items), items


if __name__ == "__main__":
    write_header()
    PATH = "ah_products.csv"

    URLS_BY_CATEGORY = load_grouped_urls(PATH)

    # If you want a flat list of URLs only (all categories combined):
    # ALL_URLS: List[str] = [u for urls in URLS_BY_CATEGORY.values() for u in urls]

    # If you want (category, url) pairs:
    PAIRS_URLS: List[Tuple[str, str]] = [
        (cat, url) for cat, urls in URLS_BY_CATEGORY.items() for url in urls
    ]

    for category, URL in PAIRS_URLS:
        product_title, ingredients, check, carbonContain = crawl_product_page(URL)
        total_count, items = count_ingredients(ingredients)
        append_row(category, product_title, 1 if check else 0, carbonContain, total_count, ingredients, items)



