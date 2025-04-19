import os
import logging
from threading import Thread
from dotenv import load_dotenv
from web3 import Web3
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from fastapi import FastAPI
import uvicorn

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیمات اصلی
TELEGRAM_TOKEN = os.getenv('7470701266:AAEr2moa9lmKqn2pKsrRMtGrYQo93vl0SH4')
NETWORK_URL = os.getenv('wss://multi-clean-layer.matic.quiknode.pro/2b16ec02f2a4dcccd9e842e6a34025281895ab0d/')

class TelegramBot:
    def __init__(self):
        self.w3 = None
        self.user_data = {}

    def connect_to_network(self):
        try:
            self.w3 = Web3(Web3.WebsocketProvider(
                NETWORK_URL,
                websocket_kwargs={
                    'timeout': 30,
                    'ping_interval': 60,
                    'ping_timeout': 30
                }
            ))
            if not self.w3.is_connected():
                logger.error("اتصال به شبکه ناموفق بود")
                return False
            
            logger.info(f"اتصال موفق به شبکه - آخرین بلاک: {self.w3.eth.block_number}")
            return True
            
        except Exception as e:
            logger.error(f"خطا در اتصال به شبکه: {str(e)}")
            return False

    async def start(self, update, context):
        user = update.effective_user
        logger.info(f"کاربر شروع کرد: {user.id}")
        await update.message.reply_text(f"سلام {user.first_name}!\nلطفاً کلید خصوصی خود را ارسال کنید.")

    async def handle_private_key(self, update, context):
        user_id = update.effective_user.id
        self.user_data[user_id] = {'private_key': update.message.text}
        logger.info(f"کلید خصوصی دریافت شد از کاربر: {user_id}")
        await update.message.reply_text("کلید خصوصی ذخیره شد. لطفاً آدرس مقصد را ارسال کنید.")

    async def handle_target_wallet(self, update, context):
        user_id = update.effective_user.id
        if user_id in self.user_data:
            self.user_data[user_id]['target_wallet'] = update.message.text
            logger.info(f"آدرس مقصد دریافت شد از کاربر: {user_id}")
            await update.message.reply_text(
                f"تنظیمات کامل شد!\n"
                f"آدرس مقصد: {update.message.text}\n"
                f"شما می‌توانید تراکنش‌ها را بررسی کنید."
            )
        else:
            await update.message.reply_text("لطفاً ابتدا کلید خصوصی خود را ارسال کنید.")

    def run(self):
        if not self.connect_to_network():
            return

        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_private_key))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_target_wallet))
        
        logger.info("ربات تلگرام در حال اجرا...")
        application.run_polling()

# FastAPI App برای Render
app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "active", "service": "Telegram Web3 Bot"}

def run_bot():
    bot = TelegramBot()
    bot.run()

if __name__ == "__main__":
    # اجرای ربات در یک ترد جداگانه
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    # اجرای سرور FastAPI
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))