import discord
import asyncio
import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timedelta, timezone

# Small web server so Render keeps the service alive
def run_web():
    port = int(os.environ.get("PORT", "10000"))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

threading.Thread(target=run_web, daemon=True).start()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN env var is missing. Add TOKEN in Render Environment Variables.")

CHANNEL_ID = 1479168730213646528
TZ = timezone(timedelta(hours=8))  # GMT+8

intents = discord.Intents(guilds=True)
client = discord.Client(intents=intents)

async def updater():
    await client.wait_until_ready()

    channel = await client.fetch_channel(CHANNEL_ID)
    print("Found channel:", channel.name, "ID:", channel.id)

    while not client.is_closed():
        now = datetime.now(TZ)
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        remaining = next_midnight - now

        total = int(remaining.total_seconds())
        hours = total // 3600
        minutes = (total % 3600) // 60

        new_name = f"Reset Countdown: {hours:02d}h {minutes:02d}m"

        try:
            await channel.edit(name=new_name)
            print("Renamed to:", new_name)
        except Exception as e:
            print("Rename failed:", repr(e))

        await asyncio.sleep(360)  # update every 6 minutes

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(updater())

print("Starting bot...")
time.sleep(360)

client.run(TOKEN)






