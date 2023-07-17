import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_path = './Resources/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        if color == 'red': self.value = 100
        elif color == 'green': self.value = 200
        elif color == 'yellow': self.value = 300

    def update(self,direction):
        self.rect.x += direction*2


class Extra(pygame.sprite.Sprite):
    def __init__(self,side,window_width, video_width):
        super().__init__()
        self.image = pygame.image.load('./Resources/extra.png').convert_alpha()

        if side == 'right':
            x = window_width - 50
            self.speed = -3
        else:
            x = video_width+1
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x,80))
        self.vw = video_width

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < self.vw:
            print('yo!')
            self.kill()

