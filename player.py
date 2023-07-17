import pygame
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, cwidth, speed, vwidth, screen, height):
        super().__init__()
        self.image0 = pygame.image.load('./Resources/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image0, (30 / 1, 15 / 1))
        self.rect = self.image.get_rect(midtop=pos)

        self.speed = speed
        self.max_x_constraint = cwidth + vwidth
        self.ready_to_shoot = True
        self.ready_to_flip = True
        self.laser_time = 0
        self.laser_cooldown = 300
        self.flip_time = 0
        self.flip_cooldown = 300

        self.lasers = pygame.sprite.Group()

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        self.vwidth = vwidth

        self.fingers = None
        self.img = None
        self.in_scope = False

        self.screen = screen
        self.flipped = False
        self.ww = cwidth + vwidth
        self.wh = height

    def constraint(self):
        if self.rect.left <= self.vwidth:
            self.rect.left = self.vwidth
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        if self.flipped:
            self.lasers.add(Laser(self.rect.center, 25, 700))
        else:
            self.lasers.add(Laser(self.rect.center, -25, self.rect.bottom))

    def flip(self):
        self.flipped = not self.flipped

    def read_fingers(self):
        _, img = self.cap.read()
        img = cv2.flip(img, 1)

        # Find hand and its landmarks
        self.hands, img = self.detector.findHands(img, flipType=False)
        self.img = img

        if self.hands:
            hand = self.hands[0]
            x, y, w, h = hand['bbox']
            x1 = x + w // 2
            x1 = np.clip(x1, 100, 1150)

            map = x1 - 100
            map = map * (self.max_x_constraint - self.vwidth)
            map = map // 1150
            self.rect.x = map + self.vwidth

            self.fingers = self.detector.fingersUp(hand)
            return True
        return False

    def get_input(self):
        if self.fingers[1] == 1 and self.ready_to_shoot:
            self.shoot_laser()
            self.ready_to_shoot = False
            self.laser_time = pygame.time.get_ticks()

        if self.fingers == [0,0,0,0,1] and self.ready_to_flip:
            self.flip()
            self.ready_to_flip = False
            self.flip_time = pygame.time.get_ticks()

    def recharge_shoot(self):
        if not self.ready_to_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown and self.fingers[1] != 1:
                self.ready_to_shoot = True

    def recharge_flip(self):
        if not self.ready_to_flip:
            current_time = pygame.time.get_ticks()
            if current_time - self.flip_time >= self.flip_cooldown and self.fingers != [0,0,0,0,1]:
                self.ready_to_flip = True

    def update(self):
        if self.read_fingers():
            self.in_scope = True

            if self.fingers[1] == 1:
                shoot1 = pygame.image.load("./Resources/shoot1.png").convert_alpha()
                shoot1 = pygame.transform.scale(shoot1,(self.ww / self.ww * 330, self.wh / self.wh * 90))
                self.screen.blit(shoot1, (5, 305))
            elif self.fingers == [0,0,0,0,1]:
                flip1 = pygame.image.load("./Resources/flip1.png").convert_alpha()
                flip1 = pygame.transform.scale(flip1,(self.ww / self.ww * 330, self.wh / self.wh * 90))
                self.screen.blit(flip1, (5, 400))
            else:
                move1 = pygame.image.load("./Resources/move1.png").convert_alpha()
                move1 = pygame.transform.scale(move1, (self.ww / self.ww * 330, self.wh / self.wh * 90))
                self.screen.blit(move1, (5, 210))

        else: self.in_scope = False

        try:
            self.constraint()
            self.lasers.update()
            self.get_input()
        except Exception as e: print(e)

        self.recharge_flip()
        self.recharge_shoot()

        if self.flipped:
            self.screen.blit(pygame.transform.flip(self.image, False, True), self.rect)
        else:
            self.screen.blit(self.image, self.rect)


    def get_image(self):
        return self.img