import base64
import sys
import time
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import asyncio
from io import BytesIO


STATE_FILE = "storage_state.json"
HTML_DUMP = "search_result.html"
SEARCH_QUERY = "https://www.cardmarket.com/es/OnePiece/Products/Search?searchString="
BOT_TOKER = "7194405151:AAHdeuhVtwmokePq0sEdJQwMR7dRY8CxR3Up"
IMG_URL = "https://en.onepiece-cardgame.com/images/cardlist/card/"
async def scrapp_url(query: str):
    
    async with async_playwright() as p:
        iphone = p.devices["iPhone 12"]
        browser = await  p.chromium.launch(headless=True)
        context = await  browser.new_context(**iphone)
        page = await  context.new_page()

        
        print(f"🔍 Buscando: {query}")
        try:
            await page.goto(query, timeout=60000, wait_until="domcontentloaded")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error al cargar la página: {e}")
            return ""

        html = await page.content()
        
        await browser.close()

        create_file("search_result", html)
        return html

async def parse_cardmarket_results(html):
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one("div.table-body")

    if not container:
        print("⚠️ No se encontró el contenedor principal 'div.table-body'")
        return []

    results = []
    product_rows = container.select("div[id^=productRow]")

    for row in product_rows:
        # Imagen desde data-bs-title
        span_icon = row.select_one("div.col-icon span[data-bs-title]")
        img_url = None

        if span_icon:
            tooltip_html = span_icon.get("data-bs-title", "")
            match = re.search(r'src="(.*?)"', tooltip_html)
            if match:
                img_url = match.group(1)

        # Nombre y URL
        a_tag = row.select_one("div.col a[href]")
        name_tag = row.select_one("div.col .d-block.small.text-muted.fst-italic")

        card_url = f"https://www.cardmarket.com{a_tag['href']}" if a_tag else None
        card_name = name_tag.get_text(strip=True) if name_tag else None
        
        codigo = (m := re.search(r"\((OP\d{2}-\d{3})\)", card_name)) and m.group(1)
        version = (v := re.search(r"\((V\.\d+)\)", card_name)) and v.group(1)

        new_img = IMG_URL + codigo
        if extraer_set_id(img_url):
            new_img = new_img + "_p2"
            card_name = card_name + " PB-XX"
            version = "PB-XX"
        if version == 'V.2':
            new_img = new_img + "_p1"

        if card_url.__contains__("Japanese"):
            card_name = card_name + " JP"

        if card_url and card_name and img_url:
            results.append({
                "text": card_name,
                "url": card_url,
                "image": new_img + ".png",
                "code": codigo,
                'version': version
            })
        else:
            print("❌ Elemento incompleto:", {
                "name": card_name,
                "url": card_url,
                "image": new_img
            })

    return results

async def parse_sellers(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    rows = soup.select("div.article-row")
    sellers = []

    row = rows[0]
    try:
            
        location_tag = row.select_one("span.icon[aria-label]")
        seller_country = location_tag["aria-label"].replace("Ubicación del artículo: ", "") if location_tag else "¿?"
        
        condition_tag = row.find_next("div", class_="product-attributes col").find_next("span", class_="badge")
        condition = condition_tag.text.strip() if condition_tag else "¿?"
        
        price_tag = row.find_next("span", class_="color-primary small text-end text-nowrap fw-bold")
        price = price_tag.text.replace("€", "").strip() if price_tag else "¿?"

        amount_tag = row.select_one("div.col-offer span.item-count")
        quantity = amount_tag.text.strip() if amount_tag else "¿?"

        sellers.append({
            "country": seller_country,
            "condition": condition,
            "price": float(price.replace(",", ".")),
            "quantity": quantity
        })

    except Exception as e:
        print(f"⚠️ Error al procesar una fila: {e}")

    return sellers

async def get_lower_price(card):
    filtered_url = card["url"] + "?language=1"
    html = await scrapp_url(filtered_url)
    price = await parse_sellers(html) 
    
    return {
        **card,
        **price[0],
        "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def create_file(name, content):
     with open(f"{name}.json", "w", encoding="utf-8") as out:
                json.dump(content, out, indent=2, ensure_ascii=False)

def extraer_set_id(url):
   return bool(re.search(r"/PB-[A-Z0-9]+/", url))

if __name__ == "__main__":

    try:
        if len(sys.argv) < 2:
            print("❗ Uso: python basic_mobile.py <nombre o código de carta>")
            sys.exit(1)

        query = sys.argv[1]
        html = scrapp_url(SEARCH_QUERY + query)
        matches = parse_cardmarket_results(html)

        if not matches:
            print("⚠️ No se encontraron resultados.")
   
        selection = int(input("🔽 Selecciona el número de la carta: ").strip())

        if 1 <= selection <= len(matches):

            selected_card = matches[selection - 1]
            print(f"\n🔁 Buscando precios para: {selected_card['text']}")
            
            lower_card = get_lower_price(selected_card) 

            create_file("lower_price_card", lower_card)
            

        else:
            print("❌ Selección no válida.")
    except ValueError:
        print("❌ Entrada inválida. Introduce un número.")


