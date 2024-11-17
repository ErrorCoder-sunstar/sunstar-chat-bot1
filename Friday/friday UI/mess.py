import pywhatkit as kit
import datetime

# Function to validate phone numbers
def is_valid_number(phone_number):
    if phone_number.startswith('+') and phone_number[1:].isdigit():
        return True
    return False

# List of phone numbers to send the message to
phone_numbers = [
    '+917449131894','+917010984429',]
    # Add more phone numbers here


# Message to send
message_body = 'Hai'

# Define the time to send the message
send_hour = 21  # 11 PM
send_minute = 54  # 14 minutes past the hour

# Get current time
now = datetime.datetime.now()

# Adjust send time if the specified time is already past
if now.hour > send_hour or (now.hour == send_hour and now.minute >= send_minute):
    send_hour = (now.hour + 1) % 24
    send_minute = (now.minute + 1) % 60

# Send the message to each phone number
for number in phone_numbers:
    if is_valid_number(number):
        try:
            kit.sendwhatmsg(number, message_body, send_hour, send_minute)
            print(f"Scheduled message to {number} at {send_hour:02d}:{send_minute:02d}")
        except Exception as e:
            print(f"Failed to schedule message to {number}: {e}")
    else:
        print(f"Invalid phone number format: {number}")

print("Messages scheduled successfully!")
