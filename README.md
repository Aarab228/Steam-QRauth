# Steam QRauth

- [RU](#RU)
- [ENG](#ENG)



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


---
---
---
---


# RU
Простенькая библиотека создания QR кода для авторизации в Steam на Python. При авторизации вы получаете следующие параметры:
- SteamID
- login
- AcessToken
- RefreshToken
- Cookies

## Быстрый старт
Для начала вам необходимо установить [node.js](https://nodejs.org/en) LTS-версию.
После установки проверьте версии следующими командами в командной строке:

```cmd
node -v
npm -v
```

Скопируйте репозиторий:

```cmd
git clone https://github.com/Aarab228/steam-QRauth
```

Выполните инициализацию проекта:

```cmd
npm init -y
```

Установите зависимости:

```cmd
npm install express steam-session pkg uuid
```

```Python
pip install -r requirements.txt
```

Запустите клиент:

```python
py client.py
```

Он автоматически запустит сервер фоновым процессом и покажет QR для авторизации. Все данные будут отображены на экране, а куки файлы будут сохранены в файл cookies.json.

Если вы по какой-то причине не успели авторизоваться в течение 2х минут, QR автоматически сгенерируется новый.

---
# Сборка.
Если вы хотите чтобы это был .exe файл, делайте следующим образом.

Установите Pyinstaller:

```python
pip install pyinstaller
```

Откройте cmd внутри рабочей области (папки проекта) и выполните:

```cmd
pkg server.js --targets node16-win-x64 --output server.exe
```

После создания **server.exe** выполните:

```python
pyinstaller --onefile --add-data "server.exe;." client.py
```

**ПОМНИТЕ! Файл `server.exe` и `client.exe` должны ВСЕГДА находится ВМЕСТЕ!**

Запустите ваш созданный `client.exe`. Вы можете запустить просто .exe, либо с помощью командной строки:

```cmd
client.exe
```
