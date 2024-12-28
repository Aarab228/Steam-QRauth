# Steam QRauth
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