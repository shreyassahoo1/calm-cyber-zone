"""
Discord Bot Integration Example for SafeGuard ML Service

This example shows how to integrate the ML service with your Discord bot.
Make sure to install discord.py: pip install discord.py
"""

import discord
from discord.ext import commands
import requests
import os
from supabase import create_client, Client

# Configuration
ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://localhost:8000")
SUPABASE_URL = os.getenv("SUPABASE_URL", "your-supabase-url")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-supabase-key")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "MTQzODAyMzg0MTc2NjE3ODg4Ng.GwRW0Q.TvSl3vpE4NEls0bX3MIutZ0onAh_BAsZuE6WE0")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def analyze_message(text: str) -> dict:
    """
    Call ML service to analyze a message
    """
    try:
        response = requests.post(
            f"{ML_SERVICE_URL}/analyze",
            json={"text": text, "platform": "discord"},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling ML service: {e}")
        return None

async def save_incident(message: discord.Message, analysis: dict):
    """
    Save incident to Supabase
    """
    try:
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
            },
            "author_id": str(message.author.id),
            "author_name": message.author.name,
            "channel_id": str(message.channel.id),
            "channel_name": message.channel.name,
            "message_url": message.jump_url,
            "toxicity_score": analysis["toxicity_score"],
            "sentiment_score": analysis["sentiment_score"],
            "detected_at": message.created_at.isoformat(),
        }
        
        # Insert into Supabase
        result = supabase.table("incidents").insert(incident_data).execute()
        print(f"Incident saved: {result.data[0]['id']}")
        return result.data[0]
        
    except Exception as e:
        print(f"Error saving incident: {e}")
        return None

@bot.event
async def on_ready():
    print(f'{bot.user} has logged in!')
    
    # Update bot status in Supabase
    try:
        supabase.table("bot_status").upsert({
            "platform": "discord",
            "status": "online",
            "last_ping": "now()",
        }).execute()
    except Exception as e:
        print(f"Error updating bot status: {e}")

@bot.event
async def on_message(message: discord.Message):
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Ignore commands (let commands be handled by command handler)
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return
    
    # Analyze message
    analysis = analyze_message(message.content)
    
    if analysis is None:
        # ML service unavailable, skip analysis
        return
    
    # Check if message is problematic
    severity = analysis["severity"]
    is_threat = analysis["is_threat"]
    
    # Handle based on severity
    if severity in ["high", "critical"] or is_threat:
        # Save incident to database
        incident = await save_incident(message, analysis)
        
        # Log to console
        print(f"⚠️ Incident detected: {severity} severity")
        print(f"   Message: {message.content[:50]}...")
        print(f"   Author: {message.author.name}")
        print(f"   Toxicity: {analysis['toxicity_score']}")
        print(f"   Threat: {is_threat}")
        
        # Optional: Delete message or warn user
        if severity == "critical" or is_threat:
            try:
                await message.delete()
                await message.channel.send(
                    f"⚠️ A message from {message.author.mention} was removed due to policy violations."
                )
            except discord.Forbidden:
                print("Bot doesn't have permission to delete messages")
        
        # Optional: Send alert to moderators
        # You can add a channel ID for alerts
        # alert_channel = bot.get_channel(YOUR_ALERT_CHANNEL_ID)
        # if alert_channel:
        #     await alert_channel.send(f"🚨 Critical incident detected: {message.jump_url}")
    
    # Process commands (if any)
    await bot.process_commands(message)

@bot.command(name='analyze')
async def analyze_command(ctx, *, text: str = None):
    """
    Manually analyze a message
    Usage: !analyze <text>
    """
    if text is None:
        # Analyze the last message
        async for message in ctx.channel.history(limit=2):
            if not message.author.bot and message.id != ctx.message.id:
                text = message.content
                break
        
        if text is None:
            await ctx.send("No message found to analyze.")
            return
    
    analysis = analyze_message(text)
    
    if analysis is None:
        await ctx.send("❌ ML service is unavailable.")
        return
    
    # Create embed with results
    embed = discord.Embed(
        title="Message Analysis",
        description=f"Analysis of: `{text[:100]}...`" if len(text) > 100 else f"Analysis of: `{text}`",
        color=discord.Color.orange()
    )
    
    embed.add_field(
        name="Toxicity Score",
        value=f"{analysis['toxicity_score']:.2%}",
        inline=True
    )
    
    embed.add_field(
        name="Sentiment Score",
        value=f"{analysis['sentiment_score']:.2f}",
        inline=True
    )
    
    embed.add_field(
        name="Severity",
        value=analysis['severity'].upper(),
        inline=True
    )
    
    embed.add_field(
        name="Threat Detected",
        value="Yes" if analysis['is_threat'] else "No",
        inline=True
    )
    
    embed.add_field(
        name="Confidence",
        value=f"{analysis['confidence']:.2%}",
        inline=True
    )
    
    await ctx.send(embed=embed)

@bot.command(name='health')
async def health_command(ctx):
    """
    Check ML service health
    """
    try:
        response = requests.get(f"{ML_SERVICE_URL}/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            await ctx.send(f"✅ ML Service is healthy. Models loaded: {health.get('models_loaded', False)}")
        else:
            await ctx.send(f"❌ ML Service returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"❌ ML Service is unavailable: {str(e)}")

# Run bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

