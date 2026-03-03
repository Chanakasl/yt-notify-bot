import discord
import feedparser
import asyncio
import os

TOKEN = os.getenv('TOKEN')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

sent_videos = set()

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} ලොග් වුනා!')
        self.loop.create_task(self.check_youtube())

    async def check_youtube(self):
        await self.wait_until_ready()
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        if not channel:
            print("Channel එක හොයාගන්න බැහැ!")
            return
        
        while not self.is_closed():
            try:
                feed_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}'
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:5]:
                    video_id = entry.video_id
                    if video_id not in sent_videos:
                        await channel.send(f"**නව YouTube Video!**\n{entry.title}\n{entry.link}")
                        sent_videos.add(video_id)
                        print(f"Sent: {entry.title}")
                
                await asyncio.sleep(300)  # විනාඩි 5ක් නවතින්න
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(60)

client = MyClient(intents=intents)
client.run(TOKEN)
