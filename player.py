import pygame
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, cwidth, speed, vwidth):
        super().__init__()
        self.image = pygame.image.load('./Resources/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = cwidth + vwidth
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 200

        self.lasers = pygame.sprite.Group()

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        self.vwidth = vwidth

        self.img = None

    def constraint(self):
        if self.rect.left <= self.vwidth:
            self.rect.left = self.vwidth
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        print('shoot laser')
        self.lasers.add(Laser(self.rect.center, -25, self.rect.bottom))

    def get_input(self):
        _, img = self.cap.read()
        img = cv2.flip(img, 1)

        # Find hand and its landmarks
        hands, img = self.detector.findHands(img, flipType=False)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            x1 = x + w//2
            x1 = np.clip(x1, 100, 1150)

            map = x1 - 100
            map = map * (self.max_x_constraint - self.vwidth)
            map = map // 1150
            self.rect.x = map + self.vwidth

            fingers = self.detector.fingersUp(hand)
            if fingers[1] == 1 and self.ready:
                self.shoot_laser()
                self.ready = False
                self.laser_time = pygame.time.get_ticks()

        self.img = img
        # cv2.imshow("Image", img)

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()

    def get_image(self):
        return self.img
