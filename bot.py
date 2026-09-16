from robobot import Bot
import os
import asyncio

TOKEN = "CEGCFA0REVCEGJFCSSXVQIZWKYPFYXYFGDCKBNEZCTXOMJJYOGZMTNEJHEHFQHMB"
BASE_URL = "https://rubika-bot-f020.onrender.com"

bot = Bot(TOKEN)

@bot.on_message()
async def debug_message(bot, event):
    print("\n========== 🔥 WEBHOOK RECEIVED ==========")
    try:
        print("EVENT TYPE:", type(event).__name__)
        print("EVENT DATA:", vars(event))
        
        event_type = getattr(event, "type", None)
        msg = getattr(event, "new_message", None)
        
        print("EVENT.TYPE:", repr(event_type))
        
        if msg is None:
            print("❌ new_message = None")
            return
        
        print("MESSAGE TYPE:", type(msg).__name__)
        print("MESSAGE DATA:", vars(msg))
        
        text = getattr(msg, "text", None)
        sender_type = getattr(msg, "sender_type", None)
        message_id = getattr(msg, "message_id", None)
        chat_id = getattr(event, "chat_id", None)
        
        print("TEXT:", repr(text))
        print("SENDER_TYPE:", repr(sender_type))
        print("MESSAGE_ID:", repr(message_id))
        print("CHAT_ID:", repr(chat_id))
        
        if not message_id or not chat_id:
            print("❌ message_id یا chat_id نداریم")
            return
        
        if text:
            await bot.react(chat_id, message_id, "👍")
            print("✅ REACTION SENT")
    
    except Exception as e:
        print("❌ ERROR:", type(e).__name__, str(e))

async def main():
    port = int(os.environ.get("PORT", 8080))
    
    print("⏳ Starting RoboBot...")
    print("🌐 BASE URL:", BASE_URL)
    print("🌐 WEBHOOK URL:", BASE_URL + "/wk")
    
    await bot.start(
        webhook_url=BASE_URL,
        webhook_path="/wk",
        host="0.0.0.0",
        port=port,
    )
    
    try:
        result = await bot.update_bot_endpoints(
            url=BASE_URL + "/wk",
            endpoint_type="ReceiveUpdate",
        )
        print("✅ WEBHOOK REGISTER RESULT:", result)
    except Exception as e:
        print("❌ WEBHOOK REGISTER ERROR:", repr(e))
    
    print("✅ BOT ONLINE - منتظر پیام...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
