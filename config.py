# config.py

# تنظیمات ربات تلگرام
TELEGRAM_BOT_TOKEN = "توکن_ربات_تلگرام_شما"

# تنظیمات Infura (برای اتریوم)
INFURA_PROJECT_ID = "شناسه_پروژه_Infura_شما"

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
