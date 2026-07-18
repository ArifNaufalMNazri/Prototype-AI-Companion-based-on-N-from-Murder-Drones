# Imports
import sys
import queue
import numpy as np
import sounddevice as sd
import NShared_state
import time
from moonshine_voice import(
  MicTranscriber, 
  TranscriptEventListener, 
  get_model_for_language,
)

class AudioWarningFilter:
    def __init__(self, original_stream):
        self.original_stream = original_stream

    def write(self, message):
        if "overflow" in message.lower():
            return
        self.original_stream.write(message)

    def flush(self):
        self.original_stream.flush()

sys.stderr = AudioWarningFilter(sys.stderr)

model_path, model_arch = get_model_for_language("en", 2)

class Listener(TranscriptEventListener):
  def on_line_completed(self, event):
    heard_text = event.line.text.strip()
    if heard_text and len(heard_text) > 1:
      NShared_state.TextQueue.put(heard_text)

      NShared_state.listening_status = "processing"


def start_listening():
  global listen_started
  mic = MicTranscriber(
     model_path = model_path,
     model_arch = model_arch,
    update_interval = 1.5
     )
  listener = Listener()

  mic.add_listener(listener)
  mic.start()
  listen_started = True
  time.sleep(2.0)
  



