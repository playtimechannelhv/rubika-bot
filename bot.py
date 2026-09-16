from robobot import Bot
from aiohttp import web
import os
import threading

TOKEN = "CEGCFA0REVCEGJFCSSXVQIZWKYPFYXYFGDCKBNEZCTXOMJJYOGZMTNEJHEHFQHMB"
bot = Bot(TOKEN)

@bot.on_message()
async def auto_react(bot, event):
    try:
        msg = event.new_message
        if msg and msg.text and msg.sender_type == "User":
            print(f"📩 پیام جدید: {msg.text}")
            await bot.react(event.chat_id, msg.message_id, "👍")
            print("✅ ری‌اکشن فرستاده شد!")
    except Exception as e:
        print(f"❌ خطا: {type(e).__name__}: {e}")

async def handle(request):
    return web.Response(text="Bot is running!")

def run_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    print("Starting bot polling...")
    bot.run()
