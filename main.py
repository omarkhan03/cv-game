import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

import pygame, sys

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("Resources/Background (1).png")
imgGameOver = cv2.imread("Resources/gameOver.png")
imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/player.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

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
            x, y, w, h = hands[0]['bbox']
            h1, w1, _ = imgBat1.shape
            x1 = x + 20
            x1 = np.clip(x1, 20, 1200)

            img = cvzone.overlayPNG(img, imgBat1, (x1, 500))

    # Overlay the images
    result = cv2.addWeighted(imgBackground, 3, img, 1, 0.0)

    cv2.imshow("Image", result)
    key = cv2.waitKey(1)
    if key == ord('r'):
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread("Resources/gameOver.png")

# if __name__ == '__main__':
#     pygame.init()
#     screen_width = 600
#     screen_height = 600
#     screen = pygame.display.set_mode((screen_width, screen_height))
#     clock = pygame.time.Clock()
#
#     while True:
#         for event in pygame.event.get():