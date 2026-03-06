# Reset Countdown Discord Bot

A Discord bot that continuously renames a specific voice/text channel with a countdown showing how much time remains until midnight (GMT+8).

## Project Structure

- `resetbot.py` — Main bot script
- `requirements.txt` — Python dependencies

## How It Works

- Connects to Discord using `discord.py`
- Targets a hardcoded channel ID (`CHANNEL_ID = 1479168730213646528`)
- Renames the channel every 4 minutes with format: `Reset Countdown: HHh MMm`
- Includes a small HTTP server (port from `PORT` env var, default `10000`) as a keep-alive ping endpoint

## Environment Variables

- `TOKEN` (secret) — Discord bot token, required

## Dependencies

- `discord.py==2.3.2`

## Workflow

- **Start application**: `python resetbot.py` — runs as a console process

## Notes

- The bot waits 4 minutes (`time.sleep(240)`) on startup before connecting to Discord
- Timezone is GMT+8
- Originally designed for Render hosting, adapted to run on Replit
