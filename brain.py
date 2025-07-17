# brain.py - Training data for the Telegram bot
# Add your training data here in the format: trigger_words -> response

# Simple word-based responses
RESPONSES = {
    # Greetings
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! What's up?",
    "hey": "Hey! How's it going?",
    "good morning": "Good morning! Hope you have a great day!",
    "good afternoon": "Good afternoon! How's your day going?",
    "good evening": "Good evening! How are you doing?",
    
    # Common questions
    "how are you": "I'm doing great, thanks for asking! How about you?",
    "what's up": "Not much, just here to chat with you! What's on your mind?",
    "what can you do": "I can chat with you and answer questions based on what I've learned!",
    "help": "I'm here to help! Just ask me anything or try saying hello!",
    
    # Farewells
    "bye": "Goodbye! Have a great day!",
    "goodbye": "Goodbye! Take care!",
    "see you later": "See you later! Have a good one!",
    "goodnight": "Goodnight! Sweet dreams!",
    
    # Fun responses
    "joke": "Why don't scientists trust atoms? Because they make up everything!",
    "tell me a joke": "What do you call a fake noodle? An impasta!",
    "how's the weather": "I'm not sure about the weather, but I hope it's nice where you are!",
    "what's your name": "I'm your friendly Telegram bot! You can call me Bot.",
    
    # Default responses for unknown inputs
    "default": [
        "I'm not sure how to respond to that. Can you try asking something else?",
        "That's interesting! Tell me more about it.",
        "I don't have a response for that yet, but I'm learning!",
        "Could you rephrase that? I might understand better.",
        "That's a good question! I'm still learning new things."
    ]
}

# Commands (these start with /)
COMMANDS = {
    "start": "Welcome! I'm your personal chatbot. Type /help to see what I can do!",
    "help": """
🤖 *Bot Commands:*
/start - Start the bot
/help - Show this help message
/info - Get bot information
/joke - Get a random joke

💬 *Chat with me:*
Just type anything and I'll try to respond! I can understand:
- Greetings (hello, hi, hey)
- Questions (how are you, what's up)
- Farewells (bye, goodbye)
- And much more!
    """,
    "info": "I'm a simple chatbot that learns from the responses in brain.py. You can train me by adding more responses!",
    "joke": "Here's a joke for you: Why did the scarecrow win an award? Because he was outstanding in his field!"
}

# Training functions
def add_response(trigger, response):
    """Add a new response to the bot's brain"""
    RESPONSES[trigger.lower()] = response
    print(f"Added: '{trigger}' -> '{response}'")

def add_command(command, response):
    """Add a new command to the bot's brain"""
    COMMANDS[command.lower()] = response
    print(f"Added command: /{command} -> '{response}'")

def list_responses():
    """List all current responses"""
    print("\n=== CURRENT RESPONSES ===")
    for trigger, response in RESPONSES.items():
        if trigger != "default":
            print(f"'{trigger}' -> '{response}'")
    
    print("\n=== CURRENT COMMANDS ===")
    for command, response in COMMANDS.items():
        print(f"/{command} -> '{response[:50]}...' " if len(response) > 50 else f"/{command} -> '{response}'")

# Quick training function for command line
def train_bot():
    """Interactive training function"""
    print("=== BOT TRAINING MODE ===")
    print("Type 'quit' to exit training")
    print("Type 'list' to see all responses")
    print("Type 'cmd' to add a command instead of a response")
    
    while True:
        choice = input("\nWhat would you like to do? (add/list/cmd/quit): ").lower()
        
        if choice == 'quit':
            break
        elif choice == 'list':
            list_responses()
        elif choice == 'add':
            trigger = input("Enter trigger word/phrase: ")
            response = input("Enter response: ")
            add_response(trigger, response)
        elif choice == 'cmd':
            command = input("Enter command name (without /): ")
            response = input("Enter command response: ")
            add_command(command, response)
        else:
            print("Invalid choice. Try 'add', 'list', 'cmd', or 'quit'")

if __name__ == "__main__":
    train_bot()
