import pygame, sys
from player import Player
import cv2
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser


class Game:
    def __init__(self):
        self.player_sprite = Player(((screen_width / 2), screen_height), screen_width, 5, video_width)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('./Resources/player.png').convert_alpha()
        self.live_x_start_pos = window_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('./Resources/Pixeled.ttf', 20)

        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=video_width + (screen_width/15), y_start=480)

        # alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1

        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241,79,80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        x_offset = x_offset + video_width
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: alien_sprite = Alien('yellow',x,y)
                elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y)
                else: alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= window_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= video_width:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,6,screen_height)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']),window_width, video_width))
            self.extra_spawn_time = randint(400,800)

    def collision_checks(self):

        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()

                # extra collisions
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()

        # alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf, score_rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.alien_lasers.update()
        self.extra_alien_timer()
        self.extra.update()
        self.collision_checks()
        self.display_lives()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()




if __name__ == '__main__':
    pygame.init()

    screen_width = 600
    screen_height = 600

    video_width = 213 * 1.7
    video_height = 120 * 1.7

    window_width = screen_width + video_width
    window_height = screen_height

    video_pos_x = 0
    video_pos_y = screen_height - video_height

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Gesture-Control Space Invaders")

    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)

    video_capture = cv2.VideoCapture(0)  # 0 represents the default camera
    video_capture.set(3, 1920)
    video_capture.set(4, 1080)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

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

        logo = pygame.image.load("./Resources/logo.png").convert_alpha()
        logo = pygame.transform.scale(logo, (window_width / window_width*400, window_height / window_height*100))
        screen.blit(logo, (-20, 0))

        game.run()
        pygame.display.flip()
        clock.tick(60)


#2-100