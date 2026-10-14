# Video to GIF Converter Bot

A Telegram bot that converts short videos into GIFs directly inside Telegram.

## Features
- Convert MP4/MOV videos to GIF
- Max size: 20MB
- Max length: 30 seconds
- Inline menu with buttons

## Deploy on Railway

1. Push this repo to GitHub.
2. Create a new project on Railway and deploy from GitHub.
3. Add environment variable:
   - `BOT_TOKEN` = your token from BotFather
4. Railway will auto-install FFmpeg and start the bot.

## BotFather Setup

**Name:** Video to GIF Converter
**About:** Convert short videos into GIFs directly inside Telegram. Simple, fast, no extra app needed.
**Description:**
Video to GIF Converter turns your short videos into GIFs without leaving Telegram.
Send a short video (under 20MB, under 30 seconds) and receive your GIF.

**Commands:**
start - Start the bot
help - How to use
about - About this bot
