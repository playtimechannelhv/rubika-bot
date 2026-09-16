from robobot import Bot
import os
import asyncio

# توکن ربات
TOKEN = "CEGCFA0REVCEGJFCSSXVQIZWKYPFYXYFGDCKBNEZCTXOMJJYOGZMTNEJHEHFQHMB"
bot = Bot(TOKEN)

# آدرس عمومی رندر خودت (بدون / در انتها)
BASE_URL = "https://rubika-bot-f020.onrender.com"

@bot.on_message()
async def auto_react(bot, event):
    try:
        if event.type == "NewMessage" and event.new_message:
            msg = event.new_message
            if msg.text and msg.sender_type == "User":
                print(f"📩 پیام جدید: {msg.text}")
                await bot.react(event.chat_id, msg.message_id, "👍")
                print("✅ ری‌اکشن فرستاده شد!")
    except Exception as e:
        print(f"❌ خطا: {type(e).__name__}: {e}")

async def main():
    port = int(os.environ.get("PORT", 8080))
    
    print("⏳ در حال اتصال به روبیکا...")
    
    # استارت سرور وب‌هوک (خودش پورت رو باز می‌کنه)
    await bot.start(
        webhook_url=BASE_URL,
        webhook_path="/wk",
        host="0.0.0.0",
        port=port,
    )
    
    # ثبت آدرس وب‌هوک نزد روبیکا
    try:
        await bot.update_bot_endpoints(
            url=f"{BASE_URL}/wk",
            endpoint_type="ReceiveUpdate",
        )
        print("✅ وب‌هوک با موفقیت ثبت شد!")
    except Exception as e:
        print(f"⚠️ خطا در ثبت وب‌هوک: {e}")
    
    print("✅ ربات آنلاین شد! منتظر پیام باش...")
    
    # این خط باعث میشه برنامه همیشه زنده بمونه
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
