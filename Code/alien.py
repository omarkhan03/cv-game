import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y,flipped):
        super().__init__()
        file_path = './Resources/' + color + '.png'
        self.image0 = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.image0, (20 / 1, 15 / 1))
        self.flipped = False
        if flipped:
            self.image = pygame.transform.flip(self.image, False, True)
            self.flipped = True
        self.rect = self.image.get_rect(topleft = (x,y))

        if color == 'red': self.value = 100
        elif color == 'green': self.value = 200
        elif color == 'yellow': self.value = 300

    def update(self,direction):
        self.rect.x += direction


class Extra(pygame.sprite.Sprite):
    def __init__(self,side,window_width, video_width, flipped):
        super().__init__()
        self.image0 = pygame.image.load('./Resources/extra.png').convert_alpha()
        self.image = pygame.transform.scale(self.image0, (20 / 1, 12 / 1))

        if side == 'right':
            x = window_width - 50
            self.speed = -3
        else:
            x = video_width
            self.speed = 3

        if flipped:
            self.image = pygame.transform.flip(self.image, False, True)
            self.flipped = True
            y = 670
        else:
            self.flipped = False
            y = 10

        self.rect = self.image.get_rect(topleft=(x,y))
        self.vw = video_width

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < self.vw:
            self.kill()
