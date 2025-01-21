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
        super().__init__(Block.image, x, y, *group, width=40)


class Coin(spritesBase.GameSprite):
    image = load_image("coin.png")

    def __init__(self, *group, x, y):
        super().__init__(Coin.image, x, y, *group, width=40)

    def update(self, *args, mag, robber, coinsCollect):
        if pygame.sprite.collide_mask(self, mag) or pygame.sprite.collide_mask(self, robber):
            self.kill()
            coinsCollect.cnt += 1


class Door(spritesBase.GameSprite):
    image = load_image("door.png")

    def __init__(self, *group, x, y):
        super().__init__(Door.image, x, y, *group, width=40, height=80)
        self.win = False
        near_door = False

    def update(self, *args, mag: spritesBase.GameSprite, robber: spritesBase.GameSprite, levelMap):
        # print('wefj')
        if self.check_sprite_inside(mag) or self.check_sprite_inside(robber):
            self.near_door = True
            print('wpjfpwejfijweiopfjwoi')
        else:
            self.near_door = False

    def check_sprite_inside(self, sprite):
        """
        Проверяет, находится ли спрайт большей частью внутри двери.

        :param sprite: Игровой спрайт (маг или вор).
        :return: True, если большая часть спрайта внутри двери, иначе False.
        """
        intersection = self.rect.clip(sprite.rect)

        sprite_area = sprite.rect.width * sprite.rect.height
        intersection_area = intersection.width * intersection.height

        return intersection_area > 0.5 * sprite_area


