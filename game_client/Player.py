import pygame
import os

WIDTH = 640
HEIGHT = 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        player_img = pygame.image.load(os.path.join(img_folder, 'Player.png')).convert()
        player_img = pygame.transform.scale(player_img, (78, 100))
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 50)

        self.health = 100  # 初始血量


    def move_left(self):
        self.rect.x -= 5
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self):
        self.rect.x += 5
        if self.rect.x > WIDTH - 50:
            self.rect.x = WIDTH - 50

    def get_position(self):
        return self.rect.x + 25, self.rect.y

    def update(self):
        pass
        # self.rect.x += 5
        # if self.rect.left > WIDTH:
        #     self.rect.right = 0

    #偵測有無碰撞
    def collider(self, bullet):
        return self.rect.colliderect(bullet.rect)
    

    def draw_health_bar(self,surface, x, y, pct):

        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, RED, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)



