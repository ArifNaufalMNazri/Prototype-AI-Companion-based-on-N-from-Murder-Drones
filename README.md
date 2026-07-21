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

### The window
I used pygame to create a window to display the eyes on screen, and also to update its position based on the position of my nose on the webcam. 
<p align = "center">
  <img src = "./Media/PygameImage.png" >
</p>

After returning the coordinates of my nose from the <b>webcam</b>, I used an algorithm to convert that into the dimensions of the pygame window using <b>ratios</b>. I <b>dynamically updated</b> the position of the eyes to match the movement of my nose, and moved it at <b>60 fps</b> for smooth animation.
<p align = "center">
  <img src = "./Media/WebCamImage.jpg" height = 300 width = 500>
  <img src = "./Media/NEyesImage.jpg" height = 300 width = 500>
</p>
With that out of the way, face tracking was <b>completed</b>.

## Listening
After doing some research, I decided to use **Moonshine** as the **speech-to-text** model. I cycled through different versions of the model to accomodate for the processing power of my laptop, until I finally implemented a suitable one. 
<p align = "center">
  <img src = "./Media/MoonshineImage.png">
</p>

I connected my earbuds to my laptop and used its **microphone** to run some tests, to which it returned my speech acceptably. There's still some problems with it, but I think it is mainly to do with my microphone, which is a problem I will delve more into later.

<p align = "center">
  <img src = "./Media/SpeechDetectionImage.png">
</p>
<p align = "center">
  <i>At the time, the microphone picked up a background conversation</i>
</p>

With the listening completed, I was halfway through the project. Now, onto **processing**.

## Processing
At first, I chose **ollama** to be the ai model to handle my questions. However, when I tried to load it onto my computer together with my program, it crashed my program with how big it was. No amount of threading or model de-scaling helped that. 
<p align = "center">
  <img src = "./Media/OllamaImage.png">
  <img src = "./Media/XImage.jpeg" height = 200 width = 200>
</p>

So, I had to pivot. I decided to use google's **gen ai** as the ai, as it would not require any processing power from my laptop. Instead, the processsing would be done in **servers** on google's system. However, I only have a **limited number of requests** I can make, which is another problem I want to address later. 
<p align = "center">
  <img src = "./Media/GoogleGenAIImage.png" height = 300 width = 300>
  <img src = "./Media/TickImage.png" height = 300 width = 300>
</p>

After designing the 'Brain' of N and directing my speech prompts to the ai, I finally had a responsive program that answered my questions, albeit in text form.
<p align = "center">
  <img src = "./Media/NResponseImage.png" width = 100%>
</p>

*Disclaimer: I might've ran out of tokens for the google gen ai from testing. My previous tests showed it responded properly.*

*Disclaimer 2: My microhpone quality was pretty bad. Instead of 'What's the mass of the sun', it detected 'is the math of son'.*

With processing completed, there was only one thing left to do: **Text-To-Speech**
