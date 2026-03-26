# 🤖 Discord Channel Keeper Bot

Bot minimalista que se conecta a un canal de voz y **nunca se va**.
Ideal para mantener un canal marcado como "activo".

---

## ⚙️ Configuración paso a paso

### 1. Crear el bot en Discord

1. Ve a https://discord.com/developers/applications
2. Clic en **"New Application"** → ponle un nombre
3. Ve a la sección **"Bot"** → clic en **"Add Bot"**
4. En la misma sección, copia el **Token** (lo necesitarás luego)
5. Activa el permiso **"Server Members Intent"** y **"Voice States"**

### 2. Invitar el bot a tu servidor

En la sección **OAuth2 > URL Generator**, selecciona:
- Scope: `bot`
- Permisos: `Connect`, `Speak`

Copia la URL generada y ábrela para invitar el bot.

### 3. Obtener el ID del canal de voz

1. En Discord, activa el **Modo Desarrollador**
   (Configuración → Avanzado → Modo Desarrollador)
2. Clic derecho sobre el canal de voz → **"Copiar ID"**

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar las variables de entorno

```bash
cp .env.example .env
```

Edita `.env` y rellena:
```
DISCORD_TOKEN=tu_token_aqui
VOICE_CHANNEL_ID=id_del_canal_de_voz
```

### 6. Ejecutar el bot

```bash
python bot.py
```

---

## 🔁 Comportamiento del bot

| Situación | Respuesta del bot |
|---|---|
| Bot iniciado | Se une al canal automáticamente |
| Cada 30 segundos | Verifica que sigue conectado |
| Bot desconectado | Se reconecta automáticamente |
| Bot expulsado del canal | Espera 3 seg y vuelve a entrar |

---

## ☁️ Ejecutar 24/7 (opcional)

Para que el bot esté siempre activo puedes usar:
- **Railway** → https://railway.app (gratis)
- **Fly.io** → https://fly.io
- Un VPS con `screen` o `pm2`:

```bash
# Con pm2
npm install -g pm2
pm2 start bot.py --interpreter python3
pm2 save
```
