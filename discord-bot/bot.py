"""
SafeGuard Discord Bot - Production Ready
Multilingual cyberbullying detection bot for Discord

Features:
- Real-time message analysis
- Multilingual support (English, Kannada, Hindi)
- Automatic incident reporting
- Configurable thresholds
- Language detection
- Supabase integration
"""

import discord
from discord.ext import commands
import requests
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Configuration
ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://localhost:8000")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Bot configuration
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
ALERT_CHANNEL_ID = os.getenv("ALERT_CHANNEL_ID")  # Optional: Channel ID for alerts
DELETE_MESSAGES = os.getenv("DELETE_MESSAGES", "true").lower() == "true"
WARN_USERS = os.getenv("WARN_USERS", "true").lower() == "true"

# Severity thresholds
MIN_SEVERITY_TO_SAVE = os.getenv("MIN_SEVERITY_TO_SAVE", "medium")  # low, medium, high, critical
MIN_SEVERITY_TO_DELETE = os.getenv("MIN_SEVERITY_TO_DELETE", "critical")  # high, critical

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Supabase client
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("Supabase client initialized")
else:
    supabase = None
    logger.warning("Supabase credentials not provided. Incidents will not be saved.")

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True

bot = commands.Bot(
    command_prefix=BOT_PREFIX,
    intents=intents,
    help_command=commands.DefaultHelpCommand()
)

# Bot statistics
bot_stats = {
    "messages_analyzed": 0,
    "incidents_detected": 0,
    "messages_deleted": 0,
    "start_time": None
}

def analyze_message(text: str) -> Optional[Dict]:
    """
    Call ML service to analyze a message
    
    Returns:
        dict: Analysis results or None if error
    """
    try:
        response = requests.post(
            f"{ML_SERVICE_URL}/analyze",
            json={"text": text, "platform": "discord"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.error(f"ML service timeout while analyzing message")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling ML service: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error analyzing message: {e}")
        return None

async def save_incident(message: discord.Message, analysis: Dict) -> Optional[Dict]:
    """
    Save incident to Supabase
    
    Returns:
        dict: Saved incident data or None if error
    """
    if not supabase:
        logger.warning("Supabase not configured. Incident not saved.")
        return None
    
    try:
        # Get language detection info
        language_info = analysis.get("details", {}).get("language_detection", {})
        detected_language = analysis.get("detected_language", "unknown")
        
        # Prepare incident data
        incident_data = {
            "platform": "discord",
            "severity": analysis["severity"],
            "status": "pending",
            "content": message.content,
            "context": {
                "channel_id": str(message.channel.id),
                "channel_name": message.channel.name,
                "guild_id": str(message.guild.id) if message.guild else None,
                "guild_name": message.guild.name if message.guild else None,
                "message_id": str(message.id),
                "message_url": message.jump_url,
                "author_mention": message.author.mention,
                "author_display_name": message.author.display_name,
                "language_detection": language_info,
                "detected_language": detected_language,
                "analysis_details": analysis.get("details", {}),
            },
            "author_id": str(message.author.id),
            "author_name": message.author.name,
            "channel_id": str(message.channel.id),
            "channel_name": message.channel.name,
            "message_url": message.jump_url,
            "toxicity_score": float(analysis["toxicity_score"]),
            "sentiment_score": float(analysis["sentiment_score"]),
            "detected_at": message.created_at.isoformat(),
        }
        
        # Insert into Supabase
        result = supabase.table("incidents").insert(incident_data).execute()
        
        if result.data:
            incident_id = result.data[0]["id"]
            logger.info(f"Incident saved: {incident_id}")
            bot_stats["incidents_detected"] += 1
            return result.data[0]
        else:
            logger.error("Failed to save incident: No data returned")
            return None
        
    except Exception as e:
        logger.error(f"Error saving incident: {e}")
        return None

async def update_bot_status(status: str = "online"):
    """Update bot status in Supabase"""
    if not supabase:
        return
    
    try:
        supabase.table("bot_status").upsert({
            "platform": "discord",
            "status": status,
            "last_ping": datetime.utcnow().isoformat(),
            "message_count": bot_stats["messages_analyzed"],
            "incidents_detected": bot_stats["incidents_detected"],
            "uptime_seconds": int((datetime.utcnow() - bot_stats["start_time"]).total_seconds()) if bot_stats["start_time"] else 0,
        }).execute()
        logger.debug(f"Bot status updated: {status}")
    except Exception as e:
        logger.error(f"Error updating bot status: {e}")

def get_severity_level(severity: str) -> int:
    """Convert severity to numeric level for comparison"""
    levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    return levels.get(severity.lower(), 0)

def should_save_incident(severity: str, is_threat: bool) -> bool:
    """Check if incident should be saved based on severity threshold"""
    min_level = get_severity_level(MIN_SEVERITY_TO_SAVE)
    severity_level = get_severity_level(severity)
    
    # Always save threats
    if is_threat:
        return True
    
    # Save if severity meets threshold
    return severity_level >= min_level

def should_delete_message(severity: str, is_threat: bool) -> bool:
    """Check if message should be deleted based on severity threshold"""
    if not DELETE_MESSAGES:
        return False
    
    min_level = get_severity_level(MIN_SEVERITY_TO_DELETE)
    severity_level = get_severity_level(severity)
    
    # Always delete threats
    if is_threat:
        return True
    
    # Delete if severity meets threshold
    return severity_level >= min_level

@bot.event
async def on_ready():
    """Called when bot is ready"""
    logger.info(f'{bot.user} has logged in!')
    logger.info(f'Bot ID: {bot.user.id}')
    logger.info(f'Guilds: {len(bot.guilds)}')
    logger.info(f'Multilingual ML Service: {ML_SERVICE_URL}')
    
    bot_stats["start_time"] = datetime.utcnow()
    
    # Update bot status
    await update_bot_status("online")
    
    # Update status periodically
    bot.loop.create_task(update_status_periodically())
    
    # Set bot activity
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="for toxic messages"
        )
    )

