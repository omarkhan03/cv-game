import pygame
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('./Resources/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        print('shoot laser')

    def get_input(self):
        _, img = self.cap.read()
        img = cv2.flip(img, 1)

        # Find hand and its landmarks
        hands, img = self.detector.findHands(img, flipType=False)
        # hands = detector.findHands(img, flipType=False, draw=False)

        if hands:
            x, y, w, h = hands[0]['bbox']
            # h1, w1, _ = imgBat1.shape
            x1 = x + w//2
            x1 = np.clip(x1, 100, 1150)
            print(x1)

            map = x1 - 100
            map = map * self.max_x_constraint
            map = map // 1150

            # if x1 < 400:
            #     self.rect.x -= self.speed
            # elif x1 > 800:
            #     self.rect.x += self.speed
            keys = pygame.key.get_pressed()

            self.rect.x = map

            if keys[pygame.K_SPACE]:
                self.shoot_laser()

        cv2.imshow("Image", img)

    def update(self):
        self.get_input()
        self.constraint()





