# Imports
import pygame 
import sys
import NTrackFace
from cv2 import destroyAllWindows
#-------Functions-------
# Find center position of image
def get_center(width, height, image_width, image_height, Flag):
  pygame.init()
   
  screen_width = width
  screen_height = height

  position_x = (screen_width-image_width)/2
  position_y = (screen_height - image_height)/2
  center_x = width/2
  center_y = height/2
  
  if Flag:
    return position_x, position_y, center_x, center_y
  else: 
    return position_x, position_y

# Window setup function
def window_setup(width, height):
  screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.SCALED, vsync=1)# Creates screen
  pygame.display.set_caption("N")

  display_surface = pygame.Surface((width, height))# Creates surface to display other images
  display_surface.fill("Black")

  clock = pygame.time.Clock()
  
  return screen, display_surface, clock
# Image setup
def image_setup(filepath, width, height):
  image = pygame.image.load(filepath).convert_alpha()

  return image, width, height
# Eye tracking face function
def get_new_position(width, height, center_x, center_y, target_x, target_y, position_x, position_y):
  # Gets new position vector
  translate_x = (target_x/720)*width
  translate_y = (target_y/720)*height
  # Determine tracking speed
  Factor = 7.5
  v_x = (translate_x - center_x)/Factor
  v_y = (translate_y - center_y)/Factor
  # Variable to store next position of eye
  Check_x = position_x + v_x 
  Check_y = position_y + v_y 
  # 1. Checks if current eye center is equal to nose position
  # 2. Checks is image position is out of bounds of screen
  if (center_x < translate_x or center_x > translate_x) and (Check_x > 2 and Check_x + 222 <  width - 2):
    # Updates x-position
    position_x += v_x 
    center_x += v_x  
  else: 
    # Blocks image from going off-screen
    if Check_x < 2:
      position_x += 0.1
    if Check_x + 222 > width - 2:
      position_x -= 0.1
  if (center_y < translate_y or center_y > translate_y) and (Check_y > 2 and Check_y + 140 < height - 2):
    # Updates y-position
    position_y += v_y 
    center_y += v_y 
  else: 
    if Check_y < 2:
      position_y += 0.1
    if Check_y + 140 > height - 2:
      position_y -= 0.1

  return position_x, position_y, center_x, center_y
# Rendering image function
def render_N(center_x, center_y, screen, display_surface, image, clock):
  # Checks if window has been closed
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      destroyAllWindows()
      exit()

  # Displays image on screen
  screen.fill("Black")
  screen.blit(display_surface, (0,0))
  screen.blit(image, (center_x, center_y))
  # Updates screen for new positions
  pygame.display.update()
  # Set to 60 fps
  clock.tick(60)
