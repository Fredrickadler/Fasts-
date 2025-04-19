import os
import logging
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from web3 import Web3
from fastapi import FastAPI
import uvicorn

# تنظیمات پیشرفته لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

# بارگذاری محیط
from dotenv import load_dotenv
load_dotenv()

class Web3Bot:
    def __init__(self):
        self.app = None
        self.w3 = None

    async def connect_web3(self):
        """اتصال به شبکه Polygon"""
        try:
            self.w3 = Web3(Web3.WebsocketProvider(
                os.getenv('wss://multi-clean-layer.matic.quiknode.pro/2b16ec02f2a4dcccd9e842e6a34025281895ab0d/'),
                websocket_kwargs={
                    'timeout': 30,
                    'ping_interval': 10,
                    'ping_timeout': 5
                }
            ))
            if not self.w3.is_connected():
                logger.error("❌ اتصال به شبکه Polygon ناموفق")
                return False
            
            logger.info(f"✅ Connected to Polygon. Chain ID: {self.w3.eth.chain_id}")
            return True
            
        except Exception as e:
            logger.error(f"Web3 Connection Error: {str(e)}")
            return False

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور /start"""
        user = update.effective_user
        logger.info(f"User {user.id} started conversation")
        await update.message.reply_html(
            f"👋 سلام <b>{user.first_name}</b>!\n"
            "لطفاً کلید خصوصی خود را ارسال کنید:"
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش پیام‌های کاربر"""
        user_id = update.effective_user.id
        text = update.message.text
        
        if 'private_key' not in context.user_data:
            context.user_data['private_key'] = text
            logger.info(f"User {user_id} submitted private key")
            await update.message.reply_text("🔑 کلید خصوصی دریافت شد. حالا آدرس مقصد را ارسال کنید:")
        else:
            context.user_data['target_wallet'] = text
            logger.info(f"User {user_id} submitted target wallet: {text}")
            await update.message.reply_text(
                f"✅ تنظیمات کامل شد!\n"
                f"آدرس مقصد: <code>{text}</code>\n"
                f"ربات آماده دریافت دستورات است.",
                parse_mode='HTML'
            )

    def run_bot(self):
        """اجرای ربات تلگرام"""
        try:
            self.app = Application.builder().token(os.getenv('7678697695:AAGAu62W-RwXgTt7igKQWy-Yxl4NM5O9JIo')).build()
            
            # ثبت handlerها
            self.app.add_handler(CommandHandler("start", self.start))
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            logger.info("🤖 Telegram Bot is running...")
            self.app.run_polling()
        except Exception as e:
            logger.critical(f"Bot failed: {str(e)}")

def run_fastapi():
    """سرور HTTP برای Render"""
    app = FastAPI()
    
    @app.get("/")
    async def health_check():
        return {"status": "OK", "service": "Web3 Telegram Bot"}
    
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 8000)))

if __name__ == "__main__":
    # ایجاد نمونه ربات
    bot = Web3Bot()
    
    # تست اتصال به شبکه
    if not bot.connect_web3():
        logger.error("Failed to connect to blockchain. Exiting...")
        exit(1)
    
    # اجرای ربات در ترد جداگانه
    bot_thread = Thread(target=bot.run_bot, daemon=True)
    bot_thread.start()
    
    # اجرای سرور HTTP
    run_fastapi()