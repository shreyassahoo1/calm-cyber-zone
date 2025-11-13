# Discord Bot Setup Guide

Complete guide to set up and run the SafeGuard Discord Bot with multilingual support.

## Quick Start

### 1. Prerequisites

- Python 3.9+
- Discord Bot Token
- ML Service running (see `ml-service/README.md`)
- Supabase account (optional but recommended)

### 2. Install Dependencies

```bash
cd discord-bot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```bash
cp env.example .env
```

Edit `.env` file with your credentials:

```env
DISCORD_TOKEN=your-discord-bot-token-here
ML_SERVICE_URL=http://localhost:8000
SUPABASE_URL=your-supabase-url-here
SUPABASE_KEY=your-supabase-key-here
BOT_PREFIX=!
ALERT_CHANNEL_ID=your-alert-channel-id-here
DELETE_MESSAGES=true
WARN_USERS=true
MIN_SEVERITY_TO_SAVE=medium
MIN_SEVERITY_TO_DELETE=critical
```

### 4. Get Discord Bot Token

1. Go to https://discord.com/developers/applications
2. Create a new application
3. Go to "Bot" section
4. Click "Add Bot"
5. Copy the bot token
6. Enable "Message Content Intent" under "Privileged Gateway Intents"

### 5. Invite Bot to Server

1. Go to "OAuth2" > "URL Generator"
2. Select scopes: `bot`, `applications.commands`
3. Select bot permissions:
   - Read Messages
   - Send Messages
   - Delete Messages
   - Embed Links
   - Read Message History
4. Copy the generated URL
5. Open the URL in your browser
6. Select your server and authorize

### 6. Start ML Service

```bash
cd ml-service
python main.py
```

### 7. Start Discord Bot

```bash
cd discord-bot
python bot.py
```

## Configuration

### Environment Variables

#### Required

- **DISCORD_TOKEN** - Your Discord bot token

#### Optional

- **ML_SERVICE_URL** - ML service URL (default: http://localhost:8000)
- **SUPABASE_URL** - Supabase URL for database
- **SUPABASE_KEY** - Supabase API key
- **BOT_PREFIX** - Bot command prefix (default: !)
- **ALERT_CHANNEL_ID** - Channel ID for moderator alerts
- **DELETE_MESSAGES** - Enable/disable message deletion (default: true)
- **WARN_USERS** - Enable/disable user warnings (default: true)
- **MIN_SEVERITY_TO_SAVE** - Minimum severity to save incidents (default: medium)
- **MIN_SEVERITY_TO_DELETE** - Minimum severity to delete messages (default: critical)

### Severity Thresholds

- **low** - Low toxicity, minimal action
- **medium** - Moderate toxicity, monitoring recommended
- **high** - High toxicity, action recommended
- **critical** - Critical toxicity, immediate action

## Bot Commands

- **!analyze [text]** - Analyze a message manually
- **!health** - Check ML service health
- **!stats** - Show bot statistics
- **!ping** - Check bot latency

## Features

### Real-time Analysis

The bot analyzes every message in real-time:
- Detects toxicity, sentiment, and threats
- Supports English, Kannada, Hindi, and code-mixed text
- Automatically detects language
- Saves incidents to database

### Incident Reporting

When an incident is detected:
- Incident is saved to Supabase database
- Includes message content, author, channel, language, etc.
- Severity and threat detection included
- Language detection details stored

### Message Actions

Based on severity:
- **Critical/Threats** - Message is deleted automatically
- **User Warning** - User is warned (if enabled)
- **Moderator Alert** - Alert sent to moderators (if configured)

### Language Detection

The bot automatically detects:
- **English** (en) - Full model support
- **Kannada** (kn) - Keyword-based + sentiment
- **Hindi** (hi) - Keyword-based + sentiment
- **Code-mixed** (mixed) - English + Kannada/Hindi

## Troubleshooting

### Bot Not Starting

- Check Discord token is correct
- Check Python version (3.9+)
- Check dependencies are installed
- Check logs for errors

### ML Service Not Available

- Check ML service is running
- Check ML_SERVICE_URL is correct
- Check network connectivity
- Check ML service logs

### Supabase Not Working

- Check Supabase credentials
- Check network connectivity
- Check database schema
- Check logs for errors

### Messages Not Being Deleted

- Check bot has permission to delete messages
- Check DELETE_MESSAGES is set to true
- Check MIN_SEVERITY_TO_DELETE threshold
- Check bot has proper permissions

## Monitoring

### Bot Statistics

Use `!stats` command to view:
- Messages analyzed
- Incidents detected
- Messages deleted
- Uptime
- Guilds

### Health Monitoring

Use `!health` command to check:
- ML service status
- Models loaded status

### Logging

Bot logs are saved to `discord_bot.log`:
- Info: Normal operations
- Warning: Incidents detected
- Error: Errors and exceptions

## Deployment

### Local Development

```bash
python bot.py
```

### Production

1. Use process manager (PM2, systemd, etc.)
2. Set up auto-restart
3. Monitor logs
4. Set up alerts

### Docker (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs
3. Check ML service status
4. Check Supabase connectivity

## Next Steps

1. ✅ Set up Discord bot
2. ✅ Configure environment variables
3. ✅ Start ML service
4. ✅ Start Discord bot
5. ✅ Test with !analyze command
6. ✅ Monitor incidents in Supabase
7. ✅ Configure alerts and thresholds

Happy coding! 🚀

