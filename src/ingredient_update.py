import pandas as pd
import re

INPUT_PATH = "ready_meals.csv"
OUTPUT_PATH = "ready_meals_updated.csv"

def slice_after_last_colon_to_period(s: str) -> str:
    """取最後一個冒號之後到下一個句點前的文字"""
    if not isinstance(s, str):
        return ""
    text = s.strip()
    if not text:
        return ""
    last_colon = text.rfind(":")
    if last_colon == -1:
        return text[:-1] if text.endswith(".") else text
    next_period = text.find(".", last_colon + 1)
    return text[last_colon + 1:next_period].strip() if next_period != -1 else text[last_colon + 1:].strip()

def parse_ingredients(text: str):
    """
    用 ', ' 切分，避免 0,1% 被拆開；
    如果有括號，只取括號裡並用 ',' 拆；
    外層 prefix 不算。
    """
    if not isinstance(text, str):
        return []

    core = slice_after_last_colon_to_period(text)
    if not core:
        core = text.strip().rstrip(".")

    parts = [p.strip() for p in core.split(", ") if p.strip()]

    items = []
    for part in parts:
        if "(" in part and ")" in part:
            inner = re.search(r"\((.*?)\)", part)
            if inner:
                items.extend([p.strip() for p in inner.group(1).split(",") if p.strip()])
        else:
            items.append(part.strip())
    return items

def main():
    df = pd.read_csv(INPUT_PATH, encoding="latin-1")

    # 找到 ingredients 欄位
    ing_col = [c for c in df.columns if "ingredients" in c.lower()]
    if not ing_col:
        raise ValueError("No ingredients column found!")
    ing_col = ing_col[0]

    # 清空再重建兩欄
    df["IngredientAmount"] = 0
    df["All items"] = ""

    for idx, row in df.iterrows():
        parsed = parse_ingredients(row[ing_col])
        df.at[idx, "IngredientAmount"] = len(parsed)
        df.at[idx, "All items"] = ", ".join(parsed)

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print(f"Saved updated file to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
