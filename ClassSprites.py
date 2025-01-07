import pygame
import os
import sys
import math
import commonConsts



pygame.init()

def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def checkList(list):
    
    for i in list:
        if i.activate:
            return True
    return False

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int, *group, width=0, height=0, ):
        super().__init__(*group)
        self.image = image
        if (width>0) or (height>0):
            if width==0:
                width=height
            if height==0:
                height=width
            self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def get_left_cell_x(self):
        return int(self.rect.left // commonConsts.BLOCK_SIZE)

    def get_right_cell_x(self):
        return int(self.rect.right // commonConsts.BLOCK_SIZE)

    def get_top_cell_y(self):
        return int(self.rect.top // commonConsts.BLOCK_SIZE)

    def get_bottom_cell_y(self):
        return int(self.rect.bottom // commonConsts.BLOCK_SIZE)

class Block(GameSprite):
    image = load_image("blok.jpg")

    def __init__(self, *group, x, y):
        super().__init__(Block.image, x, y, *group, width= 40)

class Coin(GameSprite):
    image = load_image("coin.png")

    def __init__(self, *group, x, y):
        super().__init__(Coin.image, x, y, *group, width= 40)
    
    def update(self, *args, mag, robber, coinsCollect):
        if pygame.sprite.collide_mask(self, mag) or pygame.sprite.collide_mask(self, robber):
            self.kill()
            coinsCollect.cnt += 1
            

class Door(GameSprite):
    image = load_image("door.png")

    def __init__(self, *group, x, y):
        super().__init__(Door.image, x, y, *group, width= 40, height= 80)
        self.win = False


class MagicDoor(GameSprite):
    image = load_image("magicdoor.png")

    def __init__(self, *group, x, y):
        super().__init__(MagicDoor.image, x, y, *group, width= 40, height= 80)
        # self.open = False
    
    def update(self, *args, mag, levelMap):
        # if pygame.sprite.collide_mask(mag, self):
        if levelMap[int(mag.ypos//40)][int(mag.xpos//40)-1] == "I" or levelMap[int(mag.ypos//40)][int(mag.xpos//40)+1] == "I":
            #print(6)
            if args and pygame.key.get_pressed()[pygame.K_s]:
                # self.open = True
                #print(8)
                levelMap[int(self.rect.y//40)] = levelMap[int(self.rect.y//40)][:int(self.rect.x//40)]+"."+levelMap[int(self.rect.y//40)][int(self.rect.x//40)+1:]
                levelMap[int(self.rect.y//40)+1] = levelMap[int(self.rect.y//40)+1][:int(self.rect.x//40)]+"."+levelMap[int(self.rect.y//40)+1][int(self.rect.x//40)+1:]
                self.kill()

class Button(GameSprite):
    image = load_image("button.png")

    def __init__(self, *group, x, y):
        super().__init__(Button.image, x, y, *group, width= 40)
        self.activate = False
    
    def update(self, *args, mag, robber):
        if args and ((pygame.sprite.collide_mask(self, mag) and pygame.key.get_pressed()[pygame.K_q]) or (pygame.sprite.collide_mask(self, robber) and pygame.key.get_pressed()[pygame.K_u])):
            self.activate = True
        else:
            self.activate = False

class Lever(GameSprite):
    image = load_image("lever.png")

    def __init__(self, *group, x, y):
        super().__init__(Lever.image, x, y, *group, width= 40)
        self.activate = False

    def update(self, *args, mag, robber):
        if not(args[0] is None):
            if ((pygame.sprite.collide_mask(self, mag) and pygame.KEYDOWN and args[0].key == pygame.K_q) or (pygame.sprite.collide_mask(self, robber) and pygame.KEYDOWN and args[0].key == pygame.K_u)):
                if self.activate:
                    self.activate = False
                else:
                    self.activate = True

class GorizontalDoor(GameSprite):
    image = load_image("gorizontaldoor.png")

    def __init__(self, *group, x, y):
        super().__init__(GorizontalDoor.image, x, y, *group, width= 80, height= 40)
        self.button = []
        self.y = int(self.rect.y//40)
        self.x = int(self.rect.x//40)
        self.imghide = load_image(f"hide.png")
    
    def connect(self, cnt, objectt, typetext, cntbuttons=None):
        self.image = load_image(f"gorizontaldoor{cnt}.png")
        self.image = pygame.transform.scale(self.image, (80, 40))
        self.image_original = self.image
        if cntbuttons is None:
            self.button.append(objectt)
            self.button[0].image = load_image(f"{typetext}{cnt}.png")
            self.button[0].image = pygame.transform.scale(self.button[0].image, (40, 40))
        else:
            for i in range(cntbuttons):
                self.button.append(objectt[i])
                self.button[i].image = load_image(f"{typetext}{cnt}.png")
                self.button[i].image = pygame.transform.scale(self.button[i].image, (40, 40))
            
    def check(self, levelMap):
        if checkList(self.button):
            # levelMap[int(y//40)] = levelMap[int(y//40)][:int(x//40)]+"."+levelMap[int(y//40)][int(x//40)+1:]
            # levelMap[int(y//40)+1] = levelMap[int(y//40)+1][:int(x//40)]+"."+levelMap[int(y//40)+1][int(x//40)+1:]
            levelMap[self.y] = levelMap[self.y][:self.x]+".."+levelMap[self.y][self.x+2:]
            self.image = self.imghide
            #print("\n".join(levelMap))
        else:
            levelMap[self.y] = levelMap[self.y][:self.x]+"--"+levelMap[self.y][self.x+2:]
            self.image = self.image_original
            # for i in self.button:
            #     print(i.activate)

class VerticalDoor(GameSprite):
    image = load_image("verticaldoor.png")

    def __init__(self, *group, x, y):
        super().__init__(VerticalDoor.image, x, y, *group, width= 40, height= 80)
        self.button = []
        self.y = int(self.rect.y//40)
        self.x = int(self.rect.x//40)
        self.imghide = load_image(f"hide.png")
    
    def connect(self, cnt, objectt, typetext, cntbuttons=None):
        self.image = load_image(f"verticaldoor{cnt}.png")
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.image_original = self.image
        if cntbuttons is None:
            self.button.append(objectt)
            self.button[0].image = load_image(f"{typetext}{cnt}.png")
            self.button[0].image = pygame.transform.scale(self.button[0].image, (40, 40))
        else:
            for i in range(cntbuttons):
                print("qwe")
                self.button.append(objectt[i])
                self.button[i].image = load_image(f"{typetext}{cnt}.png")
                self.button[i].image = pygame.transform.scale(self.button[i].image, (40, 40))
            
    def check(self, levelMap):
        if checkList(self.button):
            levelMap[self.y] = levelMap[self.y][:self.x]+"."+levelMap[self.y][self.x+1:]
            levelMap[self.y+1] = levelMap[self.y+1][:self.x]+"."+levelMap[self.y+1][self.x+1:]
            self.image = self.imghide
            #print("\n".join(levelMap))
        else:
            levelMap[self.y] = levelMap[self.y][:self.x]+"|"+levelMap[self.y][self.x+1:]
            levelMap[self.y+1] = levelMap[self.y+1][:self.x]+"|"+levelMap[self.y+1][self.x+1:]
            self.image = self.image_original
            # for i in self.button:
            #     print(i.activate)

class Monsters(GameSprite):
    image = load_image("monster.png")

    def __init__(self, *group, x, y, clock):
        super().__init__(Monsters.image, x, y, *group, width= 40, height= 40)
        self.xpos = x
        self.ypos = y
        self.clock = clock
        self.rightFlag = False
    
    def update(self, *args, mag, robber, levelMap):
        self.v = 120
        #BLOCK_SIZE = 40
        left_x = int(self.xpos // commonConsts.BLOCK_SIZE)
        right_x = int((self.xpos + self.rect.width - 1) // commonConsts.BLOCK_SIZE)  # Учитываем правый край
        bottom_y = int((self.ypos + self.rect.height) // commonConsts.BLOCK_SIZE)
        if pygame.sprite.collide_mask(self, mag):
            mag.alive = False
        # if self.rightFlag:
        #     if (mag.xpos+40 == self.xpos or mag.xpos == self.xpos) and int(mag.ypos//40) == int(self.ypos//40):
        #         mag.alive = False
        # else:
        #     if (mag.xpos+40 == self.xpos+40 or mag.xpos == self.xpos+40) and int(mag.ypos//40) == int(self.ypos//40):
        #         mag.alive = False
        if self.rightFlag==False:
            if levelMap[int(self.ypos//40)][int(self.xpos//40)+1] in ".@$7X" and levelMap[int(self.ypos//40)+1][int(self.xpos//40)+1] in "#-":
                self.xpos += self.v/commonConsts.FPS
                self.rect.left = self.xpos
            else:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rightFlag = True
        if self.rightFlag:
            if levelMap[int(self.ypos//40)][int(self.xpos//40)] in ".@$7X" and levelMap[int(self.ypos//40)+1][int(self.xpos//40)] in "#-":
                self.xpos -= self.v/commonConsts.FPS
                self.rect.left = self.xpos
            else:
                self.rightFlag = False
                self.image = pygame.transform.flip(self.image, True, False)


class Mag(GameSprite):
    image = load_image("mag.png")

    def __init__(self, *group, x, y, clock):
        super().__init__(Mag.image, x, y, *group, width= 40)
       
        self.alive = True
        self.xpos = x
        self.ypos = y
        self.clock = clock
        self.jump_in_progress = False
        self.vertical_velocity = 0
        self.is_flipped = False
        self.image_original = pygame.transform.scale(self.image, (40, 40))

    def update(self, *args, levelMap):
        #if args and (args[0].type == pygame.KEYDOWN):
        #    print(args[0].key, pygame.K_d)
        #if args and (args[0].type == pygame.KEYDOWN) and (args[0].key == pygame.K_d):
        self.v = 240

        # Проверка нижних углов персонажа
        self.left_x = int(self.xpos // commonConsts.BLOCK_SIZE)
        self.right_x = int((self.xpos + self.rect.width - 1) // commonConsts.BLOCK_SIZE)  # Учитываем правый край
        self.bottom_y = int((self.ypos + self.rect.height) // commonConsts.BLOCK_SIZE)  # Нижний край персонажа

        self.top_y = int((self.ypos) // commonConsts.BLOCK_SIZE)
        # Профверка блока под левым и правым нижним пикселем
        block_below_left = levelMap[self.bottom_y][self.left_x]
        block_below_right = levelMap[self.bottom_y][self.right_x]

        # Проверяем, есть ли блоки под нижними пикселями
        if block_below_left in [".", "$", "@", "X", "7", "*", "0"] and block_below_right in [".", "$", "@", "X", "7", "*", "0"] \
                and not self.jump_in_progress:
            # Если под персонажем пустое пространство, он будет падать
            self.ypos += 400 / commonConsts.FPS  # Падение с определенной скоростью
            self.rect.top = self.ypos
        else:
            # Если под персонажем есть блок, фиксируем его на уровне блока
            self.ypos = self.bottom_y * commonConsts.BLOCK_SIZE - self.rect.height  # Фиксируем на верхней границе блока
            self.rect.top = self.ypos

        if args and pygame.key.get_pressed()[pygame.K_d]:
            if levelMap[int(self.ypos // commonConsts.BLOCK_SIZE)][int(self.xpos // commonConsts.BLOCK_SIZE) + 1] in [".", "$", "@", "X", "7", "*", "0"]:
                if levelMap[int((self.ypos + 39) // commonConsts.BLOCK_SIZE)][
                    int((self.xpos + self.v / commonConsts.FPS) // commonConsts.BLOCK_SIZE)] not in '#I':
                    self.xpos += self.v / commonConsts.FPS
                    self.rect.left = self.xpos
                    if self.is_flipped:
                        self.image = self.image_original
                        self.is_flipped = False
        if args and pygame.key.get_pressed()[pygame.K_a]:
            if levelMap[int(self.ypos // commonConsts.BLOCK_SIZE)][int(self.xpos // commonConsts.BLOCK_SIZE)] in [".", "$", "@", "X", "7", "*", "0"]:
                if levelMap[int((self.ypos + 39) // commonConsts.BLOCK_SIZE)][
                    int((self.xpos - self.v / commonConsts.FPS) // commonConsts.BLOCK_SIZE)] not in '#I':
                    self.xpos -= self.v / commonConsts.FPS
                    self.rect.left = self.xpos
                    if not self.is_flipped:
                        self.image = pygame.transform.flip(self.image_original, True, False)
                        self.is_flipped = True
        if args and pygame.key.get_pressed()[pygame.K_w] and not self.jump_in_progress:
            # Проверка, что персонаж стоит на блоке
            self.bottom_y = int((self.ypos + self.rect.height) // commonConsts.BLOCK_SIZE)
            self.left_x = int(self.xpos // commonConsts.BLOCK_SIZE)
            self.right_x = int((self.xpos + self.rect.width - 1) // commonConsts.BLOCK_SIZE)

            # Если под персонажем есть блок, то разрешаем прыжок
            if (
                    levelMap[self.bottom_y][self.left_x] not in [".", "$", "@", "X", "7", "*", "0"]
                    or levelMap[self.bottom_y][self.right_x] not in [".", "$", "@", "X", "7", "*", "0"]
            ):
                self.jump_height = 3 * 40  # 3 blocks of 40 pixels each
                self.jump_speed = -120 / commonConsts.FPS  # Slow upward movement for the "flying" feel
                self.current_jump_height = 0  # Track how much height has been achieved
                self.jump_in_progress = True  # Flag to track jumping state

        if self.jump_in_progress:
            # Check for collision above before moving
            if self.vertical_velocity < 0:  # Moving up
                self.top_y = int((self.ypos + self.vertical_velocity) // 40)
                self.left_x = int(self.xpos // 40)
                self.right_x = int((self.xpos + self.rect.width - 1) // 40)

                # If there's a block above, stop upward movement
                if (
                        levelMap[self.top_y][self.left_x] not in [".", "$", "@", "X", "7", "*", "0"]
                        or levelMap[self.top_y][self.right_x] not in [".", "$", "@", "X", "7", "*", "0"]
                ):
                    self.vertical_velocity = 0  # Stop upward movement
                    self.jump_in_progress = False  # Cancel jump

            # Continue upward movement if within jump height limit
            if self.current_jump_height < self.jump_height:
                self.vertical_velocity = self.jump_speed
                self.current_jump_height += abs(self.vertical_velocity)/commonConsts.FPS
            else:
                # Start descending after reaching max height
                self.vertical_velocity = 1200 / commonConsts.FPS  # Simulate falling

            # Check for collision while falling
            if self.vertical_velocity > 0:  # Moving down
                self.bottom_y = int((self.ypos + self.vertical_velocity + self.rect.height) // 40)
                self.left_x = int(self.xpos // 40)
                self.right_x = int((self.xpos + self.rect.width - 1) // 40)

                # If there's a block below, stop downward movement
                if (
                        levelMap[self.bottom_y][self.left_x] == '#'
                        or levelMap[self.bottom_y][self.right_x] == '#'
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
        #     self.ypos += 100/commonConsts.FPS
        #     self.clock.tick(commonConsts.FPS)
        #     self.rect.top = self.ypos
        #     self.ypos -= 100/commonConsts.FPS
        #     self.clock.tick(commonConsts.FPS)
        #     self.rect.top = self.ypos
    # def falling(self, levelMap):
    #     if levelMap[int(self.ypos//40)+1][int(self.xpos//40)] == ".":
    #         self.ypos += 400/commonConsts.FPS
    #         self.clock.tick(commonConsts.FPS)
    #         self.rect.top = self.ypos

class Robber(GameSprite):
    image = load_image("robber.png")

    def __init__(self, *group, x, y):
        super().__init__(Robber.image, x, y, *group, width= 40, height= 80)
        self.alive = True

    # def update(self):
    #     if args and args[0].type == pygame.MOUSEBUTTONDOWN:
    #         self.image = self.image_boom


 