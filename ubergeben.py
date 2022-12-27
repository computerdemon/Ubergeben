import discord
import asyncio
import time
import json
import string
import time
import threading
import wave
import traceback
import config

from discord.ext import commands

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    """)
    import sys
    sys.exit(1)

# DISCORD variables
TOKEN = config.TOKEN
CHANNEL_ID = config.CHANNEL

# AZURE variables
speech_key = config.speech_key
service_region = config.region

# Set up the Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

stop_flag = False

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_message(message):
    if message.content.startswith("!speech"):
        # Get the channel where the command was sent
        channel = message.channel
        # Create a task to run the speech recognition in the background
        print('Received !speech command')
        evt = speechsdk.SessionEventArgs
        await speech(channel, evt)
    elif message.content.startswith("!stop"):
        global stop_flag
        stop_flag = True

async def speech(channel: discord.TextChannel, evt: speechsdk.SessionEventArgs):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    async def recognized_cb(evt: speechsdk.SessionEventArgs):
        text = evt.result.text
        await channel.send("Recognized: {}".format(text))

    def stop_cb(evt: speechsdk.SessionEventArgs):
        speech_recognizer.stop_continuous_recognition_async()

    speech_recognizer.recognized.connect(lambda evt: asyncio.run_coroutine_threadsafe(recognized_cb(evt), client.loop))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    result_future = speech_recognizer.start_continuous_recognition_async()
    print('Continuous Recognition is now running, say something.')

    try:
        recognizing_output = await asyncio.wait_for(recognized_cb(evt), timeout=None)
        recognized_output = await asyncio.wait_for(recognized_cb(evt), timeout=None)
        print(recognizing_output)
        print(recognized_output)
    except TypeError as e:
        print("Error occurred:", e)
    except asyncio.TimeoutError:
        print("Timed out waiting for recognition")
        tb = traceback.format_exc()
        print(tb)
    except Exception as e:
        print("Error occurred:", e)

client.run(TOKEN)
