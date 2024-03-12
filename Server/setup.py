from setuptools import setup

setup(
    name="cheque_check_server",
    version="1.0",
    py_modules=["Server", "DatabaseAPI", "ChequeAPI"],
    entry_points={
        "console_scripts": [
            "cheque_check_server = Server:main"
        ]
    }
)