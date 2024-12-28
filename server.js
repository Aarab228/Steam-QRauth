const express = require('express');
const { EAuthTokenPlatformType, LoginSession } = require('steam-session');
const { v4: uuidv4 } = require('uuid');

const app = express();
app.use(express.json());

let sessions = {};

app.post('/start-login', async (req, res) => {
    const session = new LoginSession(EAuthTokenPlatformType.MobileApp);
    session.loginTimeout = 120000; // 2 минуты

    try {
        const startResult = await session.startWithQR();

        // Генерируем уникальный sessionID
        const sessionId = uuidv4();
        sessions[sessionId] = {
            session,
            authenticated: false,
            tokens: null, // Здесь хранится токен после аутентификации
            qrChallengeUrl: startResult.qrChallengeUrl,
        };

        res.json({
            qrChallengeUrl: startResult.qrChallengeUrl,
            sessionID: sessionId,
        });

        session.on('remoteInteraction', () => {
            console.log(`Сессия ${sessionId}: QR-код отсканирован.`);
        });

        session.on('authenticated', async () => {
            console.log(`Сессия ${sessionId}: Успешная аутентификация!`);
            
            // Сохраняем данные токенов и аккаунта
            sessions[sessionId].authenticated = true;
            sessions[sessionId].tokens = {
                steamID: session.steamID.toString(),
                accountName: session.accountName,
                accessToken: session.accessToken,
                refreshToken: session.refreshToken,
            };
        });

        session.on('timeout', async () => {
            console.log(`Сессия ${sessionId}: Таймаут.`);
            session.removeAllListeners();
            delete sessions[sessionId];
        });

        session.on('error', (err) => {
            console.error(`Сессия ${sessionId}: Ошибка - ${err.message}`);
            delete sessions[sessionId];
        });
    } catch (err) {
        console.error('Ошибка инициализации логина:', err.message);
        res.status(500).json({ error: err.message });
    }
});

app.get('/session-status/:sessionID', (req, res) => {
    const { sessionID } = req.params;
    const sessionData = sessions[sessionID];

    if (!sessionData) {
        return res.status(404).json({ error: 'Сессия не найдена или истекла.' });
    }

    res.json({
        authenticated: sessionData.authenticated,
        tokens: sessionData.tokens, // Возвращаем токены, если сессия аутентифицирована
    });
});


app.post("/create-cookies", async (req, res) => {
    const { sessionID } = req.body; // получаем sessionID из тела запроса

    if (!sessionID || !sessions[sessionID]) {
        return res.status(404).json({ error: "Сессия не найдена или истекла" });
    }

    const sessionData = sessions[sessionID];

    if (!sessionData.authenticated) {
        return res.status(403).json({ error: "Сессия не авторизована" });
    }

    try {
        const cookies = await sessionData.session.getWebCookies();
        res.json({ cookies });
    } catch (err) {
        console.error("Ошибка создания cookies для сессии ${sessionID: ${err.message");
        res.status(500).json({ error: err.message });
    }
});


app.listen(3000, () => {
    console.log('API server running on http://localhost:3000');
});