class MagicDoor(spritesBase.GameSprite):
    image = load_image("magicdoor.png")

    def __init__(self, *group, x, y):
        super().__init__(MagicDoor.image, x, y, *group, width=40, height=80)
        # self.open = False

    def update(self, *args, mag: spritesBase.GameSprite, levelMap):
        # if pygame.sprite.collide_mask(mag, self):
        # if levelMap[int(mag.ypos//40)][int(mag.xpos//40)-1] == "I" or levelMap[int(mag.ypos//40)][int(mag.xpos//40)+1] == "I":
        if levelMap[int(mag.get_top_cell_y())][int(mag.get_left_cell_x()) - 1] == "I" or \
                levelMap[int(mag.get_top_cell_y())][int(mag.get_left_cell_x()) + 1] == "I":
            # print(6)
            if args and pygame.key.get_pressed()[pygame.K_e]:
                # self.open = True
                # print(8)
                levelMap[int(self.rect.y // 40)] = levelMap[int(self.rect.y // 40)][:int(self.rect.x // 40)] + "." + \
                                                   levelMap[int(self.rect.y // 40)][int(self.rect.x // 40) + 1:]
                levelMap[int(self.rect.y // 40) + 1] = levelMap[int(self.rect.y // 40) + 1][
                                                       :int(self.rect.x // 40)] + "." + levelMap[
                                                                                            int(self.rect.y // 40) + 1][
                                                                                        int(self.rect.x // 40) + 1:]
                self.kill()


class Button(spritesBase.GameSprite):
    image = load_image("button.png")

    def __init__(self, *group, x, y):
        super().__init__(Button.image, x, y, *group, width=40)
        self.activate = False

    def update(self, *args, mag, robber):
        if args and ((pygame.sprite.collide_mask(self, mag) and pygame.key.get_pressed()[pygame.K_q]) or (
                pygame.sprite.collide_mask(self, robber) and pygame.key.get_pressed()[pygame.K_u])):
            self.activate = True
        else:
            self.activate = False


class Lever(spritesBase.GameSprite):
    image = load_image("lever.png")

    def __init__(self, *group, x, y):
        super().__init__(Lever.image, x, y, *group, width=40)
        self.activate = False

    def update(self, *args, mag: spritesBase.GameSprite, robber: spritesBase.GameSprite):
        if not (args[0] is None):
            if ((self.check_sprite_inside(mag) and pygame.KEYDOWN and args[0].key == pygame.K_q) or (
                    self.check_sprite_inside(robber) and pygame.KEYDOWN and args[0].key == pygame.K_u)):
                if self.activate:
                    self.activate = False
                else:
                    self.activate = True

    def check_sprite_inside(self, sprite):
        """
        Проверяет, находится ли спрайт большей частью внутри двери.

        :param sprite: Игровой спрайт (маг или вор).
        :return: True, если большая часть спрайта внутри двери, иначе False.
        """
        intersection = self.rect.clip(sprite.rect)

        sprite_area = sprite.rect.width * sprite.rect.height
        intersection_area = intersection.width * intersection.height

        return intersection_area > 0.25 * sprite_area


class GorizontalDoor(spritesBase.GameSprite):
    image = load_image("gorizontaldoor.png")

    def __init__(self, *group, x, y):
        super().__init__(GorizontalDoor.image, x, y, *group, width=80, height=40)
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
            levelMap[self.get_top_cell_y()] = levelMap[self.get_top_cell_y()][:self.get_left_cell_x()] + ".." + \
                                              levelMap[self.get_top_cell_y()][self.get_left_cell_x() + 2:]
            self.image = self.imghide
            # print("\n".join(levelMap))
        else:
            levelMap[self.get_top_cell_y()] = levelMap[self.get_top_cell_y()][:self.get_left_cell_x()] + "--" + \
                                              levelMap[self.get_top_cell_y()][self.get_left_cell_x() + 2:]
            self.image = self.image_original
            # for i in self.button:
            #     print(i.activate)


class Box(spritesBase.GameSprite):
    image = load_image("Box.png")

    def __init__(self, *group, x, y, robber, levelMap):
        super().__init__(Box.image, x, y, *group, width=40)
        self.robber = robber
        self.levelMap = levelMap


class Spike(spritesBase.GameSprite):
    image = load_image("spike.png")

    def __init__(self, *group, x, y, robber, mag, levelMap):
        super().__init__(Box.image, x, y, *group, width=40)
        self.robber = robber
        self.levelMap = levelMap
        self.mag = mag


class VerticalDoor(spritesBase.GameSprite):
    image = load_image("verticaldoor.png")

    def __init__(self, *group, x, y):
        super().__init__(VerticalDoor.image, x, y, *group, width=40, height=80)
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
            levelMap[self.get_top_cell_y()] = levelMap[self.get_top_cell_y()][:self.get_left_cell_x()] + "." + levelMap[
                                                                                                                   self.get_top_cell_y()][
                                                                                                               self.get_left_cell_x() + 1:]
            levelMap[self.get_top_cell_y() + 1] = levelMap[self.get_top_cell_y() + 1][:self.get_left_cell_x()] + "." + \
                                                  levelMap[self.get_top_cell_y() + 1][self.get_left_cell_x() + 1:]
            self.image = self.imghide
            # print("\n".join(levelMap))
        else:
            levelMap[self.get_top_cell_y()] = levelMap[self.get_top_cell_y()][:self.get_left_cell_x()] + "|" + levelMap[
                                                                                                                   self.get_top_cell_y()][
                                                                                                               self.get_left_cell_x() + 1:]
            levelMap[self.get_top_cell_y() + 1] = levelMap[self.get_top_cell_y() + 1][:self.get_left_cell_x()] + "|" + \
                                                  levelMap[self.get_top_cell_y() + 1][self.get_left_cell_x() + 1:]
            self.image = self.image_original
            # for i in self.button:
            #     print(i.activate)


class Monsters(spritesBase.MovableGameSprite):
    image = load_image("monster.png")

    def __init__(self, *group, x, y, levelMap, mag, robber):
        super().__init__(Monsters.image, x, y, *group, width=40, height=40, level_map=levelMap, hspeed=120)
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
        if args and pygame.sprite.collide_mask(self, self.robber):
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.kill()
            else:
                self.robber.alive = False


class Mag(spritesBase.MovableGameSprite):
    image = load_image("mag.png")

    def __init__(self, *group, x, y, levelMap):
        super().__init__(Mag.image, x, y, *group, width=40, height=40, level_map=levelMap, hspeed=240)
        self.alive = True

    def can_move(self, block_content):
        return block_content in [".", "$", "@", "X", "7", "*", "0", "T"]

    def can_stay(self, block_content):
        return not (block_content in [".", "$", "@", "X", "7", "*", "0", "T"])

    def do_update(self, *args):
        if args and pygame.key.get_pressed()[pygame.K_d]:
            self.set_direction(True)
            self.move()
        if args and pygame.key.get_pressed()[pygame.K_a]:
            self.set_direction(False)
            self.move()
        if args and pygame.key.get_pressed()[pygame.K_w]:
            self.jump()


class Robber(spritesBase.MovableGameSprite):
    image = load_image("robber.png")

    def __init__(self, *group, x, y, levelMap):
        super().__init__(Robber.image, x, y, *group, width=40, height=80, level_map=levelMap, hspeed=240)
        self.alive = True

    def can_move(self, block_content):
        return block_content in [".", "$", "@", "X", "7", "*", "0", "T"]

    def can_stay(self, block_content):
        return not (block_content in [".", "$", "@", "X", "7", "*", "0", "T"])

    def do_update(self, *args):
        if args and pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.set_direction(True)
            self.move()
        if args and pygame.key.get_pressed()[pygame.K_LEFT]:
            self.set_direction(False)
            self.move()
        if args and pygame.key.get_pressed()[pygame.K_UP]:
            self.jump()

    # def update(self):
    #     if args and args[0].type == pygame.MOUSEBUTTONDOWN:
    #         self.image = self.image_boom