async def update_status_periodically():
    """Update bot status periodically"""
    while True:
        await asyncio.sleep(60)  # Update every minute
        await update_bot_status("online")

@bot.event
async def on_message(message: discord.Message):
    """Handle incoming messages"""
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Ignore commands (let commands be handled by command handler)
    if message.content.startswith(BOT_PREFIX):
        await bot.process_commands(message)
        return
    
    # Skip empty messages
    if not message.content or len(message.content.strip()) == 0:
        return
    
    # Analyze message
    bot_stats["messages_analyzed"] += 1
    analysis = analyze_message(message.content)
    
    if analysis is None:
        # ML service unavailable, skip analysis
        logger.warning("ML service unavailable. Skipping analysis.")
        return
    
    # Get analysis results
    severity = analysis.get("severity", "low")
    is_threat = analysis.get("is_threat", False)
    toxicity_score = analysis.get("toxicity_score", 0.0)
    sentiment_score = analysis.get("sentiment_score", 0.0)
    detected_language = analysis.get("detected_language", "unknown")
    
    # Check if incident should be saved
    if should_save_incident(severity, is_threat):
        # Save incident to database
        incident = await save_incident(message, analysis)
        
        # Log incident
        logger.warning(f"⚠️ Incident detected: {severity} severity | Language: {detected_language}")
        logger.warning(f"   Message: {message.content[:100]}...")
        logger.warning(f"   Author: {message.author.name} ({message.author.id})")
        logger.warning(f"   Channel: {message.channel.name} ({message.channel.id})")
        logger.warning(f"   Toxicity: {toxicity_score:.3f} | Sentiment: {sentiment_score:.3f}")
        logger.warning(f"   Threat: {is_threat}")
        
        # Send alert to moderators (if alert channel is configured)
        if ALERT_CHANNEL_ID:
            await send_alert(message, analysis, incident)
        
        # Delete message if needed
        if should_delete_message(severity, is_threat):
            try:
                await message.delete()
                bot_stats["messages_deleted"] += 1
                logger.info(f"Message deleted: {message.id}")
                
                # Warn user if enabled
                if WARN_USERS:
                    warning_msg = await message.channel.send(
                        f"⚠️ {message.author.mention}, your message was removed due to policy violations. "
                        f"Severity: {severity.upper()}"
                    )
                    # Delete warning message after 10 seconds
                    await asyncio.sleep(10)
                    try:
                        await warning_msg.delete()
                    except:
                        pass
                        
            except discord.Forbidden:
                logger.error("Bot doesn't have permission to delete messages")
            except discord.NotFound:
                logger.warning("Message not found (may have been deleted already)")
            except Exception as e:
                logger.error(f"Error deleting message: {e}")
    
    # Process commands (if any)
    await bot.process_commands(message)

async def send_alert(message: discord.Message, analysis: Dict, incident: Optional[Dict]):
    """Send alert to moderators channel"""
    try:
        alert_channel = bot.get_channel(int(ALERT_CHANNEL_ID))
        if not alert_channel:
            logger.warning(f"Alert channel not found: {ALERT_CHANNEL_ID}")
            return
        
        severity = analysis.get("severity", "unknown")
        is_threat = analysis.get("is_threat", False)
        detected_language = analysis.get("detected_language", "unknown")
        
        # Create embed
        embed = discord.Embed(
            title="🚨 Incident Detected",
            description=f"**Severity:** {severity.upper()}\n**Threat:** {'Yes' if is_threat else 'No'}\n**Language:** {detected_language}",
            color=discord.Color.red() if severity == "critical" else discord.Color.orange(),
            timestamp=message.created_at
        )
        
        embed.add_field(
            name="Message",
            value=message.content[:1000] if len(message.content) <= 1000 else message.content[:1000] + "...",
            inline=False
        )
        
        embed.add_field(
            name="Author",
            value=f"{message.author.mention} ({message.author.name})",
            inline=True
        )
        
        embed.add_field(
            name="Channel",
            value=f"{message.channel.mention} ({message.channel.name})",
            inline=True
        )
        
        embed.add_field(
            name="Toxicity Score",
            value=f"{analysis.get('toxicity_score', 0):.2%}",
            inline=True
        )
        
        embed.add_field(
            name="Sentiment Score",
            value=f"{analysis.get('sentiment_score', 0):.2f}",
            inline=True
        )
        
        embed.add_field(
            name="Message URL",
            value=message.jump_url,
            inline=False
        )
        
        if incident:
            embed.add_field(
                name="Incident ID",
                value=incident.get("id", "Unknown"),
                inline=True
            )
        
        await alert_channel.send(embed=embed)
        
    except Exception as e:
        logger.error(f"Error sending alert: {e}")

