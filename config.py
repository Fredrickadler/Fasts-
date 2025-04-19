# config.py - تنظیمات کامل ربات انتقال خودکار ارزهای دیجیتال

# ==================== تنظیمات اصلی ====================
TELEGRAM_BOT_TOKEN = "7678697695:AAGAu62W-RwXgTt7igKQWy-Yxl4NM5O9JIo"

# ==================== تنظیمات شبکه‌ها ====================
NETWORKS = {
    'ethereum': {
        'rpc': 'https://rpc.ankr.com/eth',  # بهترین RPC عمومی اتریوم
        'scan': 'https://etherscan.io/tx/',
        'chain_id': 1,
        'symbol': 'ETH'
    },
    'bsc': {
        'rpc': 'https://bsc-dataseed1.defibit.io/',  # جایگزین سریع برای BSC
        'scan': 'https://bscscan.com/tx/',
        'chain_id': 56,
        'symbol': 'BNB'
    },
    'polygon': {
        'rpc': 'https://polygon-rpc.com/',  # RPC رسمی پالیگان
        'scan': 'https://polygonscan.com/tx/',
        'chain_id': 137,
        'symbol': 'MATIC'
    },
    'base': {
        'rpc': 'https://mainnet.base.org',  # RPC اصلی Base
        'scan': 'https://basescan.org/tx/',
        'chain_id': 8453,
        'symbol': 'ETH'
    }
}

# ==================== تنظیمات فنی ====================
CHECK_INTERVAL = 0.03  # فاصله چک کردن تراکنش‌ها (بر حسب ثانیه - 30ms)
GAS_LIMIT = 21000      # حد استاندارد گس برای انتقال ساده
MAX_RETRIES = 3        # تعداد دفعات تلاش برای انتقال در صورت خطا
RETRY_DELAY = 5        # تاخیر بین تلاش‌های مجدد (ثانیه)

# ==================== تنظیمات امنیتی ====================
SAFE_MODE = True       # اگر True باشد، قبل از انتقال تأیید می‌گیرد
MINIMUM_TRANSFER = {   # حداقل مقدار انتقال برای هر شبکه (به اتر)
    'ethereum': 0.001,
    'bsc': 0.001,
    'polygon': 0.1,
    'base': 0.001
}

# ==================== پیام‌های قابل تنظیم ====================
MESSAGES = {
    'start': "🤖 ربات انتقال خودکار ارزهای دیجیتال فعال شد!\nلطفا کلید خصوصی کیف پول خود را ارسال کنید:",
    'invalid_key': "⚠️ کلید خصوصی نامعتبر است! باید با 0x شروع شود و 66 کاراکتر داشته باشد.",
    'ask_destination': "✅ کلید خصوصی دریافت شد.\nلطفا آدرس کیف پول مقصد را ارسال کنید:",
    'invalid_address': "⚠️ آدرس کیف پول نامعتبر است! لطفا آدرس صحیح را وارد کنید.",
    'start_monitoring': "🔄 مانیتورینگ شروع شد! هر واریزی به کیف پول‌های زیر به صورت خودکار انتقال داده می‌شود:\n"
                      "- Ethereum (ETH)\n"
                      "- Binance Smart Chain (BNB)\n"
                      "- Polygon (MATIC)\n"
                      "- Base (ETH)"
}

# ==================== RPCهای جایگزین (برای مواقع قطعی) ====================
BACKUP_RPCS = {
    'ethereum': [
        'https://cloudflare-eth.com',
        'https://eth.llamarpc.com'
    ],
    'bsc': [
        'https://bsc-dataseed.binance.org/',
        'https://bsc-dataseed1.ninicoin.io/'
    ],
    'polygon': [
        'https://polygon-bor.publicnode.com',
        'https://polygon-rpc.com'
    ],
    'base': [
        'https://base.publicnode.com',
        'https://developer-access-mainnet.base.org'
    ]
}
