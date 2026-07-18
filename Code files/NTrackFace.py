# Imports
import asyncio 
import NShared_state
import cv2 
import sys
import pygame  
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
#--------Functions--------
# Setup face-tracking settings
def setup():
  # Setup
  #Load face_landmarker.task 
  baseOptions = python.BaseOptions(model_asset_path="face_landmarker.task")
  options = vision.FaceLandmarkerOptions(
  base_options = baseOptions,
  output_face_blendshapes=False,                #}
  output_facial_transformation_matrixes=False,  #} Turned off to keep program running fast
  num_faces=1, # Ignore background. Focus on user. 
  )

  #Object to find face. Uses vision model and options configuration.
  detector = vision.FaceLandmarker.create_from_options(options)

  cap = cv2.VideoCapture(0) # Connect to webcam. 0 to get webcam

  return detector, cap
# Search for nose position in screen
def findFace(detector, cap): 
  while True:
    success, frame = cap.read() # Takes snapshow from webcam. 
                              # success: Boolean to see if camera working
                              # frame: Pixel array grid    
    in_frame = True
    frame = cv2.flip(frame, 1) # Flip pixels for mirror effect 
    h, w, _ = frame.shape # Gets height(h) and widht(w) of camera. _ is colour depth
 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)# Changes pixels in image from BGR to RGB
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame) # Convert python array to Mediapipe container

    detection_result = detector.detect(mp_image)# Find landmarks and stores them

    if detection_result.face_landmarks and len(detection_result.face_landmarks)>0: # Checks if face detected
      face_landmarks = detection_result.face_landmarks[0] # Takes tracking coordinates from camera
      Nose = face_landmarks[1]
    else :
      in_frame = False
      return 5, 5, in_frame
    
    return int(Nose.x*720), int(Nose.y*720), in_frame

def background_tracker(detector, cap):
  import queue
  try:
    while True: 
      Nosepixel_x, Nosepixel_y, in_frame = findFace(detector, cap)
      while not NShared_state.CoordQueue.empty():
        try:
          NShared_state.CoordQueue.get_nowait()
        except queue.empty():
          break
      NShared_state.CoordQueue.put((Nosepixel_x, Nosepixel_y, in_frame))
  except (RuntimeError, ValueError, KeyboardInterrupt):
    print("That was a nice chat. See you again next time!")

