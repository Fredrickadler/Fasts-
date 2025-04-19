# تنظیمات ربات تلگرام
TELEGRAM_BOT_TOKEN = "7678697695:AAGAu62W-RwXgTt7igKQWy-Yxl4NM5O9JIo"

# تنظیمات Infura (برای اتریوم)
INFURA_PROJECT_ID = "YOUR_INFURA_PROJECT_ID"  # جایگزین کنید با شناسه پروژه Infura خودتان

# تنظیمات شبکه‌ها
NETWORKS = {
    'ethereum': {
        'rpc': f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}',
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

# سایر تنظیمات
CHECK_INTERVAL = 0.03  # 30 میلی‌ثانیه
GAS_LIMIT = 21000  # حد گس برای انتقال ساده