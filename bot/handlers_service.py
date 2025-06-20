from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
import re
from scrapper.basic import get_lower_price, scrapp_url, parse_cardmarket_results, parse_sellers
from db.db_service import insert_card, insert_price_history, insert_tracked_card
from datetime import datetime

VALID_CODE_REGEX = r"^(OP\d{2}-\d{3}|EB\d{2}-\d{3}|PRB\d{2}-\d{3})$"
SEARCH_QUERY = "https://www.cardmarket.com/es/OnePiece/Products/Search?searchString="

async def handle_register_card(context, data, query):
    modo = data.split("_")[1]  # 'up', 'down', 'both'
    user_id = query.from_user.id
    card = context.user_data.get("selected_card")
    print(f"card: {card}")

    if card is None:
        await query.edit_message_caption("⚠️ No se encontró la carta para seguimiento.")
        return

    # Guardar el seguimiento en Supabase o donde lo necesites
    if await register_card(card, user_id, modo):
        await query.edit_message_caption("Seguimiento de carta añadido con exito.")
    else:
        await query.edit_message_caption("⚠️ Fallo al añadir el seguimiento.")
    await query.edit_message_caption(
        caption=f"📡 Seguimiento activado: {'⬆️' if modo == 'up' else '⬇️' if modo == 'down' else '⬆️⬇️'}\n\n"
                f"🃏 {card['text']}"
    )

async def register_card(card, user_id, mode):
    
    card_bbdd = {
        "code": card['code'],
        "version":card['version'],
        "name": card["text"],
        "url": card['url'],
        "image": card['image']
    }

    card_id = insert_card(card_bbdd)
    
    if card_id:
        tracked_card = {
            'user_id': user_id,
            'card_id': card_id,
            'country': card['country'],
            'condition': card['condition'],
            'quantity': card['quantity'],
            'last_price': card['price'],
            'last_check': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'mode': mode
        }

        tc_id = insert_tracked_card(tracked_card)
        if tc_id:
            price_history = {
                    'tracked_card_id': tc_id,
                    'price': card['price'],
                    'checked_at': tracked_card['last_check']
            }

            return insert_price_history(price_history)
            


    return False

async def process_selected_card(query, card_ms, context):
    print(f"card: {card_ms}")
       
    card = await get_lower_price(card_ms)
    context.user_data["selected_card"] = card

    message_text = (
        f"🃏 <b>{card['text']}</b>\n"
        f"🌍 <b>País:</b> {card.get('country', '¿?')}\n"
        f"🧾 <b>Estado:</b> {card.get('condition', '¿?')}\n"
        f"💰 <b>Precio:</b> {card.get('price', '?')} €\n"
        f"📦 <b>Disponibles:</b> {card.get('quantity', '?')}\n"
        f"\n🔗 <a href='{card['url']}'>Ver en Cardmarket</a>\n"
        f"\n📡 <i>¿Quieres seguir la evolución del precio?</i>\n"
        f"\n✏️ <i>Modifica las cantidades a buscar:</i>"
    )

    seguimiento_buttons = [
        InlineKeyboardButton("📈↑", callback_data="track_up"),
        InlineKeyboardButton("📉↓", callback_data="track_down"),
        InlineKeyboardButton("🔁↑↓", callback_data="track_both")
    ]

    cantidad_buttons = [
        InlineKeyboardButton("Buscar 1", callback_data="qty_1"),
        InlineKeyboardButton("Buscar 2", callback_data="qty_2"),
        InlineKeyboardButton("Buscar 3", callback_data="qty_3"),
        InlineKeyboardButton("Buscar 4", callback_data="qty_4")
    ]

    restore_button =  [InlineKeyboardButton("🔙 Volver a resultados", callback_data="volver_resultados")]

    keyboard = [seguimiento_buttons, cantidad_buttons, restore_button]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_photo(
        photo=card["image"],
        caption=message_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    context.user_data["card_messages"] = []  # reset

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card_code = update.message.text.strip().upper()

    if re.match(VALID_CODE_REGEX, card_code):
        await update.message.reply_text(f"✅ Código válido recibido: {card_code} \nBuscando resultados...")
        html = await scrapp_url(SEARCH_QUERY + card_code)
        matches = await parse_cardmarket_results(html)
        await save_messages(matches, update, context)

    else:
        await update.message.reply_text("❌ Formato inválido. Usa uno de estos formatos:\n- OP01-142\n- EB02-555\n- PRB07-123")

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    data = query.data
    print(f"data : {data}")

    if data.startswith("card_"):
        idx = int(data.split("_")[1])
        results = context.user_data.get("card_results", [])
        print(f"boton pulsado: {idx}")
        print(f"results : {results}")
        #Cuando hay solo un resultado no va
        print(f"len(results) : {len(results)}")
        if 0 <= idx < len(results):
            selected = results[idx]

            # Llamada a tu función personalizada
            await hide_messages(context, chat_id)
            await process_selected_card(query, selected, context)

        else:
            await query.edit_message_text("❌ Resultado no encontrado.")

    elif data.startswith("qty_"):
        cantidad = int(data.split("_")[1])
        await query.edit_message_caption(caption=f"🔄 Cantidad modificada a {cantidad}")

    elif data.startswith("track_"):
        await handle_register_card(context, data, query)

async def save_messages(cards, update, context):
    
    context.user_data["card_messages"] = []  # reset

    for idx, card in enumerate(cards):
        message = await update.message.reply_photo(
            photo=card["image"],
            caption=card["text"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ver más detalles", callback_data=f"card_{idx}")]
            ])
        )
        context.user_data["card_messages"].append(message.message_id)
    
    context.user_data["card_results"] = cards

async def hide_messages(context, chat_id):
    for msg_id in context.user_data.get("card_messages", []):
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass  # El mensaje ya fue borrado

    # Guarda también los resultados para volver atrás si hace falta
    context.user_data["cards"] = context.user_data.get("cards", [])
    
    loading_msg = await context.bot.send_message(
        chat_id=chat_id,
        text="⏳ Comprobando carta..."
    )
   