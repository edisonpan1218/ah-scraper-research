# Albert Heijn Product Scraper (Research Demo)

This repository contains Python scripts that demonstrate how to **collect and parse product information** from the [Albert Heijn](https://www.ah.nl) website using **Selenium**, **Requests**, and **BeautifulSoup**.  

 **Disclaimer**  
- This project is for **educational and research purposes only**.  
- The scripts are designed as examples of automated data collection.  
- Please make sure that your usage complies with the **Albert Heijn Terms of Service** and relevant laws.  
- No scraped product data is included in this repository.  
- The author does **not encourage large-scale scraping** or redistribution of data.  

---

## Features
- Extract product title, ingredients, and CO₂ info from product pages.  
- Parse ingredients into individual items, expanding parenthesis content.  
- Count number of parsed ingredients and write results into CSV.  

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ah-scraper-research.git
   cd ah-scraper-research
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Manually install ChromeDriver that matches your Chrome version,  
   and place it in your system PATH.  
---

## Usage

1. **Collect product links**  
   Run `get_all_product_link.py` to fetch all product URLs from the selected categories.  You get ah_products.csv after executing it.
   ```bash
   python src/get_all_product_link.py
   ```

2. **Scrape product information**  
   Use `get_product_info.py` to visit each product page and extract details such as title, ingredients, and CO₂ info.  You get thesis_data.csv after executing it.
   ```bash
   python src/get_product_info.py
   ```

3. **Parse and update ingredients**  
   Finally, run `ingredient_update.py` to re-parse the ingredients column, expand items inside parentheses, and update the CSV you select with the corrected ingredient counts.  You get the csv_update after executing it.
   ```bash
   python src/ingredient_update.py
   ```

---

## Example Output 

| Category | ProductName | LabelStatus | CO2  | IngredientAmount | Ingredients | All items |
| -------- | -------- | -------- | -------- | -------- | -------- |  ----- | 
| beef     |   AH Mergpijp   | 0 | | 1 | Ingrediënten: rundvlees. | ([rundvlees])

---

