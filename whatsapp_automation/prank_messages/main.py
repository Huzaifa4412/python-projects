import pyautogui as pg
import time
import random

# List of commonly disliked animals
messages = [
    "Masti na karow 🙏",
    "Insaan bn jow 🧒",
    "Pharlo 👨‍🎓",
    "Insta chor do",
    "Coding sikh lo bachi mil gai gi",
    "Inssan ka puttar bn jow",
    "Client Hunting karow",
    "Eid say phalay client chaiya",
    "😘",
]

# Wait time to switch to WhatsApp or any text field
time.sleep(15)  # Gives you 5 seconds to click on WhatsApp or Notepad

# Send 100 messages
for i in range(150):
    meg = random.choice(messages)  # Pick a random MESSAGE
    message = f"AZEEM Beta {meg} 🥱"  # Construct the message
    pg.write(message)  # Type the message
    pg.press("enter")  # Press Enter to send
    time.sleep(0.5)  # Short delay to avoid typing too fast
