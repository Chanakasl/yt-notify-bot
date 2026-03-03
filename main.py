import discord
from discord.ext import commands
import feedparser
import asyncio
import os

TOKEN = os.getenv('TOKEN')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

sent_videos = set()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} ලොග් වුනා!')
    bot.loop.create_task(check_youtube())

async def check_youtube():
    await bot.wait_until_ready()
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        print("Channel එක හොයාගන්න බැහැ!")
        return
    
    while not bot.is_closed():
        try:
            feed_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}'
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:5]:
                video_id = entry.video_id
                if video_id not in sent_videos:
                    await channel.send(f"**නව YouTube Video!**\n{entry.title}\n{entry.link}")
                    sent_videos.add(video_id)
                    print(f"Sent: {entry.title}")
            
            await asyncio.sleep(300)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(60)

# !ping command එක
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

# !lastvideo command එක (අන්තිම video එක පෙන්වන්න)
@bot.command()
async def lastvideo(ctx):
    feed_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}'
    feed = feedparser.parse(feed_url)
    if feed.entries:
        latest = feed.entries[0]
        await ctx.send(f"**අන්තිම YouTube Video:**\n{latest.title}\n{latest.link}")
    else:
        await ctx.send("වීඩියෝ හම්බුනේ නැහැ")

# !check command එක (අතින් check කරන්න)
@bot.command()
async def check(ctx):
    feed_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}'
    feed = feedparser.parse(feed_url)
    new_videos = []
    for entry in feed.entries[:5]:
        if entry.video_id not in sent_videos:
            new_videos.append(entry)
    
    if new_videos:
        for video in new_videos:
            await ctx.send(f"**අලුත් YouTube Video!**\n{video.title}\n{video.link}")
            sent_videos.add(video.video_id)
    else:
        await ctx.send("අලුත් වීඩියෝ නැහැ")

bot.run(TOKEN)
