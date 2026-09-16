from robobot import Bot
import os

TOKEN = "CEGCFA0REVCEGJFCSSXVQIZWKYPFYXYFGDCKBNEZCTXOMJJYOGZMTNEJHEHFQHMB"
bot = Bot(TOKEN)

@bot.on_message()
async def auto_react(bot, event):
    msg = event.new_message
    if msg and msg.text and not msg.is_me:
        print(f"📩 پیام جدید: {msg.text}")
        try:
            await bot.react(msg.chat_id, msg.message_id, "👍")
            print("✅ ری‌اکشن فرستاده شد!")
        except Exception as e:
            print(f"❌ خطا: {e}")

async def main():
    # Render خودش پورت رو ست میکنه، ما ازش میخونیم
    port = int(os.environ.get("PORT", 8080))
    
    # ⚠️ این آدرس رو بعد از دیپلوی روی Render باید با آدرس خودت عوض کنی
    webhook_url = "https://your-app.onrender.com" 
    
    print("⏳ در حال اتصال به روبیکا...")
    
    # ثبت آدرس وب‌هوک نزد روبیکا
    try:
        await bot.update_bot_endpoints(
            url=f"{webhook_url}/wk",
            endpoint_type="ReceiveUpdate"
        )
        print("✅ وب‌هوک با موفقیت ثبت شد!")
    except Exception as e:
        print(f"⚠️ خطا در ثبت وب‌هوک (ممکنه بعدا درست بشه): {e}")
    
    # استارت زدن سرور
    await bot.start(
        webhook_url=webhook_url,
        webhook_path="/wk",
        host="0.0.0.0",
        port=port
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
