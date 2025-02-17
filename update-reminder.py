import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import schedule
import time

# Load environment variables from .env file
load_dotenv()

# Get the Slack Bot token and comma-separated Channel IDs from environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_IDS = os.getenv("SLACK_CHANNEL_IDS")  # e.g., "CHANNEL1,CHANNEL2,CHANNEL3"
UTC_24HRS_TIME = os.getenv("UTC_24HRS_TIME")

# Parse channel IDs into a list, stripping any extra whitespace
channels = [channel.strip() for channel in SLACK_CHANNEL_IDS.split(",")]

# Initialize the Slack client with your Bot token
client = WebClient(token=SLACK_BOT_TOKEN)

def send_startup_message():
    startup_message = (
        "Hi <!channel> 👋, I'm sudo, I'll be reminding you daily to post your updates in the channel.\n"
        "_Send your updates in a format:_\n\n"
        "*Yesterday's Recap:*\n"
        "\t1. Task -1\n"
        "\t2. Task -2\n"
        "\t3. Task -3\n\n"
        "*Today's Focus:*\n"
        "\t1. Task 1\n"
        "\t2. Task 2\n"
        "\t3. Task 3\n\n"
        "*Blockers (if any):*\n"
        "\tNone"
    )
    for channel in channels:
        try:
            response = client.chat_postMessage(
                channel=channel,
                text=startup_message
            )
            print(f"Startup message sent to {channel}: {response['message']['text']}")
        except SlackApiError as e:
            print(f"Error sending startup message to {channel}: {e.response['error']}")

def send_reminder():
    for channel in channels:
        try:
            response = client.chat_postMessage(
                channel=channel,  # Send the message to the current channel
                text="<!channel> Please post your updates for the day!"
            )
            print(f"Reminder sent to {channel}: {response['message']['text']}")
        except SlackApiError as e:
            print(f"Error sending reminder to {channel}: {e.response['error']}")

# Send the one-time startup message immediately upon starting the script
send_startup_message()

# Schedule the daily reminder message at the specified UTC time
schedule.every().day.at(UTC_24HRS_TIME).do(send_reminder)

# Keep the script running to handle the schedule
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check the schedule every minute
