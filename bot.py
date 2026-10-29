import requests
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

def search_public_domain(query):
    url = "https://archive.org/advancedsearch.php"
    params = {
        "q": f"{query} AND mediatype:movies AND collection:feature_films",
        "fl[]": ["identifier", "title"],
        "rows": 5, "page": 1, "output": "json"
    }
    r = requests.get(url, params=params, timeout=15).json()
    return r['response']['docs']

async def start_command(update, context):
    await update.message.reply_text(
        "🎬 *Crezie Mv - Public Domain Films*\n\n"
        "👉 භාවිතය: /search Chaplin",
        parse_mode='Markdown')

async def search_command(update, context):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Ex: /search Chaplin")
        return
    films = search_public_domain(query)
    for film in films:
        identifier = film['identifier']
        title = film['title']
        watch_url = f"https://archive.org/details/{identifier}"
        keyboard = [[InlineKeyboardButton("▶️ බලන්න", url=watch_url)]]
        await update.message.reply_text(f"🎬 *{title}*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("search", search_command))
app.run_polling()
