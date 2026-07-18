import pygame
import io
import requests
import os
import base64

speak_key = "QnpZN3ZXc0JkRW4xSU91c2dzc3FyTXBvRThjMHBPMTM6akVjZV9HeXZOb1NjX1loeW9YcFAwUA=="
voice_id = "community-ze9cithzjnsj"
Temp_audio_path = "temp_speech.mp3"

pygame.mixer.init()

def speak_setup(speak_text):
  if not speak_text:
    return
  try: 
    response = requests.post(
      "https://api.inworld.ai/tts/v1/voice",
      headers = {
        "Authorization": f"Basic {speak_key}",
        "Content-Type": "application/json"
      },
      json = {
        "text": speak_text,
        "voiceId": voice_id,
        "modelId": "inworld-tts-1.5-max",
        "audioConfig": {
          "audioEncoding": "MP3",
          "sampleRateHertz": 24000
        }
      },
      timeout = 15
    )

    response.raise_for_status()

    audio_bytes = base64.b64decode(response.json()["audioContent"])

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    with open(Temp_audio_path, "wb") as f:
      f.write(audio_bytes)

    pygame.mixer.music.load(Temp_audio_path)
    pygame.mixer.music.play()

  except Exception as e:
    print(f"[Error in speaking]: {e}")
def play_pregenerated_speech(file_path):
  try:
    if not pygame.mixer.music.get_busy():
      pygame.mixer.music.load(file_path)
      pygame.mixer.music.play()
  except Exception as e:
    print(f"Error in speaking pregenerated: {e}")
