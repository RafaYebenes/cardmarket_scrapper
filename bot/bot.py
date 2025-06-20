from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
import re
from bot.handlers_service import handle_button_click, handle_message
from db.db_service import insert_user, check_if_user_exists
from flask import Flask
app = Flask('')
# Reemplaza con tu token
TOKEN = "7194405151:AAHdeuhVtwmokePq0sEdJQwMR7dRY8CxR3U"


# Comando de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"¡Hola, introduce la carta que quieres buscar OPXX-XXX, EBXX-XXX, PRBXX-XXX")
    user = update.effective_user
    if not check_if_user_exists(user[id]):
        insert_user(user)
        print('usuario insertado en la bbdd')



# Crea la app y añade el manejador del comando /start
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_button_click))


    print("Bot funcionando... Pulsa Ctrl+C para detenerlo.")
    app.run_polling()
    
@app.route('/')
def home():
    return "Bot activo"

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()
