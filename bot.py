from robobot import Bot
from aiohttp import web
import os
import asyncio

# توکن ربات شما
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

# وب سرور برای اینکه Render فکر کنه یه سرویس فعاله
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"✅ Web server started on port {port}")

async def main():
    # اجرای همزمان وب سرور و ربات توی یه ترد اصلی
    await asyncio.gather(
        start_web_server(),
        bot.run()
    )

if __name__ == "__main__":
    asyncio.run(main())
