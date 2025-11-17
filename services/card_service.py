from db.db_service import  insert_tracked_card, delete_tracked_card, insert_card
from scrapper.basic import scrapp_url, get_lower_price, parse_cardmarket_results
import asyncio
from services.card_data import CARDMARKET_COLLECTIONS

import re


async def fetch_cards(code):
    html = await scrapp_url(code)  # Esto debe ser await si sigue siendo async
    matches = await parse_cardmarket_results(html)
    filtered_matches = [card for card in matches if "Japanese" not in card["url"]]
            
    cards_with_prices = await asyncio.gather(*(get_lower_price(card) for card in filtered_matches))
    cards_with_prices = [card for card in cards_with_prices if isinstance(card, dict)]
    inserted_cards = set()
    try:
        for i, card in enumerate(cards_with_prices):
            print(f"\n📦 CARD #{i} = {card} (type: {type(card)})")
            if not isinstance(card, dict):
                print(f"❌ Saltando, no es un dict → {card}")
                continue
            try:
                extract_collection_from_url(card)
                new_card = insert_card(card)
                inserted_cards.add(new_card)
            except Exception as e:
                print(f"⚠️ Error al extraer colección: {e} → {card}")
   
    except Exception as e:
        print(f"⚠️ Error en fetch_cards: {e}")

        
    return inserted_cards


def track_card(data):
    insert_tracked_card(data)
    return {"message": "Card tracked"}

def untrack_card(card_id):
    delete_tracked_card(card_id)
    return {"message": "Card untracked"}



def normalize(text):
    return text.lower().replace(":", "").replace(" - ", " ").replace("–", " ").replace("&", "and").replace("-", " ").strip()

def extract_collection_from_url(card):
    if not isinstance(card, dict) or "url" not in card:
        print("❌ Valor inválido recibido en extract_collection_from_url:", card)
        return card

    url = card.get("url", "").lower()
    parts = url.split("/")

    if len(parts) <= 7:
        card["collection"] = None
        return card

    raw_collection = parts[7]  # Ej: 'romance-dawn', 'promos-royal-blood', etc.
    url_words = set(normalize(raw_collection).split())
    best_match = None
    best_match_score = 0

    for collection in CARDMARKET_COLLECTIONS:
        name = collection["name"]
        name_words = set(normalize(name).split())

        # Solo consideramos colección válida si contiene TODAS las palabras del URL
        if url_words.issubset(name_words):
            score = len(url_words) / len(name_words)  # Cuanto más cercano a 1, mejor
            if score > best_match_score:
                best_match_score = score
                best_match = name
        else:
            best_match = normalize(raw_collection).title()

    card["collection"] = best_match
    return card
