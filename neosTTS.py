# Don't forget your packages!!
from gtts import gTTS
import json
import os
import asyncio
import websockets
import pyperclip
import subprocess

# Websocket runs on port 7000 by default
print("")
print("NeosTTS (Text To Speech) by dfgHiatus.")
print("")
print("When audio is generated, you'll see a message that is was and where it's stored.")
print("As long as this window stays open, this should run with no issues.")
print("KNOWN ISSUES: Bad queries can cause this to crash, *you have been warned.*")
print("")
print("[Info] Websocket created on port 7000.")
print("")
socketString = "Generated Audio"

# The meat and potatoes
async def facetrack(websocket, path):
    async for message in websocket:
        socketString = "Generated Audio"

        # message = '{"text": "hello", "language": "en", "slow": "false", "dialect": "com"}'

        # Convert websocket message to usable data
        data = json.loads(message)
        data = json.loads(message)
           
        # Isolate The text to synthesize
        text = data['text']
         
        # Isolate The language to synthesize
        language = data['language']
         
        # Isolate The speed
        speed = data['slow']
         
        # Isolate dialect
        dialect = data['dialect']

        # Remove old audio
        try:
            os.remove("audio.wav") 
        except OSError:
            pass
        
        # Initialize tts, create mp3 and play. Params??
        tts = gTTS(text, lang=language, slow=speed, tld=dialect)
        tts.save('audio.mp3')
        
        subprocess.call(['ffmpeg', '-i', 'audio.mp3',
                           'audio.wav'])

        # Get Path of Generated Audio File, and set to clipboard. In Neos we can auto-paste and clear
        audioPath = os.getcwd()
        print("")
        print("")
        print("")
        print('Audio creation sucessful!')
        print(audioPath + '\\' + 'audio.wav')
        print("")
        print("")
        print("")

        pyperclip.copy(audioPath + '\\' + 'audio.wav')
        
        socketString = 'Generated ' + text + ' at ' + audioPath + '\\' + 'audio.wav' 
        
        await websocket.send(socketString)

# Pushes string to port 7000
asyncio.get_event_loop().run_until_complete(
    websockets.serve(facetrack, 'localhost', 7000))
asyncio.get_event_loop().run_forever()
