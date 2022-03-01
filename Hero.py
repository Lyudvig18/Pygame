import pygame
import Bullet
import os

class Main_character(pygame.sprite.Sprite):
    image_flip = pygame.image.load("Image_gg/PNG/wizard.png")
    image = pygame.transform.flip(image_flip, 1, 0)

    coin = pygame.image.load("Coin1.png")

    def __init__(self, width, height, screen, monstr, *group):
        super().__init__(*group)

        self.image = Main_character.image

        self.group = group[0]

        self.up_costs = {
            1 : 100,
            2 : 100
        }

        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - (self.rect.width // 2)
        self.rect.y =  height - self.rect.height - 80
        self.rect_width = self.rect.width

        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.speed = 7

        self.move_right = False
        self.move_left = False
        self.balance = 0

        self.animCount = 0
        self.animCount_attack = 0
        self.animCount_die = 0

        self.attack = False

        self.max_hp = 100
        self.health = self.max_hp

        self.die = False

        self.last_move_left = False

        self.animation_for_left = []
        self.animation_for_right = []

        self.animation_for_left_attack = []
        self.animation_for_right_attack = []

        self.animation_for_left_die = []
        self.animation_for_right_die = []

        self.monstr_groups = monstr

        self.left_stop = 0
        self.right_stop = self.screen_width

        for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/PNG/walk"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/PNG/walk/{filename}")
            image = pygame.transform.scale(image, (210, 200))
            self.animation_for_left.append(pygame.transform.flip(image, 1, 0))
            self.animation_for_right.append(image)

        for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/PNG/Attack"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/PNG/Attack/{filename}")
            image = pygame.transform.scale(image, (210, 200))
            self.animation_for_left_attack.append(pygame.transform.flip(image, 1, 0))
            self.animation_for_right_attack.append(image)

        for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/PNG/Die"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/PNG/Die/{filename}")
            image = pygame.transform.scale(image, (210, 200))
            self.animation_for_left_die.append(pygame.transform.flip(image, 1, 0))
            self.animation_for_right_die.append(image)

        self.isjump = False
        self.jumpCount = 10

        self.bullet_group = pygame.sprite.Group()

    def update(self, keys, events):
        if keys[pygame.K_UP] and events.type == pygame.KEYDOWN:
            self.attack = True
        elif events.type == pygame.KEYUP and self.attack:
            self.attack = False

        if keys[pygame.K_RIGHT]:
            if self.rect.x + self.rect.width <= self.right_stop:
                self.rect = self.rect.move(self.speed, 0)
                self.image = Main_character.image_flip

                self.move_right = True
                self.move_left = False
                self.last_move_left = False
                self.attack = False

        elif keys[pygame.K_LEFT]:
            if self.rect.x >= self.left_stop:
                self.rect = self.rect.move(-self.speed, 0)
                self.image = Main_character.image

                self.move_left = True
                self.move_right = False
                self.last_move_left = True
                self.attack = False
        else:
            self.move_right = False
            self.move_left = False

        if keys[pygame.K_SPACE] and not(self.isjump):
            self.isjump = True
        
        colls_with_monstr = pygame.sprite.spritecollide(self, self.monstr_groups, False)
        if colls_with_monstr and len(colls_with_monstr) != 0:
            for i in colls_with_monstr:
                if i.rect.x >= self.rect.x:
                    self.right_stop = i.rect.x
                    self.left_stop = 0 
                elif i.rect.x <= self.rect.x:
                    self.left_stop = i.rect.x + i.rect.width
                    self.right_stop = self.screen_width

        else:
            self.left_stop = 0
            self.right_stop = self.screen_width

        if self.die:
            self.animation_died()
        else:
            self.jump()
            self.animation()
            self.health_bar()
            self.balanced()

    def jump(self):
        if self.isjump:
            if self.jumpCount >= -10:
                if self.jumpCount < 0:
                    self.rect.y += (self.jumpCount ** 2) / 2
                else:
                    self.rect.y -= (self.jumpCount ** 2) / 2

                self.jumpCount -= 1

            else:
                self.isjump = False
                self.jumpCount = 10
                self.rect.y = self.screen_height - self.rect.height - 80

    def animation(self):
        if self.attack and self.animCount_attack == 39:
            self.create_bullet()

        if self.animCount + 1 >= 40:
            self.animCount = 0

        if self.animCount_attack + 1 >= 40:
            self.animCount_attack = 0

        if self.move_left:
            self.image = self.animation_for_left[self.animCount // 8]
            self.animCount += 1

        elif self.move_right:
            self.image = self.animation_for_right[self.animCount // 8]
            self.animCount += 1

        else:
            if self.last_move_left:
                self.image = Main_character.image
            else:
                self.image = Main_character.image_flip

        if self.attack and self.last_move_left:
            self.image = self.animation_for_left_attack[self.animCount_attack // 10]
            self.animCount_attack += 1
        elif self.attack and not(self.last_move_left):
            self.image = self.animation_for_right_attack[self.animCount_attack // 10]
            self.animCount_attack += 1

        if self.attack and self.animCount_attack == 40:
            self.create_bullet()

    def health_bar(self):
        images = []
        for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/health"):
            images.append(pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_gg/health/{filename}"))

        if self.health == self.max_hp:
            self.screen.blit(images[0], (self.screen_width - images[0].get_rect().width, 0))
        elif self.health == self.max_hp * 0.8:
            self.screen.blit(images[1], (self.screen_width - images[1].get_rect().width, 0))
        elif self.health == self.max_hp * 0.6:
            self.screen.blit(images[3], (self.screen_width - images[3].get_rect().width, 0))
        elif self.health == self.max_hp * 0.4: 
            self.screen.blit(images[4], (self.screen_width - images[4].get_rect().width, 5))
        elif self.health == self.max_hp * 0.2:
            self.screen.blit(images[2], (self.screen_width - images[2].get_rect().width, 5))
        elif self.health <= 0:
            self.screen.blit(images[5], (self.screen_width - images[5].get_rect().width, 0))
            self.die = True
    
    def create_bullet(self):
        Bullet.Bullet(self.screen_width, self.screen_height, self.screen, Main_character, (self.rect.x - 80, self.rect.y - 10), self.last_move_left, self.bullet_group)

    def damaged(self, mob):
        self.health -= mob.attacks

    def animation_died(self):
        if self.animCount_die + 1 >= 40:
            self.group.remove(self)
            self.animCount_die = 0

        if self.last_move_left:
            self.image = self.animation_for_left_die[self.animCount_die // 8]
            self.animCount_die += 1
        else:
            self.image = self.animation_for_right_die[self.animCount_die // 8]
            self.animCount_die += 1

    def balanced(self):
        self.screen.blit(Main_character.coin, (0, 0))
        f = pygame.font.SysFont("arial", 37)
        text = f.render(str(self.balance), True, (0, 0, 0))
        self.screen.blit(text, (35, -5))

    def costs(self):
        f = pygame.font.SysFont("arial", 37)
        text1 = f.render(str(self.up_costs[1]), True, (0, 0, 0))
        text2 = f.render(str(self.up_costs[2]), True, (0, 0, 0))

        self.screen.blit(text1, (452, 440))
        self.screen.blit(text2, (852, 440))

        self.screen.blit(Main_character.coin, (423, 445))
        self.screen.blit(Main_character.coin, (823, 445))


class Background():
    image = pygame.image.load("background/background.png")
    image_die = pygame.image.load("background/die.jpg")

    def __init__(self, screen):

        self.image = Background.image
        self.image = pygame.transform.scale(self.image, (1420, 720))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.screen = screen

    def update(self, die, waves):
        if die:
            self.image = Background.image_die
            self.image = pygame.transform.scale(self.image, (1420, 720))


        wave = {
            1 : "Первая волна",
            2 : "Вторая волна",
            3 : "Третья волна",
            4 : "Четвёртая волна",
            5 : "Битва с боссом!"
        }

        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        if waves != 0:
            f = pygame.font.SysFont("arial", 36)
            text = f.render(wave[waves], True, (0, 0, 0))
            self.screen.blit(text, (590, 0)) 
        

