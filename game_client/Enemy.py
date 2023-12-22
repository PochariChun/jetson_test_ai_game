import pygame
import os

WIDTH = 640
HEIGHT = 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        player_img = pygame.image.load(os.path.join(img_folder, '章魚哥.png')).convert()
        player_img = pygame.transform.scale(player_img, (90, 90))
        self.image = player_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

        self.move_direction = 2
        self.move_counter = 0

        self.health = 100  # 初始血量

    #開射

        self.shoot_delay = 1000  # 射击间隔（毫秒）
        self.last_shot = pygame.time.get_ticks()  # 上次射击的时间

    def shoot(self, bullets_group):
        """ 敌人射击方法 """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            bullet = Bullet(self.rect.centerx, self.rect.bottom)
            bullets_group.add(bullet)
            self.last_shot = current_time

    # 敵人生命值
    def draw_health_bar(self,surface, x, y, pct):

        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, GREEN, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)
            

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 100:
            self.move_direction *= -1
            self.move_counter *= -1
    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        bullet_img = pygame.image.load(os.path.join(img_folder, '雪花.png')).convert_alpha()  # 加载图像       
        bullet_img = pygame.transform.scale(bullet_img, (20, 20))
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y-30))

    def update(self):
        self.rect.y += 3  # 子弹速度

    