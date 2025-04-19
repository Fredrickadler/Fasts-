import os
from dotenv import load_dotenv
from web3 import Web3
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio

# Load environment variables
load_dotenv()

# Configuration
TOKEN = os.getenv('7470701266:AAEr2moa9lmKqn2pKsrRMtGrYQo93vl0SH4')
NETWORK_URL = os.getenv('wss://multi-clean-layer.matic.quiknode.pro/2b16ec02f2a4dcccd9e842e6a34025281895ab0d/')

# Global variables
private_key = None
target_wallet = None
w3 = None

async def start(update, context):
    await update.message.reply_text("سلام! برای شروع، لطفاً پرایوت کی خود رو وارد کن.")

async def handle_private_key(update, context):
    global private_key
    private_key = update.message.text
    await update.message.reply_text("پرایوت کی ذخیره شد. حالا لطفاً آدرس ولتی که می‌خواهید توکن‌ها به آن انتقال یابند، وارد کنید.")

async def handle_target_wallet(update, context):
    global target_wallet
    target_wallet = update.message.text
    await update.message.reply_text(f"آدرس مقصد ذخیره شد: {target_wallet}. رصد کیف پول شما شروع می‌شود.")
    asyncio.create_task(monitor_network())

async def get_latest_block():
    if w3:
        block = w3.eth.get_block('latest')
        print(f"Latest block: {block['number']}")

async def monitor_network():
    while True:
        await get_latest_block()
        await asyncio.sleep(5)

def main():
    # Connect to network
    global w3
    w3 = Web3(Web3.WebsocketProvider(NETWORK_URL))
    
    if not w3.isConnected():
        print("Failed to connect to network")
        return

    # Create Telegram application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_private_key))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_target_wallet))

    # Start polling
    application.run_polling()

if __name__ == "__main__":
    main()