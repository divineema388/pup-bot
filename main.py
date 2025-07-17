import os
import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from brain import RESPONSES, COMMANDS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.app = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up command and message handlers"""
        # Add command handlers
        for command in COMMANDS.keys():
            self.app.add_handler(CommandHandler(command, self.handle_command))
        
        # Add message handler for regular text
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle bot commands"""
        command = update.message.text[1:].lower()  # Remove '/' and convert to lowercase
        
        if command in COMMANDS:
            response = COMMANDS[command]
            await update.message.reply_text(response, parse_mode='Markdown')
        else:
            await update.message.reply_text("Unknown command. Type /help for available commands.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user_message = update.message.text.lower()
        user_name = update.effective_user.first_name
        
        # Log the message
        logger.info(f"Received message from {user_name}: {user_message}")
        
        # Find best response
        response = self.find_response(user_message)
        
        # Send response
        await update.message.reply_text(response)
    
    def find_response(self, message):
        """Find the best response for a given message"""
        message = message.lower().strip()
        
        # Direct match
        if message in RESPONSES:
            return RESPONSES[message]
        
        # Check for partial matches
        for trigger, response in RESPONSES.items():
            if trigger != "default" and trigger in message:
                return response
        
        # Check for keyword matches
        message_words = message.split()
        for trigger, response in RESPONSES.items():
            if trigger != "default":
                trigger_words = trigger.split()
                if any(word in message_words for word in trigger_words):
                    return response
        
        # Default response
        default_responses = RESPONSES["default"]
        return random.choice(default_responses)
    
    def run(self):
        """Start the bot"""
        logger.info("Starting bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function to run the bot"""
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("Error: BOT_TOKEN not found in environment variables!")
        print("Please check your .env file and make sure it contains:")
        print("BOT_TOKEN=your_bot_token_here")
        return
    
    try:
        bot = TelegramBot(bot_token)
        print("Bot is starting...")
        print("Press Ctrl+C to stop the bot")
        bot.run()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
