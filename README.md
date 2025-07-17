# pup-bot

A Telegram chatbot with GitHub Actions deployment.

## Features
- Easy training with brain.py
- Automated deployment with GitHub Actions
- 24/7 hosting on GitHub

## Setup
1. Fork this repository
2. Add your `BOT_TOKEN` to GitHub Secrets
3. Push changes to trigger deployment

## Local Development
```bash
pip install -r requirements.txt
python main.py
```

## Training the Bot
```bash
python brain.py
```

Bot is automatically deployed when you push to the main branch!
