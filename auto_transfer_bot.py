from web3 import Web3
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# تنظیمات ربات تلگرام
TOKEN = "7470701266:AAEr2moa9lmKqn2pKsrRMtGrYQo93vl0SH4"
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# متغیرهای امنیتی
private_key = None
target_wallet = None
w3 = None

# WebSocket URLs برای شبکه‌های مختلف
network_urls = {
    'polygon': "wss://multi-clean-layer.matic.quiknode.pro/2b16ec02f2a4dcccd9e842e6a34025281895ab0d/",
    'ethereum': "wss://mainnet.infura.io/ws/v3/YOUR_INFURA_PROJECT_ID",
    'bsc': "wss://bsc-ws-node.nariox.org:443",
    'polygon_base': "wss://rpc-mainnet.maticvigil.com/ws"
}

# اتصال به شبکه انتخابی
def connect_to_network(network_name):
    global w3
    if network_name in network_urls:
        w3 = Web3(Web3.WebsocketProvider(network_urls[network_name]))
        if w3.isConnected():
            print(f"Connected to {network_name} network via WebSocket!")
            return True
        else:
            print(f"Failed to connect to {network_name} network.")
            return False
    else:
        print("Network not recognized.")
        return False

# فرمان شروع ربات تلگرام
def start(update, context):
    update.message.reply_text("سلام! برای شروع، لطفاً پرایوت کی خود رو وارد کن.")

# ذخیره پرایوت کی
def handle_private_key(update, context):
    global private_key
    private_key = update.message.text
    update.message.reply_text("پرایوت کی ذخیره شد. حالا لطفاً آدرس ولتی که می‌خواهید توکن‌ها به آن انتقال یابند، وارد کنید.")

# ذخیره آدرس مقصد
def handle_target_wallet(update, context):
    global target_wallet
    target_wallet = update.message.text
    update.message.reply_text(f"آدرس مقصد ذخیره شد: {target_wallet}. رصد کیف پول شما شروع می‌شود.")

    # شروع رصد کیف پول
    monitor_network()

# اضافه کردن هندلرها برای تلگرام
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
private_key_handler = MessageHandler(Filters.text & ~Filters.command, handle_private_key)
dispatcher.add_handler(private_key_handler)
target_wallet_handler = MessageHandler(Filters.text & ~Filters.command, handle_target_wallet)
dispatcher.add_handler(target_wallet_handler)

# بررسی وضعیت بلاک
def get_latest_block():
    if w3:
        block = w3.eth.get_block('latest')
        print(f"Latest block: {block['number']}")

# رصد تراکنش‌ها و وضعیت بلاک
def monitor_network():
    while True:
        get_latest_block()  # وضعیت آخرین بلاک رو چک می‌کنیم
        time.sleep(5)  # هر 5 ثانیه یکبار وضعیت رو بررسی می‌کنیم

# شروع ربات تلگرام
updater.start_polling()
updater.idle()