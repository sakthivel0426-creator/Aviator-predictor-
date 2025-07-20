import os
from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
app = FastAPI()

application = Application.builder().token(BOT_TOKEN).build()

def analyze_trend(data):
    try:
        numbers = [float(x) for x in data.split()]
        low = len([x for x in numbers if x < 2])
        high = len([x for x in numbers if x >= 10])

        if high >= 2:
            return "🔴 Signal: WAIT\nToo many recent high crashes."
        elif low >= 6:
            return "🔵 Signal: SAFE BET\nTry auto cashout at 1.5x–2x."
        elif low >= 4 and high == 0:
            return "🟠 Signal: RISK BET\nTry for a 10x+ once."
        else:
            return "⚪ Signal: NO CLEAR TREND\nObserve a few more rounds."
    except:
        return "⚠️ Invalid input. Send 10 space-separated numbers."

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = analyze_trend(update.message.text)
    await update.message.reply_text(result)

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze))

@app.post("/")
async def telegram_webhook(req: Request):
    body = await req.json()
    update = Update.de_json(body, bot)
    await application.process_update(update)
    return {"ok": True}
