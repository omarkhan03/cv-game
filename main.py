import pygame, sys
from player import Player
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

class Game:
    def __init__(self):
        self.player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

    def run(self):
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        # Update all sprite groups
        # Run all sprite groups


if __name__ == '__main__':
    pygame.init()

    screen_width = 600
    screen_height = 600

    video_width = 213
    video_height = 120

    video_pos_x = 0
    video_pos_y = screen_height - video_height

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    #
    video_capture = cv2.VideoCapture(0)  # 0 represents the default camera
    video_capture.set(3, 1920)
    video_capture.set(4, 1080)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        # # Capture video frame from the camera
        # ret, frame = video_capture.read()

        # # Find hand and its landmarks
        # detector = HandDetector(detectionCon=0.8, maxHands=1)
        # hands, frame = detector.findHands(frame, flipType=False)

        # if hands:
        #     hand = hands[0]
        #     x, y, w, h = hand['bbox']


        # Convert the frame from BGR to RGB for PyGame
        img = game.player_sprite.img

        try:
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate the frame
            frame_rgb = pygame.surfarray.make_surface(frame_rgb)

            # Scale the video frame to fit the specified dimensions
            frame_scaled = pygame.transform.scale(frame_rgb, (video_width, video_height))

            # Clear the PyGame window and blit the video frame
            screen.fill((30, 30, 30))
            screen.blit(frame_scaled, (video_pos_x, video_pos_y))
        except:
            print("First game loop (image not initialized)")


        # Update the PyGame display
        # pygame.display.update()

        game.run()
        pygame.display.flip()
        clock.tick(60)

