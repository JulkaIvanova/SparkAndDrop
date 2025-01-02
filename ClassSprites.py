import pygame
import os
import sys




pygame.init()



def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Block(pygame.sprite.Sprite):
    image = load_image("blok.jpg")

    def __init__(self, *group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. 
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Block.image
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    image = load_image("coin.png")

    def __init__(self, *group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. 
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Coin.image
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Door(pygame.sprite.Sprite):
    image = load_image("door.png")

    def __init__(self, *group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. 
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Door.image
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MagicDoor(pygame.sprite.Sprite):
    image = load_image("magicdoor.png")

    def __init__(self, *group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. 
        # Это очень важно!!!
        super().__init__(*group)
        self.image = MagicDoor.image
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Button(pygame.sprite.Sprite):
    image = load_image("button.png")

    def __init__(self, *group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. 
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Button.image
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Lever(pygame.sprite.Sprite):
    image = load_image("lever.png")

    def __init__(self, *group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. 
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Lever.image
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class GorizontalDoor(pygame.sprite.Sprite):
    image = load_image("gorizontaldoor.png")

    def __init__(self, *group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. 
        # Это очень важно!!!
        super().__init__(*group)
        self.image = GorizontalDoor.image
        self.image = pygame.transform.scale(self.image, (80, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Mag(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, clock):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. 
        # Это очень важно!!!
        super().__init__(*group)
        self.image = load_image("mag.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xpos = x
        self.ypos = y
        self.clock = clock
    def update(self, *args):
        #if args and (args[0].type == pygame.KEYDOWN):
        #    print(args[0].key, pygame.K_d)
        #if args and (args[0].type == pygame.KEYDOWN) and (args[0].key == pygame.K_d):
        self.v = 240
        self.fps = 60
        if args and pygame.key.get_pressed()[pygame.K_d]:
            self.xpos += self.v/self.fps
            self.clock.tick(self.fps)
            self.rect.left = self.xpos
        if args and pygame.key.get_pressed()[pygame.K_a]:
            self.xpos -= self.v/self.fps
            self.clock.tick(self.fps)
            self.rect.left = self.xpos
        if args and pygame.key.get_pressed()[pygame.K_w]:
            self.ypos += 100/self.fps
            self.clock.tick(self.fps)
            self.rect.left = self.ypos
            self.ypos -= 100/self.fps
            self.clock.tick(self.fps)
            self.rect.left = self.ypos
    

class Robber(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. 
        # Это очень важно!!!
        super().__init__(*group)
        self.image = load_image("robber.png")
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            self.image = self.image_boom



