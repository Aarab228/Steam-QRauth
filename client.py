# -*- coding=utf-8 -*-

import requests
import time
from qrcode import QRCode
import json
import subprocess
import sys
import os
import atexit
from multiprocessing import Process, Value

import time

API_URL = "http://localhost:3000"
TIMEOUT = 120
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SERVER_PID = Value('i', 0)


class ServerRunner:
    def __init__(self):
        pass

    def start_server(self):
        global SERVER_PID
        process = None
        try:
            if sys.platform == 'win32' and os.path.exists(f"{CURRENT_PATH}\\server.exe"):
                process = subprocess.Popen(["server.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen(["node", f"{CURRENT_PATH}\\server.js"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            with SERVER_PID.get_lock():
                SERVER_PID.value = process.pid
            
            print("Node.js server is up and running.")
            process.wait()
        except Exception as e:
            print(f"Server startup error: {e}")
            sys.exit(1)
        finally:
            with SERVER_PID.get_lock():
                SERVER_PID.value = 0

    def run_node_server(self):
        server_process = Process(target = self.start_server)
        server_process.start()
        
        def terminate_server():
            if server_process.is_alive():
                self.stop_server()
                
        atexit.register(terminate_server)

        with SERVER_PID.get_lock():
            SERVER_PID.value = server_process.pid

        return server_process

    def stop_server(self):
        with SERVER_PID.get_lock():
            pid = SERVER_PID.value

        if pid == 0:
            print("The server is not running.")
            return

        try:
            if sys.platform == 'win32':
                subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=True)
            else:
                os.kill(pid, 9)
            print(f"Server (PID: {pid}) is stopped.")
        except Exception as e:
            print(f"Server stop error (PID: {pid}): {e}")
        finally:
            with SERVER_PID.get_lock():
                SERVER_PID.value = 0


class ServerAPIClient:
    def __init__(self):
        if SERVER_PID.value == 0:
            return "The server is not running."

    def generate_qr_code(self, data):
        qr = QRCode()
        qr.add_data(data)
        qr.make(fit = True)
        qr.print_ascii()

    def start_login_session(self):
        """ Initializing a login session via Node.js API. """
        response = requests.post(f"{API_URL}/start-login")
        
        if response.status_code != 200:
            print("Error during login initialization:", response.text)
            return None, None

        data = response.json()
        if 'qrChallengeUrl' not in data or 'sessionID' not in data:
            print("Error: Incorrect server response:", data)
            return None, None

        self.generate_qr_code(data['qrChallengeUrl'])
        return data['qrChallengeUrl'], data['sessionID']

    def check_session_status(self, session_id):
        """ Checking the status of the session. """
        response = requests.get(f"{API_URL}/session-status/{session_id}")
        
        if response.status_code == 404:
            print("Session not found or expired.")
            return None, None

        data = response.json()
        return data.get('authenticated', False), data.get('tokens', None)
    
    def convert_cookies_to_dict(self, cookies):
        """ Converts a list of cookie strings into a dictionary (key-value). """
        cookie_dict = {}
        
        for cookie in cookies:
            parts = cookie.split('=', 1)
            if len(parts) == 2:
                key, value = parts
                cookie_dict[key] = value
        
        return cookie_dict

    def create_cookies(self, session_id):
        """ Creates a cookie of the authorized session """
        response = requests.post(f"{API_URL}/create-cookies", json={"sessionID": session_id})
        
        if response.status_code != 200:
            print("Error when creating cookies:", response.text)
            return None
        
        data = response.json()
        cookies = data.get("cookies")
        
        if not cookies:
            print("Error: Incorrect server response:", data)
            return None
        
        cookie_dict = self.convert_cookies_to_dict(cookies)
        
        with open("cookies.json", "w") as file:
            json.dump(cookie_dict, file, indent=4)

        return cookie_dict

    def update_access_token(self, refreshToken):
        response = requests.get(f"{API_URL}/update-session/{refreshToken}")

        data = response.json()
        return data.get('accessToken', None)

    def clear_console(self):
        os.system("cls" if os.name == "nt" else "clear")

    def get_auth_credentials(self) -> dict:
        qr_url, session_id = self.start_login_session()
        if not session_id:
            print("Failed to initialize the session.")
            return

        print("Waiting for authentication to complete...")
        for _ in range(TIMEOUT // 5):
            time.sleep(5)
            authenticated, tokens = self.check_session_status(session_id)
            if authenticated:
                print("Successful authentication!")
                return {
                    "steamID": tokens['steamID'],
                    "accountName": tokens['accountName'],
                    "accessToken": tokens['accessToken'],
                    "refreshToken": tokens['refreshToken']
                }
