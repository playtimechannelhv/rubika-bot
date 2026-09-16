from robobot import Bot
from aiohttp import web
import os
import threading

# توکن ربات شما
TOKEN = "CEGCFA0REVCEGJFCSSXVQIZWKYPFYXYFGDCKBNEZCTXOMJJYOGZMTNEJHEHFQHMB"
bot = Bot(TOKEN)

@bot.on_message()
async def auto_react(bot, event):
    try:
        # ۱. پیام اصلی رو از داخل پاکت در میاریم
        msg = event.new_message
        
        # ۲. چک میکنیم پیام متنی باشه و از طرف خود ربات نباشه
        # توی API روبیکا، پیام‌های کاربر sender_type = "User" دارن
        if msg and msg.text and msg.sender_type == "User":
            print(f"📩 پیام جدید: {msg.text}")
            await bot.react(event.chat_id, msg.message_id, "👍")
            print("✅ ری‌اکشن فرستاده شد!")
    except Exception as e:
        print(f"❌ خطا: {type(e).__name__}: {e}")

# وب سرور ساده برای اینکه Render فکر کنه یه وب سرویس معمولیه
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
