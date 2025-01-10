const express = require('express');
const { EAuthTokenPlatformType, LoginSession } = require('steam-session');
const { v4: uuidv4 } = require('uuid');

const app = express();
app.use(express.json());

let sessions = {};

app.post('/start-login', async (req, res) => {
    const session = new LoginSession(EAuthTokenPlatformType.SteamClient);
    session.loginTimeout = 120000; // 2 min

    try {
        const startResult = await session.startWithQR();

        // Generate a unique sessionID
        const sessionId = uuidv4();
        sessions[sessionId] = {
            session,
            authenticated: false,
            tokens: null, // This is where the token is stored after authentication
            qrChallengeUrl: startResult.qrChallengeUrl,
        };

        res.json({
            qrChallengeUrl: startResult.qrChallengeUrl,
            sessionID: sessionId,
        });

        session.on('remoteInteraction', () => {
            console.log(`Session ${sessionId}: QR code scanned.`);
        });

        session.on('authenticated', async () => {
            console.log(`Session ${sessionId}: Successful authentication!`);
            
            // Save token and account data
            sessions[sessionId].authenticated = true;
            sessions[sessionId].tokens = {
                steamID: session.steamID.toString(),
                accountName: session.accountName,
                accessToken: session.accessToken,
                refreshToken: session.refreshToken,
            };
        });

        session.on('timeout', async () => {
            console.log(`Session ${sessionId}: timeout.`);
            session.removeAllListeners();
            delete sessions[sessionId];
        });

        session.on('error', (err) => {
            console.error(`Session ${sessionId}: Error - ${err.message}`);
            delete sessions[sessionId];
        });
    } catch (err) {
        console.error('Login initialization error:', err.message);
        res.status(500).json({ error: err.message });
    }
});

app.get('/session-status/:sessionID', (req, res) => {
    const { sessionID } = req.params;
    const sessionData = sessions[sessionID];

    if (!sessionData) {
        return res.status(404).json({ error: 'Session not found or expired.' });
    }

    res.json({
        authenticated: sessionData.authenticated,
        tokens: sessionData.tokens, // Return tokens if the session is authenticated
    });
});


app.get("/update-session/:refreshToken", async (req, res) => {
    const { refreshToken } = req.params;

    if (!refreshToken) {
        return res.status(404).json({ error: "Refresh token is not specified." });
    }

    try {
        let session = new LoginSession(EAuthTokenPlatformType.SteamClient);
        session.refreshToken = refreshToken;
        await session.refreshAccessToken();

        res.json({
            accessToken: session.accessToken
        });
    }
    catch (err) {
        res.status(500).json({ error: err.message });
    }
});


app.post("/create-cookies", async (req, res) => {
    const { sessionID } = req.body; // get sessionID from the request body

    if (!sessionID || !sessions[sessionID]) {
        return res.status(404).json({ error: "Session not found or expired." });
    }

    const sessionData = sessions[sessionID];

    if (!sessionData.authenticated) {
        return res.status(403).json({ error: "Session not authorized." });
    }

    try {
        const cookies = await sessionData.session.getWebCookies();
        res.json({ cookies });
    } catch (err) {
        console.error("Error creating session cookies ${sessionID: ${err.message");
        res.status(500).json({ error: err.message });
    }
});


app.listen(3000, () => {
    console.log('API server running on http://localhost:3000');
});
