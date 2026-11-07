import requests
from bs4 import BeautifulSoup
import pandas as pd

URL_TARGET = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

def extract_laptops():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(URL_TARGET, headers=headers, timeout=10)
    if response.status_code != 200:
        raise ConnectionError(f"Error HTTP {response.status_code}")
        
    soup = BeautifulSoup(response.text, "html.parser")
    productos = []
    cards = soup.select("div.thumbnail")
    
    for card in cards:
        titulo_el = card.select_one("a.title")
        precio_el = card.select_one(".price")
        desc_el = card.select_one(".description")
        
        titulo = titulo_el.get("title") if titulo_el and titulo_el.has_attr("title") else (titulo_el.text.strip() if titulo_el else "N/A")
        precio = precio_el.text.strip() if precio_el else "N/A"
        desc = desc_el.text.strip() if desc_el else "N/A"
        link = "https://webscraper.io" + titulo_el["href"] if titulo_el and titulo_el.has_attr("href") else "N/A"
        
        productos.append({
            "Herramienta": "BeautifulSoup-DevOps",
            "Titulo": titulo,
            "Precio": precio,
            "Descripcion": desc,
            "Enlace": link
        })
    return productos

def save_to_csv(data, filename="laptops_extracted.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")
    return filename

if __name__ == "__main__":
    data = extract_laptops()
    save_to_csv(data)
