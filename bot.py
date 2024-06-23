import discord
import asyncio
import json
from datetime import datetime, timedelta
import pytz

# NOT´E THAT IN ORDER FOR THIS TO WORK YOU HAVE TO BE IN THE SAME SERVER AS THE BOT!

# Replace TOKEN with the discord token
TOKEN = 'TOKEN'

# Replace UID WITH YOUR UID
USER_ID = UID

# Tbh idk about this ask chatgpt how to set your timezone here mine was europe berlin
berlin_tz = pytz.timezone('Europe/Berlin')

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

SCHEDULE_FILE = 'schedule.json'

def load_schedule():
    try:
        with open(SCHEDULE_FILE, 'r') as f:
            schedule = json.load(f)
        for entry in schedule:
            entry['datetime'] = berlin_tz.localize(datetime.strptime(entry['datetime'], '%Y-%m-%d %H:%M'))
        return schedule
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading schedule: {e}")
        return []

async def schedule_reminders(schedule, user):
    for entry in schedule:
        event_time = entry['datetime']
        now = datetime.now(tz=berlin_tz)
        reminder_time = event_time - timedelta(minutes=15)
        if now < reminder_time:
            wait_time = (reminder_time - now).total_seconds()
            print(f"Scheduling reminder for {event_time.strftime('%H:%M')} on {event_time.strftime('%d.%m.%Y')}, waiting {wait_time} seconds.")
            await asyncio.sleep(wait_time)
            # replace REMINDER_TEXT and REMINDER_TEXT2 with your text
            await user.send(f" REMINDER_TEXT {event_time.strftime('%H:%M')} REMINDER_TEXT2 {event_time.strftime('%d.%m.%Y')}.")
        else:
            print(f"Reminder time for {event_time.strftime('%H:%M')} on {event_time.strftime('%d.%m.%Y')} has already passed.")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    schedule = load_schedule()
    print(f"Loaded schedule: {schedule}") 
    if schedule:
        user = await client.fetch_user(USER_ID)
        await schedule_reminders(schedule, user)
    else:
        print("No schedule found please set it in the schedule.json file!")

client.run(TOKEN)
