import os

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY", "yakovyshyn-secret-key-lab4-2026")
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
