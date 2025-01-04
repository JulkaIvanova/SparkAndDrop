import pygame
import os
import sys
import math



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
        self.jump_in_progress = False
        self.vertical_velocity = 0
        self.is_flipped = False
        self.image_original = load_image("mag.png")  # Оригинальное изображение
        self.image_original = pygame.transform.scale(self.image_original, (40, 40))
        self.image = self.image_original
    def update(self, *args, levelMap):
        #if args and (args[0].type == pygame.KEYDOWN):
        #    print(args[0].key, pygame.K_d)
        #if args and (args[0].type == pygame.KEYDOWN) and (args[0].key == pygame.K_d):
        self.v = 120
        self.fps = 120
        # Размеры блока (например, 40x40)
        BLOCK_SIZE = 40

        # Проверка нижних углов персонажа
        left_x = int(self.xpos // BLOCK_SIZE)
        right_x = int((self.xpos + self.rect.width - 1) // BLOCK_SIZE)  # Учитываем правый край
        bottom_y = int((self.ypos + self.rect.height) // BLOCK_SIZE)  # Нижний край персонажа

        # Профверка блока под левым и правым нижним пикселем
        block_below_left = levelMap[bottom_y][left_x]
        block_below_right = levelMap[bottom_y][right_x]

        # Проверяем, есть ли блоки под нижними пикселями
        if block_below_left in [".", "$", "@", "X", "7"] and block_below_right in [".", "$", "@", "X", "7"] \
                and not self.jump_in_progress:
            # Если под персонажем пустое пространство, он будет падать
            self.ypos += 400 / self.fps  # Падение с определенной скоростью
            self.rect.top = self.ypos
        else:
            # Если под персонажем есть блок, фиксируем его на уровне блока
            self.ypos = bottom_y * BLOCK_SIZE - self.rect.height  # Фиксируем на верхней границе блока
            self.rect.top = self.ypos

        if args and pygame.key.get_pressed()[pygame.K_d]:
            if levelMap[int(self.ypos // BLOCK_SIZE)][int(self.xpos // BLOCK_SIZE) + 1] in [".", "$", "@", "X", "7"]:
                if levelMap[int((self.ypos + 39) // BLOCK_SIZE)][
                    int((self.xpos + self.v / self.fps) // BLOCK_SIZE)] not in '#I':
                    self.xpos += self.v / self.fps
                    self.clock.tick(self.fps)
                    self.rect.left = self.xpos
                    if self.is_flipped:
                        self.image = self.image_original
                        self.is_flipped = False
        if args and pygame.key.get_pressed()[pygame.K_a]:
            if levelMap[int(self.ypos // BLOCK_SIZE)][int(self.xpos // BLOCK_SIZE)] in [".", "$", "@", "X", "7"]:
                if levelMap[int((self.ypos + 39) // BLOCK_SIZE)][
                    int((self.xpos - self.v / self.fps) // BLOCK_SIZE)] not in '#I':
                    self.xpos -= self.v / self.fps
                    self.clock.tick(self.fps)
                    self.rect.left = self.xpos
                    if not self.is_flipped:
                        self.image = pygame.transform.flip(self.image_original, True, False)
                        self.is_flipped = True
        if args and pygame.key.get_pressed()[pygame.K_w] and not self.jump_in_progress:
            # Проверка, что персонаж стоит на блоке
            bottom_y = int((self.ypos + self.rect.height) // 40)
            left_x = int(self.xpos // 40)
            right_x = int((self.xpos + self.rect.width) // 40)

            # Если под персонажем есть блок, то разрешаем прыжок
            if (
                    levelMap[bottom_y][left_x] not in [".", "$", "@", "X", "7"]
                    and levelMap[bottom_y][right_x] not in [".", "$", "@", "X", "7"]
            ):
                self.jump_height = 3 * 40  # 3 blocks of 40 pixels each
                self.jump_speed = -120 / self.fps  # Slow upward movement for the "flying" feel
                self.current_jump_height = 0  # Track how much height has been achieved
                self.jump_in_progress = True  # Flag to track jumping state

        if self.jump_in_progress:
            # Check for collision above before moving
            if self.vertical_velocity < 0:  # Moving up
                top_y = int((self.ypos + self.vertical_velocity) // 40)
                left_x = int(self.xpos // 40)
                right_x = int((self.xpos + self.rect.width) // 40)

                # If there's a block above, stop upward movement
                if (
                        levelMap[top_y][left_x] not in [".", "$", "@", "X", "7"]
                        or levelMap[top_y][right_x] not in [".", "$", "@", "X", "7"]
                ):
                    self.vertical_velocity = 0  # Stop upward movement
                    self.jump_in_progress = False  # Cancel jump

            # Continue upward movement if within jump height limit
            if self.current_jump_height < self.jump_height:
                self.vertical_velocity = self.jump_speed
                self.current_jump_height += abs(self.vertical_velocity)
            else:
                # Start descending after reaching max height
                self.vertical_velocity = 1200 / self.fps  # Simulate falling

            # Check for collision while falling
            if self.vertical_velocity > 0:  # Moving down
                bottom_y = int((self.ypos + self.vertical_velocity + self.rect.height) // 40)
                left_x = int(self.xpos // 40)
                right_x = int((self.xpos + self.rect.width) // 40)

                # If there's a block below, stop downward movement
                if (
                        levelMap[bottom_y][left_x] == '#'
                        or levelMap[bottom_y][right_x] == '#'
                ):
                    self.vertical_velocity = 0  # Stop falling
                    self.jump_in_progress = False  # Stop falling when landing

            # Update position
            self.ypos += self.vertical_velocity
            self.rect.top = self.ypos

            # End jump when landing
            if self.vertical_velocity > 0 and self.ypos % 40 == 0:
                self.jump_in_progress = False
                self.vertical_velocity = 0

        # if args and pygame.key.get_pressed()[pygame.K_w]:
        #     self.ypos += 100/self.fps
        #     self.clock.tick(self.fps)
        #     self.rect.top = self.ypos
        #     self.ypos -= 100/self.fps
        #     self.clock.tick(self.fps)
        #     self.rect.top = self.ypos
    # def falling(self, levelMap):
    #     if levelMap[int(self.ypos//40)+1][int(self.xpos//40)] == ".":
    #         self.ypos += 400/self.fps
    #         self.clock.tick(self.fps)
    #         self.rect.top = self.ypos

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



