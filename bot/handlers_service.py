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
    await register_card(card, user_id, modo)

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

    inserted_card = insert_card(card_bbdd)
    print(f'inserted card: {inserted_card}')
    if inserted_card is not None:
        tracked_card = {
            'user_id': user_id,
            'card_id': card_bbdd['id'],
            'country': card['country'],
            'condition': card['condition'],
            'quantity': card['quantity'],
            'last_price': card['price'],
            'last_check': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    return ""

async def process_selected_card(query, card_ms, context):
    print(f"card: {card_ms}")
    await query.edit_message_caption("Comprobando carta")

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

    keyboard = [seguimiento_buttons, cantidad_buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_photo(
        photo=card["image"],
        caption=message_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card_code = update.message.text.strip().upper()

    if re.match(VALID_CODE_REGEX, card_code):
        await update.message.reply_text(f"✅ Código válido recibido: {card_code} \nBuscando resultados...")
        html = await scrapp_url(SEARCH_QUERY + card_code)
        matches = await parse_cardmarket_results(html)
        for idx, item in enumerate(matches):
            # Crea el botón con callback_data = índice del resultado
            button = InlineKeyboardMarkup([
                [InlineKeyboardButton("Ver más detalles", callback_data=f"card_{idx}")]
            ])

            await update.message.reply_photo(
                photo=item["image"],
                caption=item["text"],
                reply_markup=button
            )

        # Guarda los resultados en el contexto para uso posterior
        context.user_data["card_results"] = matches
    else:
        await update.message.reply_text("❌ Formato inválido. Usa uno de estos formatos:\n- OP01-142\n- EB02-555\n- PRB07-123")

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

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
            await process_selected_card(query, selected, context)
        else:
            await query.edit_message_text("❌ Resultado no encontrado.")

    elif data.startswith("qty_"):
        cantidad = int(data.split("_")[1])
        await query.edit_message_caption(caption=f"🔄 Cantidad modificada a {cantidad}")

    elif data.startswith("track_"):
        await handle_register_card(context, data, query)
