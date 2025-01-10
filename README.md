# Steam QRauth

UPDATE 1.1.

- Created 2 classes for more convenient server management.
- Added method to update accessToken with refreshToken
- Added method to get all authorization data as dict for easy use
- Removed recursive authorization method
- Added a method to reissue refreshToken by refreshToken. Whether a new refresh token is released depends on the Steam backend. Regardless of the value returned, the accessToken property is always updated with a fresh access token (unless an error has occurred). Important: If the refresh token is successfully updated (e.g., the method returns true), the old refresh token will become invalid, even if it has not yet expired.


# ENG
A simple library for creating QR code for authorization in Steam in Python. When authorizing, you get the following parameters:
- SteamID
- login
- AcessToken
- RefreshToken
- Cookies

## Quick Start
First, you need to install the [node.js](https://nodejs.org/en) LTS version.
Once installed, check the versions with the following commands at the command line:

```cmd
node -v
npm -v
```

Copy the repository:

```cmd
git clone https://github.com/Aarab228/steam-QRauth
```

Perform project initialization:

```cmd
npm init -y
```

Install dependencies:

```cmd
npm install express steam-session pkg uuid
```

```Python
pip install -r requirements.txt
```

Start the client:

```python
py client.py
```

It will automatically start the server as a background process and show the QR for authorization. All data will be displayed on the screen and cookies will be stored in the cookies.json file.

If for some reason you didn't manage to authorize within 2 minutes, QR will automatically generate a new one.

---
# Build.
If you want it to be an .exe file, do as follows.

Install Pyinstaller:

```python
pip install pyinstaller
```

Open cmd inside the workspace (project folder) and run:

```cmd
pkg server.js --targets node16-win-x64 --output server.exe
```

After creating **server.exe** execute:

```python
pyinstaller --onefile --add-data “server.exe;.” client.py
```

**REMEMBER! The `server.exe` and `client.exe` file must ALWAYS be in the same place!**

Run your created `client.exe`. You can run just the .exe, or you can run it using the command line:

```cmd
client.exe
```

# A simple example of how to use it in your code

```python
# -*- coding=utf-8 -*-

from client import ServerAPIClient, ServerRunner

def main():
    runner = ServerRunner()
    server_process = runner.run_node_server()

    client = ServerAPIClient()

    try:
        auth = client.get_auth_credentials()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        runner.stop_server()
```
