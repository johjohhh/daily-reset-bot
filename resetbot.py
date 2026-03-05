import discord
import asyncio
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from datetime import datetime, timedelta, timezone

def run_web():
    port = int(os.environ.get("PORT", "10000"))
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

threading.Thread(target=run_web, daemon=True).start()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1479109013063995423
TZ = timezone(timedelta(hours=8))  # GMT+8

intents = discord.Intents(guilds=True)
client = discord.Client(intents=intents)

async def updater():
    await client.wait_until_ready()

    # Force-fetch the channel from Discord (not cache)
    channel = await client.fetch_channel(CHANNEL_ID)
    print("Found channel:", channel.name, "ID:", channel.id)

    while not client.is_closed():
        now = datetime.now(TZ)
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        remaining = next_midnight - now

        total = int(remaining.total_seconds())
        h = total // 3600
        m = (total % 3600) // 60

        new_name = f"Daily Reset: {h:02d}h {m:02d}m"

        try:
            await channel.edit(name=new_name)
            print("Renamed to:", new_name)
        except Exception as e:
            print("Rename failed:", repr(e))

        await asyncio.sleep(300)  # 5 minutes

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(updater())

print("Starting bot…")
time.sleep(10)
client.run(TOKEN)

