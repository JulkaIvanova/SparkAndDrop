import pygame
import os
import sys
import math
import commonConsts
import spritesBase



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

class Block(spritesBase.GameSprite):
    image = load_image("blok.jpg")

    def __init__(self, *group, x, y):
        super().__init__(Block.image, x, y, *group, width= 40)

class Coin(spritesBase.GameSprite):
    image = load_image("coin.png")

    def __init__(self, *group, x, y):
        super().__init__(Coin.image, x, y, *group, width= 40)
    
    def update(self, *args, mag, robber, coinsCollect):
        if pygame.sprite.collide_mask(self, mag) or pygame.sprite.collide_mask(self, robber):
            self.kill()
            coinsCollect.cnt += 1
            

class Door(spritesBase.GameSprite):
    image = load_image("door.png")

    def __init__(self, *group, x, y):
        super().__init__(Door.image, x, y, *group, width= 40, height= 80)
        self.win = False


class MagicDoor(spritesBase.GameSprite):
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

class Button(spritesBase.GameSprite):
    image = load_image("button.png")

    def __init__(self, *group, x, y):
        super().__init__(Button.image, x, y, *group, width= 40)
        self.activate = False
    
    def update(self, *args, mag, robber):
        if args and ((pygame.sprite.collide_mask(self, mag) and pygame.key.get_pressed()[pygame.K_q]) or (pygame.sprite.collide_mask(self, robber) and pygame.key.get_pressed()[pygame.K_u])):
            self.activate = True
        else:
            self.activate = False

class Lever(spritesBase.GameSprite):
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

class GorizontalDoor(spritesBase.GameSprite):
    image = load_image("gorizontaldoor.png")

    def __init__(self, *group, x, y):
        super().__init__(GorizontalDoor.image, x, y, *group, width= 80, height= 40)
        self.button = []
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
            levelMap[self.get_top_cell_y()] = levelMap[self.get_top_cell_y()][:self.get_left_cell_x()]+".."+levelMap[self.get_top_cell_y()][self.get_left_cell_x()+2:]
            self.image = self.imghide
            #print("\n".join(levelMap))
        else:
            levelMap[self.get_top_cell_y()] = levelMap[self.get_top_cell_y()][:self.get_left_cell_x()]+"--"+levelMap[self.get_top_cell_y()][self.get_left_cell_x()+2:]
            self.image = self.image_original
            # for i in self.button:
            #     print(i.activate)

class VerticalDoor(spritesBase.GameSprite):
    image = load_image("verticaldoor.png")

    def __init__(self, *group, x, y):
        super().__init__(VerticalDoor.image, x, y, *group, width= 40, height= 80)
        self.button = []
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
            levelMap[self.get_top_cell_y()] = levelMap[self.get_top_cell_y()][:self.get_left_cell_x()]+"."+levelMap[self.get_top_cell_y()][self.get_left_cell_x()+1:]
            levelMap[self.get_top_cell_y()+1] = levelMap[self.get_top_cell_y()+1][:self.get_left_cell_x()]+"."+levelMap[self.get_top_cell_y()+1][self.get_left_cell_x()+1:]
            self.image = self.imghide
            #print("\n".join(levelMap))
        else:
            levelMap[self.get_top_cell_y()] = levelMap[self.get_top_cell_y()][:self.get_left_cell_x()]+"|"+levelMap[self.get_top_cell_y()][self.get_left_cell_x()+1:]
            levelMap[self.get_top_cell_y()+1] = levelMap[self.get_top_cell_y()+1][:self.get_left_cell_x()]+"|"+levelMap[self.get_top_cell_y()+1][self.get_left_cell_x()+1:]
            self.image = self.image_original
            # for i in self.button:
            #     print(i.activate)


class Monsters(spritesBase.MovableGameSprite):
    image = load_image("monster.png")

    def __init__(self, *group, x, y, levelMap, mag, robber):
        super().__init__(Monsters.image, x, y, *group, width= 40, height= 40, level_map=levelMap, hspeed=120)
        self.mag = mag
        self.robber = robber
    
    def can_move(self, block_content):
        return block_content in ".@$7X"
    
    def can_stay(self, block_content):
        return block_content in "#-"

    def do_update(self, *args):
        if pygame.sprite.collide_mask(self, self.mag):
            self.mag.alive = False
        self.move(False, True)


class Mag(spritesBase.MovableGameSprite):
    image = load_image("mag.png")

    def __init__(self, *group, x, y, levelMap):
        super().__init__(Mag.image, x, y, *group, width= 40, height= 40, level_map=levelMap, hspeed=240)
       
        self.alive = True
        self.xpos = x
        self.ypos = y
        self.jump_in_progress = False
        self.vertical_velocity = 0
        self.is_flipped = False
        self.image_original = pygame.transform.scale(self.image, (40, 40))

    def can_move(self, block_content):
        return block_content in [".", "$", "@", "X", "7", "*", "0"]
    
    def can_stay(self, block_content):
        return not (block_content in [".", "$", "@", "X", "7", "*", "0"])

    def do_update(self, *args):
        if args and pygame.key.get_pressed()[pygame.K_d]:
            self.set_direction(True)
            self.move()
        if args and pygame.key.get_pressed()[pygame.K_a]:
            self.set_direction(False)
            self.move()
        if args and pygame.key.get_pressed()[pygame.K_w]:
            self.jump()
        return    

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

class Robber(spritesBase.GameSprite):
    image = load_image("robber.png")

    def __init__(self, *group, x, y):
        super().__init__(Robber.image, x, y, *group, width= 40, height= 80)
        self.alive = True

    # def update(self):
    #     if args and args[0].type == pygame.MOUSEBUTTONDOWN:
    #         self.image = self.image_boom


 