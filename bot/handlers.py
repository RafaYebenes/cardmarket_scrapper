from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.states import (
    SELECCIONAR_CARTA,
    ESTABLECER_TIPO_ALERTA,
    ESTABLECER_PRECIO,
    ESTABLECER_CANTIDAD,
    ESTABLECER_ESTADO,
)

# Simulador temporal de resultados del scraper
MOCK_CARD_RESULTS = [
    {"id": "v1", "name": "Zoro - Español - NM", "url": "https://cardmarket.com/zoro1"},
    {"id": "v2", "name": "Zoro - Inglés - EX", "url": "https://cardmarket.com/zoro2"},
    {"id": "v3", "name": "Zoro - Japonés - Mint", "url": "https://cardmarket.com/zoro3"},
]


# /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"¡Hola {user.first_name}! 👋\n"
        f"Usa /seguir <código> para seguir el precio de una carta.\n"
        f"Ejemplo: /seguir OP01-142"
    )


# /seguir OP01-142
async def seguir_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Por favor, usa el formato: /seguir OP01-142")
        return ConversationHandler.END

    code = context.args[0].upper()
    context.user_data["card_code"] = code

    # Aquí deberías hacer la búsqueda real en Cardmarket
    # Por ahora usamos cartas mock
    keyboard = [
        [InlineKeyboardButton(card["name"], callback_data=card["id"])]
        for card in MOCK_CARD_RESULTS
    ]

    await update.message.reply_text(
        f"Cartas encontradas para {code}. Elige una versión:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return SELECCIONAR_CARTA


# Paso 1: Selección de carta
async def handle_card_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    version_id = query.data
    context.user_data["version_id"] = version_id

    # Guardamos temporalmente la info
    await query.edit_message_text("¿Qué tipo de alerta quieres configurar?")
    keyboard = [
        [
            InlineKeyboardButton("🔼 Precio máximo", callback_data="max"),
            InlineKeyboardButton("🔽 Precio mínimo", callback_data="min"),
        ]
    ]
    await query.message.reply_text("Elige el tipo de alerta:", reply_markup=InlineKeyboardMarkup(keyboard))
    return ESTABLECER_TIPO_ALERTA


# Paso 2: Tipo de alerta
async def handle_alert_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    alert_type = query.data

    context.user_data["alert_type"] = alert_type

    await query.message.reply_text("Introduce el precio en euros para activar la alerta:")
    return ESTABLECER_PRECIO


# Paso 3: Precio objetivo
async def handle_price_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = float(update.message.text.replace(",", "."))
    except ValueError:
        await update.message.reply_text("❌ Precio inválido. Intenta de nuevo con un número (ej. 12.5)")
        return ESTABLECER_PRECIO

    context.user_data["target_price"] = price
    await update.message.reply_text("¿Cuál es la cantidad mínima que deseas?")
    return ESTABLECER_CANTIDAD


# Paso 4: Cantidad mínima
async def handle_quantity_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        quantity = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Cantidad inválida. Intenta con un número entero.")
        return ESTABLECER_CANTIDAD

    context.user_data["min_quantity"] = quantity

    keyboard = [
        [
            InlineKeyboardButton("Mint", callback_data="Mint"),
            InlineKeyboardButton("Near Mint", callback_data="NM"),
            InlineKeyboardButton("Excellent", callback_data="EX"),
        ]
    ]
    await update.message.reply_text("Selecciona el estado mínimo deseado:", reply_markup=InlineKeyboardMarkup(keyboard))
    return ESTABLECER_ESTADO


# Paso 5: Estado deseado
async def handle_condition_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    condition = query.data
    context.user_data["min_condition"] = condition

    # Aquí normalmente guardarías en Supabase
    summary = (
        f"✅ Has configurado un seguimiento para la carta:\n"
        f"- Código: {context.user_data['card_code']}\n"
        f"- Versión ID: {context.user_data['version_id']}\n"
        f"- Tipo de alerta: {context.user_data['alert_type']}\n"
        f"- Precio objetivo: {context.user_data['target_price']} €\n"
        f"- Cantidad mínima: {context.user_data['min_quantity']}\n"
        f"- Estado: {context.user_data['min_condition']}"
    )
    await query.message.reply_text(summary)
    return ConversationHandler.END


# /cancelar en cualquier punto
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Seguimiento cancelado ❌")
    return ConversationHandler.END
