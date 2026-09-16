from robobot import Bot
from aiohttp import web
import os
import threading

# توکن ربات شما
TOKEN = "CEGCFA0REVCEGJFCSSXVQIZWKYPFYXYFGDCKBNEZCTXOMJJYOGZMTNEJHEHFQHMB"
bot = Bot(TOKEN)

@bot.on_message()
async def auto_react(bot, event):
    # در حالت Polling، event مستقیماً خود پیامه
    if event.text and not event.is_me:
        print(f"📩 پیام جدید: {event.text}")
        try:
            await bot.react(event.chat_id, event.message_id, "👍")
            print("✅ ری‌اکشن فرستاده شد!")
        except Exception as e:
            print(f"❌ خطا: {e}")

# وب سرور ساده برای اینکه Render فکر کنه یه وب سرویس معمولیه
async def handle(request):
    return web.Response(text="Bot is running!")

def run_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    # وب سرور رو توی یه ترد جداگانه اجرا میکنیم تا Render راضی باشه
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    # ربات رو با Polling اجرا میکنیم (مثل Termux)
    print("Starting bot polling...")
    bot.run()
