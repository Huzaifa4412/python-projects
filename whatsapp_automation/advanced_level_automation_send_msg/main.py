from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import urllib.parse

# Message to send
message_body = "Hello! This is a test message sent via WhatsApp."

# Path to the file containing phone numbers (one per line, e.g., +923001234567)
numbers_file = "phone_numbers.txt"


# Function to validate phone number format (basic validation for + followed by 10-15 digits)
def is_valid_phone_number(number):
    pattern = r"^\+\d{10,15}$"
    return bool(re.match(pattern, number))


# Read phone numbers from file
try:
    with open(numbers_file, "r") as file:
        phone_numbers = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print(f"Error: The file {numbers_file} was not found.")
    exit(1)

# Initialize Selenium WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is in PATH or specify path
driver.get("https://web.whatsapp.com")

# Wait for user to scan QR code (manual login)
print("Please scan the QR code on WhatsApp Web to log in.")
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '//div[@title="Search input textbox"]'))
)
print("Logged in successfully!")

# Send message to each phone number
successful_sends = 0
failed_sends = 0

for number in phone_numbers:
    # Validate phone number format
    if not is_valid_phone_number(number):
        print(f"Invalid phone number format: {number}")
        failed_sends += 1
        continue

    try:
        # Construct WhatsApp Web URL for the phone number
        encoded_number = urllib.parse.quote(number)
        driver.get(f"https://web.whatsapp.com/send?phone={encoded_number[1:]}")

        # Wait for the chat to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@title="Type a message"]'))
        )

        # Find the message input box and send the message
        message_box = driver.find_element(By.XPATH, '//div[@title="Type a message"]')
        message_box.send_keys(message_body)
        message_box.send_keys(Keys.ENTER)

        print(f"Message sent to {number}")
        successful_sends += 1

        # Add delay to avoid WhatsApp rate limits (e.g., 5 seconds)
        time.sleep(5)
    except Exception as e:
        print(f"Failed to send message to {number}: {e}")
        failed_sends += 1

# Close the browser
driver.quit()

# Summary
print(
    f"\nSummary: {successful_sends} messages sent successfully, {failed_sends} failed."
)
