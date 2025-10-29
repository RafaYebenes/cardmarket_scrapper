from flask import Flask, request, jsonify
from flask_cors import CORS
from scrapper.basic import parse_cardmarket_results, scrapp_url, get_lower_price
from services.card_service import fetch_cards
from db import db_service
import asyncio
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://opchecker.duckdns.org:5173"]}})


@app.route("/api/cards", methods=["GET"])
def get_cards():
    cards = db_service.get_all_cards()
    return jsonify(cards)

@app.route("/api/track", methods=["POST"])
def track_card():
    data = request.get_json()

    user_id = data.get("user_id")
    card_id = data.get("card_id")
    country = data.get("country")
    condition = data.get("condition")
    quantity = data.get("quantity")

    tracked_card = {
        "user_id": user_id,
        "card_id": card_id,
        "country": country,
        "condition": condition,
        "quantity": quantity,
        "last_price": 0,
        "last_check": None
    }

    result = db_service.insert_tracked_card(tracked_card)
    return jsonify({"success": result is not None, "id": result})


@app.route("/api/search_cards", methods=["POST"])
async def search_card():
    data = request.get_json()
    code = data.get("code")

    if not code:
        return jsonify({"error": "Missing card code"}), 400

    query_url = f"https://www.cardmarket.com/es/OnePiece/Products/Search?searchString={code}"

    try:
        # Llamamos sea las funciones async
        matches = await fetch_cards(query_url)
        
        return matches
    
    except Exception as e:
        print("❌ Error en check_price:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/tracked/<user_id>", methods=["GET"])
def get_tracked_cards(user_id):
    tracked = db_service.get_tracked_cards_by_user_id(user_id)
    return jsonify(tracked)

if __name__ == "__main__":
    app.run(host="213.165.85.8", port=5000, debug=True)

