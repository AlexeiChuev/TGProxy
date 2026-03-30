import subprocess
import hashlib
import json
import os

# Эту строку GitHub автоматически заменит на твой секретный пароль при сборке
SECRET_SALT = "REPLACE_ME_SECRET_SALT"
CONFIG_FILE = "license.json"

def get_hwid():
    """Получает серийный номер системного диска Windows"""
    try:
        cmd = 'wmic diskdrive get serialnumber'
        result = subprocess.check_output(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW).decode().split()
        return result[1] if len(result) > 1 else "UNKNOWN_HWID"
    except Exception:
        return "FALLBACK_HWID"

def generate_key(hwid):
    """Генерирует уникальный ключ"""
    return hashlib.sha256((hwid + SECRET_SALT).encode()).hexdigest()[:12]

def is_activated():
    """Проверяет, есть ли правильный ключ в конфиге"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                data = json.load(f)
                return data.get("key") == generate_key(get_hwid())
            except json.JSONDecodeError:
                return False
    return False

def save_key(key):
    """Сохраняет валидный ключ"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"key": key}, f)
