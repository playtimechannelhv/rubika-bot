import os
import asyncio
from aiohttp import web, ClientSession
from robobot import Bot

TOKEN = "CEGCFA0REVCEGJFCSSXVQIZWKYPFYXYFGDCKBNEZCTXOMJJYOGZMTNEJHEHFQHMB"
BASE_URL = "https://rubika-bot-f020.onrender.com"
WEBHOOK_PATH = "/wk"
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(TOKEN)  # فقط برای متد مستند bot.react

async def register_webhook():
    url = f"https://botapi.rubika.ir/v3/{TOKEN}/updateBotEndpoints"
    payload = {"url": f"{BASE_URL}{WEBHOOK_PATH}", "type": "ReceiveUpdate"}
    async with ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            body = await resp.text()
            print(f"📡 ثبت وب‌هوک → status={resp.status} body={body}")
            return resp.status == 200

async def handle_webhook(request: web.Request):
    try:
        raw = await request.text()
        print("🔵 RAW BODY:", raw)
        data = await request.json()
    except Exception as e:
        print(f"❌ خطا در خوندن بدنه: {e}")
        return web.Response(status=400, text="bad request")

    update = data.get("update", data)
    if update.get("type") == "NewMessage":
        msg = update.get("new_message") or {}
        text = msg.get("text")
        sender_type = msg.get("sender_type")
        chat_id = update.get("chat_id")
        message_id = msg.get("message_id")

        if text and sender_type == "User":
            print(f"📩 پیام جدید: {text}")
            try:
                await bot.react(chat_id, message_id, "👍")
                print("✅ ری‌اکشن فرستاده شد!")
            except Exception as e:
                print(f"❌ خطا در فرستادن ری‌اکشن: {e}")

    return web.Response(status=200, text="ok")

async def handle_health(request: web.Request):
    return web.Response(text="Bot is running!")

async def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.router.add_get("/", handle_health)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"⏳ سرور روی پورت {PORT} بالا اومد.")

    ok = await register_webhook()
    print("✅ وب‌هوک با موفقیت ثبت شد!" if ok else "⚠️ ثبت وب‌هوک ناموفق بود.")

    print("✅ ربات آنلاین شد! منتظر پیام باش...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
