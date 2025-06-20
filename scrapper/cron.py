##Cron Services para monitorizar el precio de las cartas
import db.db_service as db 
import scrapper.basic as scrapper
import asyncio
from datetime import datetime
import requests


TOKEN = "7194405151:AAHdeuhVtwmokePq0sEdJQwMR7dRY8CxR3U"

##Metodo 1 comprobación de las cartas en seguimiento que tenemos
def get_cards(user_id):
    print('obteniendo cartas')
    cards = db.get_tracked_cards_by_user_id(user_id)
    print(f"Cartas encontradas: {cards}")
    if len(cards) > 0:
        return cards
    else:
        print(f"⚠️ No se han obtenido cartas para user: {user_id}")
        return []


##Metodo 2 llamada a card market y obtención del precio mas bajo acutal integrar modulos de basic.py para esto
async def check_cardmarket(card_id):
    try:
        print("llamando a mkm")
        card = db.get_card_by_id(card_id)
        print(f"card check_cardmarket: {card}")
        
        if card:
            lower_price =  await scrapper.get_lower_price(card)
            return lower_price
    except Exception as e:
        print("❌ Fallo durante el cron, error: {e}.")




##Metodo 3 si el precio ha fluctuado o llegado al limite establecido mandamos notificación a telegram 
def check_prices(cards, new_prices, user_id):
    cambios = []

    for actual in cards:
        for tracked in new_prices:
            if actual["card_id"] == tracked["id"]:
                if actual["last_price"] != tracked["price"]:
                    update_price(actual, tracked["price"], user_id)
                    if actual["last_price"] > tracked["price"]:
                        send_notification(tracked, user_id, "Ha subido")
                    else:
                        send_notification(tracked, user_id, "Ha bajado")

                        
    
    return cambios

def send_notification(card, user_id, message):
    
        message_text = (
        f"🃏 {card['name']}\n"
        f"🌍 País: {card.get('country', '¿?')}  🧾 Estado: {card.get('condition', '¿?')}\n"
        f"💰 Precio: {card.get('price', '?')} € 📦 Disponibles: {card.get('quantity', '?')}\n"
        f"🔗 {message} \n"
        f"\n🔗 {card['url']}\n"
        )
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": user_id,
            "text": message_text
        }

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            print("✅ Mensaje enviado con éxito.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error al enviar mensaje: {e}")
        return None

def update_price(card, new_price, user_id):
    card["last_price"] = new_price
    card['last_check'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.update_tracked_card(card, user_id)

##Metodo 4 flujo que incluya todo lo anterior
async def main():
    try:
        users =  db.get_all_users()
        print(f"users: {users}")
        
        for user in users:
            print(f"user: {user}")
            
            user_id = user['id']
            print(f"user_id: {user_id}")
            cards = get_cards(user_id)
            new_prices = []
            if len(cards) > 0:
                for card in cards:
                    print(f'card to analize:\n{card}')
                    new = await check_cardmarket(card['card_id'])
                    print(f"new price: {new}")
                    new_prices.append(new)
                print(f"new prices: {new_prices}")
                check_prices(cards, new_prices, user_id)
    except ValueError:
        print("❌ Entrada inválida. Introduce un número.")


if __name__ == "__main__":
    asyncio.run(main())

