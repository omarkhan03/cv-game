# Gesture-Controlled Arcade Game

## Table of contents

- [Description](#description)
- [Video Demonstration](#video-demonstration)
- [How to install and run](#how-to-install-and-run)
- [Credits](#credits)

# Description

A gesture-controlled arcade game written in Python using OpenCV and PyGame. I made this to experiment with computer vision and to learn OpenCV in a fun way.
The main idea is that the player is able to make hand-gestures to control a spaceship and defeat enemies. The three hand-gesture inputs are:
- Moving the spaceship around (simply move your hand around horizontally)
- Shooting a bullet (point with index finger)
- Flipping over the ship to target enemies on the other side (raise your thumb and pinkie finger)

On the left side of the window is the UI, which displays a video feed taken from your computer's camera.  There are indicators for which hand gesture the player is currently making (overlayed on top of and above the video feed). It also contains information such as points and health. On the right side of the window is the actual game, which is essentially space invaders except the ship can flip around and shoot in two directions. There is only one level.

<br>

# [Video Demonstration](https://youtu.be/2USyuYQyp-k)

https://github.com/omarkhan03/cv-game/assets/106503860/39e8bc5a-315d-4bee-bc65-dedbac63dc76

*Turn on sound!*

[Link to YouTube video.](https://youtu.be/2USyuYQyp-k)

<br>

# How to install and run
*The instructions below assume a Unix-like environment.*

1. If you don't have Python3 already installed on your system, install it from https://www.python.org/downloads/. Ensure you have the latest version of pip installed by following the instructions on https://pip.pypa.io/en/latest/installation/#ensurepip.  

2. Clone the repository
    ```sh
      git clone https://github.com/your_username_/Project-Name.git
    ```
3. CD into the Code directory
     ```sh
       cd Code
     ```
4. Install all requirements
    ```sh
     pip install -r requirements.txt
    ```
5. Run main.py
    ```sh
     python3 main.py
    ```

<br>

# Credits
- Thanks to [Murtaza's workshop](https://www.youtube.com/@murtazasworkshop)'s videos for helping to learn OpenCV as well as the CvZone library, from which I used the hand tracking module.

- I built off of [this PyGame tutorial](https://www.youtube.com/watch?v=o-6pADy5Mdg) by Clear Code on YouTube. Thanks a lot!