@bot.command(name='analyze')
async def analyze_command(ctx, *, text: str = None):
    """
    Manually analyze a message
    Usage: !analyze <text>
    If no text provided, analyzes the last message in the channel
    """
    if text is None:
        # Analyze the last message
        async for msg in ctx.channel.history(limit=2):
            if not msg.author.bot and msg.id != ctx.message.id:
                text = msg.content
                break
        
        if text is None:
            await ctx.send("❌ No message found to analyze.")
            return
    
    # Analyze message
    analysis = analyze_message(text)
    
    if analysis is None:
        await ctx.send("❌ ML service is unavailable.")
        return
    
    # Get language detection info
    language_info = analysis.get("details", {}).get("language_detection", {})
    detected_language = analysis.get("detected_language", "unknown")
    
    # Create embed with results
    embed = discord.Embed(
        title="📊 Message Analysis",
        description=f"Analysis of: `{text[:200]}...`" if len(text) > 200 else f"Analysis of: `{text}`",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    # Severity color
    severity = analysis.get("severity", "low")
    if severity == "critical":
        embed.color = discord.Color.red()
    elif severity == "high":
        embed.color = discord.Color.orange()
    elif severity == "medium":
        embed.color = discord.Color.gold()
    else:
        embed.color = discord.Color.green()
    
    embed.add_field(
        name="Toxicity Score",
        value=f"{analysis.get('toxicity_score', 0):.2%}",
        inline=True
    )
    
    embed.add_field(
        name="Sentiment Score",
        value=f"{analysis.get('sentiment_score', 0):.2f}",
        inline=True
    )
    
    embed.add_field(
        name="Severity",
        value=severity.upper(),
        inline=True
    )
    
    embed.add_field(
        name="Threat Detected",
        value="Yes" if analysis.get("is_threat", False) else "No",
        inline=True
    )
    
    embed.add_field(
        name="Detected Language",
        value=detected_language.upper(),
        inline=True
    )
    
    embed.add_field(
        name="Confidence",
        value=f"{analysis.get('confidence', 0):.2%}",
        inline=True
    )
    
    # Add language detection details
    if language_info:
        mixed_languages = language_info.get("mixed_languages", [])
        if mixed_languages:
            embed.add_field(
                name="Languages",
                value=", ".join([lang.upper() for lang in mixed_languages]),
                inline=False
            )
    
    await ctx.send(embed=embed)

@bot.command(name='health')
async def health_command(ctx):
    """Check ML service health"""
    try:
        response = requests.get(f"{ML_SERVICE_URL}/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            embed = discord.Embed(
                title="✅ ML Service Health",
                description=f"Status: {health.get('status', 'unknown')}",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Models Loaded",
                value="Yes" if health.get('models_loaded', False) else "No",
                inline=True
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ ML Service returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"❌ ML Service is unavailable: {str(e)}")

@bot.command(name='stats')
async def stats_command(ctx):
    """Show bot statistics"""
    uptime = (datetime.utcnow() - bot_stats["start_time"]).total_seconds() if bot_stats["start_time"] else 0
    uptime_hours = int(uptime / 3600)
    uptime_minutes = int((uptime % 3600) / 60)
    
    embed = discord.Embed(
        title="📊 Bot Statistics",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="Messages Analyzed",
        value=str(bot_stats["messages_analyzed"]),
        inline=True
    )
    
    embed.add_field(
        name="Incidents Detected",
        value=str(bot_stats["incidents_detected"]),
        inline=True
    )
    
    embed.add_field(
        name="Messages Deleted",
        value=str(bot_stats["messages_deleted"]),
        inline=True
    )
    
    embed.add_field(
        name="Uptime",
        value=f"{uptime_hours}h {uptime_minutes}m",
        inline=True
    )
    
    embed.add_field(
        name="Guilds",
        value=str(len(bot.guilds)),
        inline=True
    )
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping_command(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: {latency}ms")

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle errors"""
    logger.error(f"Error in event {event}: {args} {kwargs}")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}")
    else:
        logger.error(f"Error in command {ctx.command}: {error}")
        await ctx.send(f"❌ An error occurred: {str(error)}")

# Run bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN environment variable is not set!")
        exit(1)
    
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        exit(1)

