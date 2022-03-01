import pygame
import os

class Mob_manager():
    def __init__(self):
        self.kol_vo = 0
        self.wave = 1

    def manager(self, width, height, screen, character, max_in_group, maximum, group, wave):
        if self.wave != wave:
            self.kol_vo = 0
            self.wave += 1
        if len(group) < (max_in_group + wave * 2) and self.kol_vo < (maximum + wave * 5) and wave < 5:
            if self.kol_vo % 2 == 0:
                group.add(Troll(width, height, screen, character, True, group))
            elif self.kol_vo % 3 == 0 and wave >= 3:
                group.add(Troll_grey(width, height, screen, character, True, group))
            else:
                group.add(Troll(width, height, screen, character, False, group))
        elif wave == 5 and self.kol_vo == 0:
            group.add(Ork(width, height, screen, character, True, group))
            self.wave = wave
        self.kol_vo += 1


class Mobs(pygame.sprite.Sprite):
    def __init__(self, width, height, screen, character, left, *group):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.screen = screen
        self.character = character
        self.left = left


class Troll(Mobs):
    image_left = pygame.image.load("Image_monstr/1_TROLL/Troll_01_1_IDLE_000.png")
    image_right = pygame.transform.flip(image_left, 1, 0)

    images = []
    images_left = []

    for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/1_TROLL/Run"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/1_TROLL/Run/{filename}")
            prp = image.get_rect().width / image.get_rect().height

            image = pygame.transform.scale(image, (int(200 * prp), 200))

            images.append(image)
            images_left.append(pygame.transform.flip(image, 1, 0))

    images_die = []
    images_left_die = []

    for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/1_TROLL/Die"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/1_TROLL/Die/{filename}")
            prp = image.get_rect().width / image.get_rect().height
            image = pygame.transform.scale(image, (int(200 * prp), 200))

            images_die.append(image)
            images_left_die.append(pygame.transform.flip(image, 1, 0))

    images_attack = []
    images_left_attack = []

    for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/1_TROLL/Attack"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/1_TROLL/Attack/{filename}")
            prp = image.get_rect().width / image.get_rect().height

            if len(images_attack) > 2:
                image = pygame.transform.scale(image, (int(prp * 200), 190))
                images_attack.append(image)
                images_left_attack.append(pygame.transform.flip(image, 1, 0))
            else:
                image = pygame.transform.scale(image, (int(prp * 200), 200))
                images_attack.append(image)
                images_left_attack.append(pygame.transform.flip(image, 1, 0))


    def __init__(self, width, height, screen, character, left, *group):
        super().__init__(width, height, screen, character, left, *group)

        self.image = pygame.transform.scale(Troll.image_left, (240, 200))

        self.rect = self.image.get_rect()
        self.rect.x = 0 - self.rect.width if self.left else self.width + self.rect.width
        self.rect.y = self.height - self.rect.height - 80

        self.speed = 1 if self.left else -1

        self.health = 100
        self.attacks = 20

        self.group = group

        self.animCount = 0
        self.animCount_die = 0
        self.animCount_attack = 0

        self.die = False
        self.stop = False
        self.attack = False

        self.damage = False


    def update(self):
        self.rect = self.rect.move(self.speed, 0)

        colls_with_bullet = pygame.sprite.spritecollide(self, self.character.bullet_group, True, pygame.sprite.collide_rect_ratio(0.4))
        if colls_with_bullet:
            self.health -= colls_with_bullet[0].damage
        else:
            self.speed = 1 if self.left else -1

        colls_with_hero = pygame.sprite.spritecollide(self, self.character.group, False)
        if colls_with_hero:
            self.speed = 0
            self.attack = True
            if self.damage:
                self.character.damaged(self)
                self.damage = False

        else:
            self.speed = 1 if self.left else -1
            self.attack = False

        if self.health <= 0:
            self.animation_die()    
        elif not self.attack:
            self.animation()
        elif self.attack:
            self.animation_attack()

    def animation(self):
        if self.animCount + 1 >= 90:
            self.animCount = 0

        if self.left:
            self.image = Troll.images[self.animCount // 9]
        else:
            self.image = Troll.images_left[self.animCount // 9]

        self.animCount += 1

    def animation_die(self):
        if self.animCount_die + 1 >= 45:
            self.character.balance += 100
            self.group[0].remove(self)
            self.animCount_die = 0

        if self.left:
            self.image = Troll.images_die[self.animCount_die // 9]
        else:
            self.image = Troll.images_left_die[self.animCount_die // 9]

        self.animCount_die += 1

    def animation_attack(self):
        if self.animCount_attack + 1 >= 60:
            self.damage = True
            self.animCount_attack = 0

        if self.left:
            self.image = Troll.images_attack[self.animCount_attack // 10]
        else:
            self.image = Troll.images_left_attack[self.animCount_attack // 10]

        self.animCount_attack += 1

class Troll_grey(Mobs):
    image_left = pygame.image.load("Image_monstr/2_TROLL/Troll_01_1_IDLE_000.png")
    image_right = pygame.transform.flip(image_left, 1, 0)

    images = []
    images_left = []

    for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/2_TROLL/Run"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/2_TROLL/Run/{filename}")
            prp = image.get_rect().width / image.get_rect().height

            image = pygame.transform.scale(image, (int(200 * prp), 200))

            images.append(image)
            images_left.append(pygame.transform.flip(image, 1, 0))

    images_die = []
    images_left_die = []

    for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/2_TROLL/Die"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/2_TROLL/Die/{filename}")
            prp = image.get_rect().width / image.get_rect().height
            image = pygame.transform.scale(image, (int(200 * prp), 200))

            images_die.append(image)
            images_left_die.append(pygame.transform.flip(image, 1, 0))

    images_attack = []
    images_left_attack = []

    for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/2_TROLL/Attack"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/2_TROLL/Attack/{filename}")
            prp = image.get_rect().width / image.get_rect().height

            if len(images_attack) > 2:
                image = pygame.transform.scale(image, (int(prp * 200), 190))
                images_attack.append(image)
                images_left_attack.append(pygame.transform.flip(image, 1, 0))
            else:
                image = pygame.transform.scale(image, (int(prp * 200), 200))
                images_attack.append(image)
                images_left_attack.append(pygame.transform.flip(image, 1, 0))

    def __init__(self, width, height, screen, character, left, *group):
        super().__init__(width, height, screen, character, left, *group)

        self.image = pygame.transform.scale(Troll.image_left, (240, 200))

        self.rect = self.image.get_rect()
        self.rect.x = 0 - self.rect.width if self.left else self.width + self.rect.width
        self.rect.y = self.height - self.rect.height - 80

        self.speed = 2 if self.left else -2

        self.health = 300
        self.attacks = 40

        self.group = group

        self.animCount = 0
        self.animCount_die = 0
        self.animCount_attack = 0

        self.die = False
        self.stop = False
        self.attack = False

        self.damage = False


    def update(self):
        self.rect = self.rect.move(self.speed, 0)

        colls_with_bullet = pygame.sprite.spritecollide(self, self.character.bullet_group, True, pygame.sprite.collide_rect_ratio(0.4))
        if colls_with_bullet:
            self.health -= colls_with_bullet[0].damage
        else:
            self.speed = 2 if self.left else -2

        colls_with_hero = pygame.sprite.spritecollide(self, self.character.group, False)
        if colls_with_hero:
            self.speed = 0
            self.attack = True
            if self.damage:
                self.character.damaged(self)
                self.damage = False

        else:
            self.speed = 2 if self.left else -2
            self.attack = False

        if self.health <= 0:
            self.animation_die()    
        elif not self.attack:
            self.animation()
        elif self.attack:
            self.animation_attack()

    def animation(self):
        if self.animCount + 1 >= 90:
            self.animCount = 0

        if self.left:
            self.image = Troll_grey.images[self.animCount // 9]
        else:
            self.image = Troll_grey.images_left[self.animCount // 9]

        self.animCount += 1

    def animation_die(self):
        if self.animCount_die + 1 >= 45:
            self.character.balance += 300
            self.group[0].remove(self)
            self.animCount_die = 0

        if self.left:
            self.image = Troll_grey.images_die[self.animCount_die // 9]
        else:
            self.image = Troll_grey.images_left_die[self.animCount_die // 9]

        self.animCount_die += 1

    def animation_attack(self):
        if self.animCount_attack + 1 >= 60:
            self.damage = True
            self.animCount_attack = 0

        if self.left:
            self.image = Troll_grey.images_attack[self.animCount_attack // 10]
        else:
            self.image = Troll_grey.images_left_attack[self.animCount_attack // 10]

        self.animCount_attack += 1


class Ork(Mobs):
    image_left = pygame.image.load("Image_monstr/Ork/Troll3/Idle_000.png")
    image_right = pygame.transform.flip(image_left, 1, 0)

    images = []
    images_left = []


    for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/Ork/Troll3/Walk"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/Ork/Troll3/Walk/{filename}")
            prp = image.get_rect().width / image.get_rect().height

            image = pygame.transform.scale(image, (int(300 * prp), 300))

            images.append(image)
            images_left.append(pygame.transform.flip(image, 1, 0))

    images_die = []
    images_left_die = []

    for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/Ork/Troll3/Die"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/Ork/Troll3/Die/{filename}")
            prp = image.get_rect().width / image.get_rect().height
            image = pygame.transform.scale(image, (int(300 * prp), 300))

            images_die.append(image)
            images_left_die.append(pygame.transform.flip(image, 1, 0))

    images_attack = []
    images_left_attack = []

    for filename in os.listdir("C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/Ork/Troll3/Attack"):
            image = pygame.image.load(f"C:/Users/lyuk2/Desktop/Python/Project/Pygame/Image_monstr/Ork/Troll3/Attack/{filename}")
            prp = image.get_rect().width / image.get_rect().height

            if len(images_attack) > 2:
                image = pygame.transform.scale(image, (int(prp * 300), 300))
                images_attack.append(image)
                images_left_attack.append(pygame.transform.flip(image, 1, 0))
            else:
                image = pygame.transform.scale(image, (int(prp * 300), 300))
                images_attack.append(image)
                images_left_attack.append(pygame.transform.flip(image, 1, 0))

    def __init__(self, width, height, screen, character, left, *group):
        super().__init__(width, height, screen, character, left, *group)

        self.image = pygame.transform.scale(Troll.image_left, (340, 300))

        self.rect = self.image.get_rect()
        self.rect.x = 0 - self.rect.width if self.left else self.width + self.rect.width
        self.rect.y = self.height - self.rect.height - 60

        self.speed = 3 if self.left else -3

        self.health = 2000
        self.attacks = 100

        self.group = group

        self.animCount = 0
        self.animCount_die = 0
        self.animCount_attack = 0

        self.die = False
        self.stop = False
        self.attack = False

        self.damage = False


    def update(self):
        self.rect = self.rect.move(self.speed, 0)

        colls_with_bullet = pygame.sprite.spritecollide(self, self.character.bullet_group, True, pygame.sprite.collide_rect_ratio(0.4))
        if colls_with_bullet:
            self.health -= colls_with_bullet[0].damage
        else:
            self.speed = 3 if self.left else -3

        colls_with_hero = pygame.sprite.spritecollide(self, self.character.group, False)
        if colls_with_hero:
            self.speed = 0
            self.attack = True
            if self.damage:
                self.character.damaged(self)
                self.damage = False

        else:
            self.speed = 3 if self.left else -3
            self.attack = False

        if self.health <= 0:
            self.animation_die()    
        elif not self.attack:
            self.animation()
        elif self.attack:
            self.animation_attack()

    def animation(self):
        if self.animCount + 1 >= 90:
            self.animCount = 0

        if self.left:
            self.image = Ork.images[self.animCount // 10]
        else:
            self.image = Ork.images_left[self.animCount // 10]

        self.animCount += 1

    def animation_die(self):
        self.rect.y = self.height - self.rect.height - 75
        if self.animCount_die + 1 >= 70:
            self.character.balance += 1000
            self.character.wictory = True
            self.group[0].remove(self)
            self.animCount_die = 0

        if self.left:
            self.image = Ork.images_die[self.animCount_die // 10]
        else:
            self.image = Ork.images_left_die[self.animCount_die // 10]

        self.animCount_die += 1

    def animation_attack(self):
        if self.animCount_attack + 1 >= 90:
            self.damage = True
            self.animCount_attack = 0

        if self.left:
            self.image = Ork.images_attack[self.animCount_attack // 10]
        else:
            self.image = Ork.images_left_attack[self.animCount_attack // 10]

        self.animCount_attack += 1
