# N (Murder Drones), Prototype AI Companion
I had just finished watching the youtube series <b>Murder Drones</b> a month and a half prior to this. After watching someone making an AI companion based on <b>BMO</b> from <b>Adventure Time</b>, I got inspired to make my own with N as my inspiration. 
<p align = "center">
<img src="./Media/N-TitleDisplayImage.jpg" width = 300 height = 400>
<img src="./Media/title_displayN.gif">
</p>
<p align = "center">
<i>N on left, video of AI on right</i>
</p>

I threaded and created the logic that allowed the different modules of the program to work with each other, but I leaned onto Gemini AI to help create some of the modules

## The process flow
I wanted this AI to do <b>2 things</b>:
- Be <b>voice activated</b>
- <b>Track my face</b>

Below is a process <b>flow chart</b> summarizing the loop the AI operates in

<img src="./Media/NProcessFlow.png" width = 100% height = 400>

## Face Tracking
### Face Mesh
I followed some youtube tutorial guides on creating a face tracking program for N. I used <b>opencv</b> and <b>mediapipe</b> for that module. 
<p align = "center">
  <img src = "./Media/OpenCV.png" width = 300 height = 300>
  <img src = "./Media/Mediapipe.jpeg" width = 300 height = 300>
</p>
I used the face-tracking software to track the <b>position of my nose</b> in the coordinate system of my webcam. 

(I don't have footage of me testing it because I used the altered the code to make the program, so here's an image of what it looked like)
<p align = "center">
  <img src = "./Media/FaceMesh.png" >
</p>

With this in place, I could now work in <b>translating those coordinates</b> onto a window using pygame to start the tracking
