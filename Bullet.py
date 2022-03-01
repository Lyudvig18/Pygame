import pygame
import os

class Bullet(pygame.sprite.Sprite):
    damage = 2000

    def __init__(self, width, height, screen, main_character, coor, left, *group):
        super().__init__(*group)

        self.screen_width = width
        self.screen_height = height
        self.screen = screen
        self.main_character = main_character
        self.left = left
        self.group = group

        self.damage = Bullet.damage 

        self.animCount = 0
        self.animations = []

        self.speed = 3

        self.image = pygame.image.load("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/PNG/Bullet/06/Arcane_Effect_1.png")
        self.rect = self.image.get_rect()
        self.rect.y = coor[1]

        if self.left:
            self.rect.x = coor[0]
        else:
            self.rect.x = coor[0] + 240

        for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/PNG/Bullet/04"):
            self.animations.append(pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/PNG/Bullet/04/{filename}"))


    def update(self):
        if self.left:
            self.rect = self.rect.move(-self.speed, 0)
        else:
            self.rect = self.rect.move(self.speed, 0)

        if self.rect.x < (0 - self.rect.width) or self.rect.x >= self.screen_width + self.rect.width:
            self.group[0].remove(self)

        self.animation()

    def animation(self):
        if self.animCount + 1 >= 70:
            self.animCount = 0

        self.image = self.animations[self.animCount // 10]
        self.animCount += 1

        