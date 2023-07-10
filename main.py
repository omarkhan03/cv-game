import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("Resources/Background.png")
imgGameOver = cv2.imread("Resources/gameOver.png")
imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [100, 100]
speedX = 15
speedY = 15
gameOver = False
score = [0,0]

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)
    # hands = detector.findHands(img, flipType=False, draw=False) - enable this instead if you don't want the squares

    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1//2
            y1 = np.clip(y1, 20, 470)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (50, y1))
                if 50 < ballPos[0] < 50+w1 and y1 < ballPos[1] < y1+h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1195-50 < ballPos[0] < 1195+w1 and y1 < ballPos[1] < y1+h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1

    # Game Over
    if ballPos[0] < 40 or ballPos[0] > 1200:
        gameOver = True

    if gameOver:
        img = imgGameOver
        cv2.putText(img,str(score[1]+score[0]),(585,360),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255), 5)
    else:
        # Move the ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Draw the ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        cv2.putText(img,str(score[0]),(300,650),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255), 5)
        cv2.putText(img,str(score[1]),(900,650),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255), 5)


    # Overlay the images
    result = cv2.addWeighted(imgBackground, 0.8, img, 0.5, 0.0)

    cv2.imshow("Image", result)
    key = cv2.waitKey(1)
    if key == ord('r'):
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread("Resources/gameOver.png")