# <---Summary of project--->
# This project aims to teach me about using AI in my programs
# Gemini AI helped create some of the modules like NBrain and NListen
# I synthesised the modules into a working program
# This AI is based off of N from the youtube series Murder Drones
# Used Inworld.com to generate voices. Did not want to steal voice actor's voice

#<---Imports--->
# Built-in modules
from threading import Thread
from random import randint
# Self-made modules
import NFace
import NTrackFace
import NListen
import NShared_state
import NBrain
import NSpeak

#<---Functions--->

def play_preset_messages(message_path_list):
  message_index = randint(1, len(message_path_list)) - 1
 
  NSpeak.play_pregenerated_speech(message_path_list[message_index])

def ai_activated(prompt):
  return "Hello" in prompt or "Hey" in prompt

def ai_reply(activation_messages_list):
  global heard_text, reply_ready, not_hello
  while True:
    if heard_text: 
      if ai_activated(heard_text):
        not_hello = False
        play_preset_messages(activation_messages_list)
        reply_ready = True
        heard_text = ""
      
      if reply_ready and heard_text:
        if not ai_activated(heard_text) and not not_hello:
          N_reply = NBrain.think(heard_text)
          heard_text = ""

          print(f"[I'll say]: {N_reply}")
          NSpeak.speak_setup(N_reply)
          
          not_hello = True
          reply_ready = False
        else:
          play_preset_messages(retry_messages)

def face_return_to_screen():
  return face_in_frame and not last_in_frame

#<---Global Variables--->
window_width = 350
window_height= 210

Nosepixel_x = 0
Nosepixel_y = 0

face_in_frame = False
last_in_frame = False

respond = False
response_timer = 0

reply_ready = False

not_hello = True

processing_timer = 0

running_window = True

heard_text = ""
N_reply = ""# Store ai reply

processing = False
last_processing = False

# AI preset messages(Generated with Inworld)
activation_messages = ["Voices/ImAllEars.mp3","Voices/Hello.mp3","Voices/ImListening.mp3"]
return_messages = ["Voices/NiceToSeeYouAgain.mp3", "Voices/HowAreYouDoing.mp3", "Voices/HiThere.mp3"]
processing_messages = ["Voices/LetMeThink.mp3", "Voices/LetMeThink.mp3", "Voices/Processing.mp3"]
start_messages = ["Voices/start_listening_1.mp3", "Voices/start_listening_2.mp3", "Voices/start_listening_3.mp3"]
end_messages = ["Voices/Byebye.mp3", "Voices/Seeyouagain.mp3", "Voices/Thatwasanicechat.mp3"]
retry_messages=["Voices/try_again_1.mp3", "Voices/try_again_2.mp3"]


#<------------Setup------------>

# Window
screen, display_surface, clock = NFace.window_setup(window_width, window_height)
#-------Loading faces-------

# Setup face tracking
detector, cap = NTrackFace.setup()

# Eye image for tracking
NEye, NEye_width, NEye_height = NFace.image_setup("Faces/Neyes.png", 222, 140)#Setup Eye Image
position_x, position_y, center_x, center_y = NFace.get_center(window_width, window_height, NEye_width, NEye_height, True)

# Warning image for face not detected
WarningSign_NoFace, Warning_width, Warning_height = NFace.image_setup("Faces/WarningSign(NoFace).png", 140, 140)
Warning_CenterX, Warning_CenterY= NFace.get_center(window_width, window_height, Warning_width, Warning_height, False) 

# Loading face
NLoading, NLoading_width, NLoading_height = NFace.image_setup("Faces/NLoading.png", 137, 200)
NLoading_CenterX, NLoading_CenterY = NFace.get_center(window_width, window_height, NLoading_width, NLoading_height, False)

# Response face
NResponse, NResponse_width, NResponse_height = NFace.image_setup("Faces/NResponse.png", 200, 207)
NResponse_CenterX, NResponse_CenterY = NFace.get_center(window_width, window_height, NResponse_width, NResponse_height, False)

#<---Threading--->
listening_thread = Thread(target=NListen.start_listening, daemon=True)
listening_thread.start()

tracking_thread = Thread(target= NTrackFace.background_tracker, args=(detector, cap), daemon=True)
tracking_thread.start()

ai_reply_thread = Thread(target = ai_reply, args=(activation_messages,), daemon=True)
ai_reply_thread.start()


play_preset_messages(start_messages)

#<-------Main Loop------->
while True: 
  processing = False
  if not NShared_state.TextQueue.empty(): # Get user prompt from queue
    heard_text = NShared_state.TextQueue.get()
    print(f"[I heard]: {heard_text}")
    NShared_state.listening_status = "processing"

    processing_timer = 60

  if processing_timer > 0: # Sets timer for processing state
    processing_timer -= 1

    if processing_timer == 0:
      NShared_state.listening_status = "listening"
      respond = True
      response_timer = 20


  if not NShared_state.CoordQueue.empty(): # Get user nose coordinates
    Nosepixel_x, Nosepixel_y, face_in_frame = NShared_state.CoordQueue.get()

  if not face_in_frame : # Display face-not-detected face
    NFace.render_N(Warning_CenterX, Warning_CenterY, screen, display_surface, WarningSign_NoFace, clock)
    last_in_frame = face_in_frame
    continue 

  if face_return_to_screen():
    play_preset_messages(return_messages)
      
  if NShared_state.listening_status == "processing" and not ai_activated(heard_text):
    processing = True
    if processing and not last_processing:
      play_preset_messages(processing_messages)

    NFace.render_N(NLoading_CenterX, NLoading_CenterY, screen, display_surface, NLoading, clock)
    last_processing = processing 
    continue

  processing = False
  if respond and response_timer > 0: 
    response_timer -=1
    NFace.render_N(NResponse_CenterX, NResponse_CenterY, screen, display_surface, NResponse, clock)
  else:
    respond = False # Renders tracking face if user already answered
    position_x, position_y, center_x, center_y = NFace.get_new_position(window_width, window_height, center_x, center_y, Nosepixel_x, Nosepixel_y, position_x, position_y)
    NFace.render_N(position_x, position_y, screen, display_surface, NEye, clock)

  last_in_frame = face_in_frame
  last_processing = processing
