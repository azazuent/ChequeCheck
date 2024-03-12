from setuptools import setup

setup(
    name="cheque_check_telegram_bot",
    version="1.0",
    py_modules=["TelegramBot", "ServerAPI"],
    entry_points={
        "console_scripts": [
            "cheque_check_telegram_bot = TelegramBot:main"
        ]
    }
)