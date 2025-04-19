import asyncio
import logging
from web3 import Web3
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیمات لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# شبکه‌های پشتیبانی شده
NETWORKS = {
    'ethereum': {
        'rpc': 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID',
        'scan': 'https://etherscan.io/tx/',
        'chain_id': 1
    },
    'bsc': {
        'rpc': 'https://bsc-dataseed.binance.org/',
        'scan': 'https://bscscan.com/tx/',
        'chain_id': 56
    },
    'polygon': {
        'rpc': 'https://polygon-rpc.com/',
        'scan': 'https://polygonscan.com/tx/',
        'chain_id': 137
    },
    'base': {
        'rpc': 'https://mainnet.base.org',
        'scan': 'https://basescan.org/tx/',
        'chain_id': 8453
    }
}

# وضعیت کاربران
user_data = {}

class WalletMonitor:
    def __init__(self, private_key, destination_wallet, networks_to_monitor):
        self.private_key = private_key
        self.destination_wallet = destination_wallet
        self.networks = networks_to_monitor
        self.web3_instances = {}
        
        for net in self.networks:
            self.web3_instances[net] = Web3(Web3.HTTPProvider(NETWORKS[net]['rpc']))
    
    async def monitor_wallets(self):
        while True:
            for net in self.networks:
                try:
                    w3 = self.web3_instances[net]
                    account = w3.eth.account.from_key(self.private_key)
                    balance = w3.eth.get_balance(account.address)
                    
                    if balance > 0:
                        logger.info(f"Found balance on {net}: {w3.from_wei(balance, 'ether')} ETH")
                        await self.transfer_funds(net, balance)
                except Exception as e:
                    logger.error(f"Error monitoring {net}: {e}")
            
            await asyncio.sleep(30 / 1000)  # 30 میلی‌ثانیه
    
    async def transfer_funds(self, network, amount):
        try:
            w3 = self.web3_instances[network]
            account = w3.eth.account.from_key(self.private_key)
            
            # محاسبه کارمزد شبکه
            gas_price = w3.eth.gas_price
            gas_limit = 21000  # حد استاندارد برای انتقال ETH
            fee = gas_price * gas_limit
            
            if amount <= fee:
                logger.warning(f"Insufficient balance on {network} to cover fees")
                return
            
            transfer_amount = amount - fee
            
            # ساخت تراکنش
            tx = {
                'to': self.destination_wallet,
                'value': transfer_amount,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': w3.eth.get_transaction_count(account.address),
                'chainId': NETWORKS[network]['chain_id']
            }
            
            # امضای تراکنش
            signed_tx = w3.eth.account.sign_transaction(tx, self.private_key)
            
            # ارسال تراکنش
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_url = f"{NETWORKS[network]['scan']}{tx_hash.hex()}"
            
            logger.info(f"Transferred {w3.from_wei(transfer_amount, 'ether')} ETH from {network} to {self.destination_wallet}")
            logger.info(f"Transaction: {tx_url}")
            
            return tx_url
        except Exception as e:
            logger.error(f"Error transferring funds on {network}: {e}")
            raise

# دستورات ربات تلگرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! ربات انتقال خودکار توکن‌ها خوش آمدید.\n"
        "لطفا کلید خصوصی ولت خود را ارسال کنید (این اطلاعات ذخیره نمی‌شوند):"
    )

async def handle_private_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    private_key = update.message.text.strip()
    
    # اعتبارسنجی اولیه کلید خصوصی
    if not private_key.startswith('0x') or len(private_key) != 66:
        await update.message.reply_text("کلید خصوصی نامعتبر است. لطفا دوباره ارسال کنید.")
        return
    
    user_data[user_id] = {'private_key': private_key}
    await update.message.reply_text(
        "کلید خصوصی دریافت شد.\n"
        "لطفا آدرس ولت مقصد را ارسال کنید:"
    )

async def handle_destination_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    destination_wallet = update.message.text.strip()
    
    # اعتبارسنجی آدرس ولت
    if not Web3.is_address(destination_wallet):
        await update.message.reply_text("آدرس ولت نامعتبر است. لطفا دوباره ارسال کنید.")
        return
    
    if user_id not in user_data or 'private_key' not in user_data[user_id]:
        await update.message.reply_text("لطفا ابتدا کلید خصوصی خود را ارسال کنید.")
        return
    
    user_data[user_id]['destination_wallet'] = destination_wallet
    
    # شروع مانیتورینگ
    networks_to_monitor = ['ethereum', 'bsc', 'polygon', 'base']
    monitor = WalletMonitor(
        private_key=user_data[user_id]['private_key'],
        destination_wallet=destination_wallet,
        networks_to_monitor=networks_to_monitor
    )
    
    # حذف کلید خصوصی از حافظه پس از استفاده
    del user_data[user_id]['private_key']
    
    asyncio.create_task(monitor.monitor_wallets())
    await update.message.reply_text(
        "مانیتورینگ ولت‌ها شروع شد!\n"
        "هر گونه واریزی به ولت‌های زیر به صورت خودکار به ولت مقصد منتقل خواهد شد:\n"
        "- Ethereum\n"
        "- Binance Smart Chain\n"
        "- Polygon\n"
        "- Base"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    if update.message:
        await update.message.reply_text("خطایی رخ داده است. لطفا دوباره تلاش کنید.")

def main():
    # تنظیمات ربات تلگرام
    application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    
    # ثبت هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # شروع ربات
    application.run_polling()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_id in user_data:
        if 'private_key' in user_data[user_id] and 'destination_wallet' not in user_data[user_id]:
            await handle_destination_wallet(update, context)
        else:
            await update.message.reply_text("ربات در حال مانیتورینگ است. برای شروع جدید از /start استفاده کنید.")
    else:
        await handle_private_key(update, context)

if __name__ == '__main__':
    main()
