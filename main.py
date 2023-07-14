import pygame, sys
from player import Player
import cv2

class Game:
    def __init__(self):
        self.player_sprite = Player(((screen_width / 2), screen_height), screen_width, 5, video_width)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

    def run(self):
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)


if __name__ == '__main__':
    pygame.init()

    screen_width = 600
    screen_height = 600

    video_width = 213 * 1.5
    video_height = 120 * 1.5

    window_width = screen_width + video_width
    window_height = screen_height

    video_pos_x = 0
    video_pos_y = screen_height - video_height

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Gesture-Control Space Invaders")
    clock = pygame.time.Clock()
    game = Game()

    video_capture = cv2.VideoCapture(0)  # 0 represents the default camera
    video_capture.set(3, 1920)
    video_capture.set(4, 1080)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Convert the frame from BGR to RGB for PyGame
        img = game.player_sprite.img
        img = cv2.flip(img, 1)

        try:
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate the frame
            # frame_rgb = cv2.rotate(frame_rgb, cv2)  # Rotate the frame
            frame_rgb = pygame.surfarray.make_surface(frame_rgb)

            # Scale the video frame to fit the specified dimensions
            frame_scaled = pygame.transform.scale(frame_rgb, (video_width, video_height))

            # Clear the PyGame window and blit the video frame
            screen.fill((0, 0, 0))
            screen.fill((50, 50, 50), (0, 0, video_width, screen.get_height()))
            screen.blit(frame_scaled, (video_pos_x, video_pos_y))
        except:
            print("First game loop (image not initialized)")

        game.run()
        pygame.display.flip()
        clock.tick(60)

