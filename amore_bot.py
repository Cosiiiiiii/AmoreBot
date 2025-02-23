import os
import random
import asyncio
import datetime
import pytz
import threading
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Leggi le variabili d'ambiente
TOKEN = os.environ.get("TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))

# Fuso orario italiano
TZ_ROME = pytz.timezone("Europe/Rome")

# Messaggi da inviare
MESSAGGI_BUONGIORNO = [
    "Buongiorno amore❤❤🥰",
    "Buongiorno Nico❤❤🥰🥰",
    "Buongiorno🥰❤🥰❤🥰❤",
]

MESSAGGI_BUONANOTTE = [
    "Buonanotte amore❤❤❤😘",
    "Buonanottee❤❤❤❤🥰🥰",
    "Buonanotte sogni d'oro❤❤🥰😘✨",
    "Buonanotte Nico❤❤🥰"
]

MESSAGGI_POMERIGGIO = [
    "Amore come va?❤",
    "Ciao amore, quando ci vediamo??❤",
    "Ti amo❤❤",
    "Se ti va di parlare un po' ci sono❤❤❤"
]

# Comando /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Puzzi❤❤")

# Risposta a qualsiasi messaggio
async def risposta_puzzi(update: Update, context: CallbackContext):
    await update.message.reply_text("Puzzi❤❤")

# Funzione per inviare un messaggio casuale a una chat specifica
async def invia_messaggio_casuale(messaggi):
    bot = Bot(TOKEN)
    messaggio = random.choice(messaggi)
    await bot.send_message(chat_id=CHAT_ID, text=messaggio)

# Scheduler: controlla l'orario ogni 60 secondi e invia i messaggi previsti
async def scheduler():
    while True:
        now = datetime.datetime.now(TZ_ROME).time()
        if now.hour == 8 and now.minute == 0:
            await invia_messaggio_casuale(MESSAGGI_BUONGIORNO)
        elif now.hour == 16 and now.minute == 0:
            await invia_messaggio_casuale(MESSAGGI_POMERIGGIO)
        elif now.hour == 0 and now.minute == 0:
            await invia_messaggio_casuale(MESSAGGI_BUONANOTTE)
        await asyncio.sleep(60)

# Funzione per far girare lo scheduler in un thread separato
def start_scheduler():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(scheduler())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, risposta_puzzi))

    print("Bot avviato! 🚀")
    
    # Avvia lo scheduler in un thread separato
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Avvia il polling per ricevere gli aggiornamenti
    app.run_polling()

if __name__ == "__main__":
    main()

