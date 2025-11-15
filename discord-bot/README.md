# SafeGuard Discord Bot

Production-ready Discord bot for real-time cyberbullying detection with multilingual support (English, Kannada, Hindi).

## Features

- ✅ **Real-time Message Analysis** - Analyzes every message for toxicity, sentiment, and threats
- ✅ **Multilingual Support** - Supports English, Kannada, Hindi, and code-mixed text
- ✅ **Language Detection** - Automatically detects language of messages
- ✅ **Automatic Incident Reporting** - Saves incidents to Supabase database
- ✅ **Configurable Thresholds** - Customize severity thresholds for actions
- ✅ **Message Deletion** - Automatically deletes toxic messages (configurable)
- ✅ **User Warnings** - Warns users when messages are deleted (configurable)
- ✅ **Moderator Alerts** - Sends alerts to moderators (optional)
- ✅ **Bot Statistics** - Track messages analyzed, incidents detected, etc.
- ✅ **Health Monitoring** - Monitor ML service health

## Prerequisites

1. **Python 3.9+**
2. **Discord Bot Token** - Create a bot at https://discord.com/developers/applications
3. **ML Service** - Must be running (see `ml-service/README.md`)
4. **Supabase** - Database for storing incidents (optional but recommended)

## Installation

### 1. Clone Repository

```bash
cd discord-bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` file:

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

## Configuration

### Environment Variables

- **DISCORD_TOKEN** (required) - Your Discord bot token
- **ML_SERVICE_URL** (optional) - ML service URL (default: http://localhost:8000)
- **SUPABASE_URL** (optional) - Supabase URL for database
- **SUPABASE_KEY** (optional) - Supabase API key
- **BOT_PREFIX** (optional) - Bot command prefix (default: !)
- **ALERT_CHANNEL_ID** (optional) - Channel ID for moderator alerts
- **DELETE_MESSAGES** (optional) - Enable/disable message deletion (default: true)
- **WARN_USERS** (optional) - Enable/disable user warnings (default: true)
- **MIN_SEVERITY_TO_SAVE** (optional) - Minimum severity to save incidents (default: medium)
- **MIN_SEVERITY_TO_DELETE** (optional) - Minimum severity to delete messages (default: critical)

### Severity Levels

- **low** - Low toxicity, minimal action needed
- **medium** - Moderate toxicity, may require monitoring
- **high** - High toxicity, action recommended
- **critical** - Critical toxicity, immediate action required

## Running the Bot

### 1. Start ML Service

Make sure the ML service is running:

```bash
cd ml-service
python main.py
```

### 2. Start Discord Bot

```bash
python bot.py
```

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

## Supabase Integration

The bot saves incidents to Supabase with the following fields:
- Platform (discord)
- Severity (low, medium, high, critical)
- Status (pending, reviewing, resolved, dismissed)
- Content (message content)
- Context (JSON with channel, guild, language, etc.)
- Author ID and name
- Channel ID and name
- Message URL
- Toxicity score
- Sentiment score
- Detected language
- Detection timestamp

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

## Permissions

The bot needs the following permissions:
- **Read Messages** - To read messages
- **Send Messages** - To send warnings and commands
- **Delete Messages** - To delete toxic messages
- **Embed Links** - To send rich embeds
- **Read Message History** - To analyze messages

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

## License

MIT License

## Credits

- SafeGuard Platform Team
- ML Service: Multilingual toxicity detection
- Supabase: Database and backend

