import discord
import asyncio
import json
from datetime import datetime, timedelta
import pytz

# Hier den tatsächlichen Token deines Discord-Bots einfügen
TOKEN = 'MTI0NzI3ODAwMjg3OTA3NDM3Ng.Gvj2zD.n9j8oOmejwCNe9dT1b4_qbPX3mkztUXlw-oR2E'

# Hier die tatsächliche Benutzer-ID einfügen, die benachrichtigt werden soll
USER_ID = 747927665729732708

# Zeitzone Berlin
berlin_tz = pytz.timezone('Europe/Berlin')

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

SCHEDULE_FILE = 'schedule.json'

def load_schedule():
    try:
        with open(SCHEDULE_FILE, 'r') as f:
            schedule = json.load(f)
        # Konvertiere Zeit-Strings zurück zu datetime-Objekten mit Zeitzone
        for entry in schedule:
            entry['datetime'] = berlin_tz.localize(datetime.strptime(entry['datetime'], '%Y-%m-%d %H:%M'))
        return schedule
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading schedule: {e}")  # Debug-Ausgabe
        return []

# Funktion zur Planung der Erinnerungen
async def schedule_reminders(schedule, user):
    for entry in schedule:
        event_time = entry['datetime']
        now = datetime.now(tz=berlin_tz)
        reminder_time = event_time - timedelta(minutes=15)
        if now < reminder_time:
            wait_time = (reminder_time - now).total_seconds()
            print(f"Scheduling reminder for {event_time.strftime('%H:%M')} on {event_time.strftime('%d.%m.%Y')}, waiting {wait_time} seconds.")  # Debug-Ausgabe
            await asyncio.sleep(wait_time)
            await user.send(f"Erinnerung: Du hast in 15 Minuten eine SkyBad schicht um {event_time.strftime('%H:%M')} am {event_time.strftime('%d.%m.%Y')}.")
        else:
            print(f"Reminder time for {event_time.strftime('%H:%M')} on {event_time.strftime('%d.%m.%Y')} has already passed.")  # Debug-Ausgabe

@client.event
async def on_ready():
    print(f'Logged in as {client.user} eingeloggt')
    schedule = load_schedule()
    print(f"Loaded schedule: {schedule}")  # Debug-Ausgabe
    if schedule:
        user = await client.fetch_user(USER_ID)
        await schedule_reminders(schedule, user)
    else:
        print("Kein Zeitplan gefunden. Warte auf Eingabe...")

client.run(TOKEN)
