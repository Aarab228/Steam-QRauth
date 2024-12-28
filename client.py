import requests
import time
from qrcode import QRCode
import json
import subprocess
import sys
import os

API_URL = "http://localhost:3000"
TIMEOUT = 120

def run_node_server():
    """ Запуск Node.js сервера. """
    try:
        if sys.platform == 'win32' and os.path.exists('server.exe'):
            process = subprocess.Popen(["server.exe"])
            return process
        else:
            subprocess.run(["node", "server.js"], check=True)
    except subprocess.CalledProcessError as e:
        print("Ошибка при запуске сервера:", e)
        sys.exit(1)

def generate_qr_code(data):
    """ Генерация QR-кода. """
    qr = QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    qr.print_ascii()

def start_login_session():
    """ Инициализация сессии логина через Node.js API. """
    response = requests.post(f"{API_URL}/start-login")
    
    if response.status_code != 200:
        print("Ошибка при инициализации логина:", response.text)
        return None, None

    data = response.json()
    #print("Ответ сервера:", data)  # Отладочная информация
    if 'qrChallengeUrl' not in data or 'sessionID' not in data:
        print("Ошибка: Некорректный ответ сервера:", data)
        return None, None

    #print("Ссылка для QR-кода:", data['qrChallengeUrl'])
    generate_qr_code(data['qrChallengeUrl'])
    return data['qrChallengeUrl'], data['sessionID']

def check_session_status(session_id):
    """ Проверка статуса сессии. """
    response = requests.get(f"{API_URL}/session-status/{session_id}")
    
    if response.status_code == 404:
        print("Сессия не найдена или истекла.")
        return None, None

    data = response.json()
    return data.get('authenticated', False), data.get('tokens', None)

def convert_cookies_to_dict(cookies):
    """ Преобразует список строк cookies в словарь (key-value). """
    cookie_dict = {}
    
    for cookie in cookies:
        parts = cookie.split('=', 1)
        if len(parts) == 2:
            key, value = parts
            cookie_dict[key] = value
    
    return cookie_dict

def create_cookies(session_id):
    """ Создает cookie файл авторизованной сессии """
    response = requests.post(f"{API_URL}/create-cookies", json={"sessionID": session_id})
    
    if response.status_code != 200:
        print("Ошибка при создании cookies:", response.text)
        return None
    
    data = response.json()
    cookies = data.get("cookies")
    
    if not cookies:
        print("Ошибка: Некорректный ответ сервера:", data)
        return None
    
    cookie_dict = convert_cookies_to_dict(cookies)
    
    with open("cookies.json", "w") as file:
        json.dump(cookie_dict, file, indent=4)

    return cookie_dict

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    qr_url, session_id = start_login_session()
    if not session_id:
        print("Не удалось инициализировать сессию.")
        return

    print("Ожидание завершения аутентификации...")
    for _ in range(TIMEOUT // 5):
        time.sleep(5)
        authenticated, tokens = check_session_status(session_id)
        if authenticated:
            print("Успешная аутентификация!")
            print("\nДанные сессии:")
            print(f"SteamID: {tokens['steamID']}")
            print(f"Account name: {tokens['accountName']}")
            print(f"Access token: {tokens['accessToken']}")
            print(f"Refresh token: {tokens['refreshToken']}")
            print(f"Cookies: {create_cookies(session_id)}")
            return

    clear_console()
    main()

if __name__ == "__main__":
    print("Запуск сервера...")
    run_node_server()
    main()
