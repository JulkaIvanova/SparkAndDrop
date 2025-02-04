import pygame
import ClassSprites
import os
import sys
from boxService import BoxService
import commonConsts
import sounds
import sqlite_start


class mutableInt:
    def __init__(self):
        self.cnt = 0


class Level:

    def __init__(self, levelMap: list, background: pygame):
        self.levelMap = levelMap
        self.background = pygame.transform.scale(background, (1200, 800))
        self.all_sprites_bloks = pygame.sprite.Group()
        self.all_sprites_coins = pygame.sprite.Group()
        self.all_sprites_door = pygame.sprite.Group()
        self.all_sprites_magicdoor = pygame.sprite.Group()
        self.all_sprites_button = pygame.sprite.Group()
        self.all_sprites_lever = pygame.sprite.Group()
        self.all_sprites_gorizontaledoors = pygame.sprite.Group()
        self.all_sprites_mag = pygame.sprite.Group()
        self.all_sprites_robber = pygame.sprite.Group()
        self.all_sprites_verticaldoors = pygame.sprite.Group()
        self.all_monsterss = pygame.sprite.Group()
        self.all_sprites_spikes = pygame.sprite.Group()
        self.all_sprites_box = pygame.sprite.Group()
        self.coins = 0
        self.coinsCollect = mutableInt()
        self.doors = []
        self.gorizontaldoors = []
        self.levers = []
        self.buttons = []
        self.verticaldoors = []
        self.clock = pygame.time.Clock()
        self.running = True
        self.boxs = []
        self.monsterss = []

    def init(self):
        self.initialization()
        self.correct_levelMap()
        pygame.init()
        size = width, height = 1200, 800
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Самое ценное сокровище")
        pygame.display.set_icon(load_image("icon.png"))

    def initialization(self):
        box_service = BoxService(self.levelMap)
        for i in range(len(self.levelMap)):
            for j in range(len(self.levelMap[i])):
                if self.levelMap[i][j] == "@":
                    self.robber = ClassSprites.Robber(self.all_sprites_robber, x=j * 40, y=i * 40,
                                                      levelMap=self.levelMap, box_service=box_service)
                elif self.levelMap[i][j] == "$":
                    self.mag = ClassSprites.Mag(self.all_sprites_mag, x=j * 40, y=i * 40, levelMap=self.levelMap,
                                                box_service=box_service)
        for i in range(len(self.levelMap)):
            for j in range(len(self.levelMap[i])):
                if self.levelMap[i][j] == "#":
                    ClassSprites.Block(self.all_sprites_bloks, x=j * 40, y=i * 40)
                elif self.levelMap[i][j] == "7":
                    ClassSprites.Coin(self.all_sprites_coins, x=j * 40, y=i * 40)
                    self.coins += 1
                elif self.levelMap[i][j] == "I":
                    ClassSprites.MagicDoor(self.all_sprites_magicdoor, x=j * 40, y=i * 40)
                elif self.levelMap[i][j] == "T":
                    self.doors.append(ClassSprites.Door(self.all_sprites_door, x=j * 40, y=i * 40))
                elif self.levelMap[i][j] == "0":
                    self.buttons.append(ClassSprites.Button(self.all_sprites_button, x=j * 40, y=i * 40))
                elif self.levelMap[i][j] == "*":
                    self.levers.append(ClassSprites.Lever(self.all_sprites_lever, x=j * 40, y=i * 40))
                elif self.levelMap[i][j] == "-":
                    self.gorizontaldoors.append(
                        ClassSprites.GorizontalDoor(self.all_sprites_gorizontaledoors, x=j * 40, y=i * 40))
                elif self.levelMap[i][j] == "|":
                    self.verticaldoors.append(
                        ClassSprites.VerticalDoor(self.all_sprites_verticaldoors, x=j * 40, y=i * 40))
                elif self.levelMap[i][j] == "X":
                    self.monsterss.append(
                        ClassSprites.Monsters(self.all_monsterss, x=j * 40, y=i * 40, levelMap=self.levelMap,
                                              mag=self.mag, robber=self.robber, box_service=box_service))
                elif self.levelMap[i][j] == "B":
                    self.boxs.append(ClassSprites.Box(self.all_sprites_box, x=j * 40, y=i * 40, levelMap=self.levelMap,
                                                      robber=self.robber, mag=self.mag, box_service=box_service))
                elif self.levelMap[i][j] == "S":
                    ClassSprites.Spike(self.all_sprites_spikes, x=j * 40, y=i * 40, levelMap=self.levelMap,
                                       robber=self.robber, mag=self.mag)

    def correct_levelMap(self):
        d = -1
        k = -1
        t = -1
        o = -1
        for i in range(len(self.levelMap)):
            if i == d:
                d = -1
                continue
            if t == i:
                t = -1
                continue
            if o == i:
                o = -1
                continue
            for j in range(len(self.levelMap[i])):
                if j == k:
                    k = -1
                    continue
                if self.levelMap[i][j] == "T":
                    d = i + 1
                    self.levelMap[i + 1] = self.levelMap[i + 1][:j] + "T" + self.levelMap[i + 1][j + 1:]
                if self.levelMap[i][j] == "I":
                    t = i + 1
                    self.levelMap[i + 1] = self.levelMap[i + 1][:j] + "I" + self.levelMap[i + 1][j + 1:]
                if self.levelMap[i][j] == "|":
                    o = i + 1
                    self.levelMap[i + 1] = self.levelMap[i + 1][:j] + "|" + self.levelMap[i + 1][j + 1:]
                if self.levelMap[i][j] == "-":
                    self.levelMap[i] = self.levelMap[i][:j + 1] + "-" + self.levelMap[i][j + 2:]
                    k = j + 1

    def bild(self, screen: pygame.display):
        screen.blit(self.background, (0, 0))
        self.all_sprites_bloks.draw(screen)
        self.all_sprites_coins.draw(screen)
        self.all_sprites_door.draw(screen)
        self.all_sprites_magicdoor.draw(screen)
        self.all_sprites_button.draw(screen)
        self.all_sprites_lever.draw(screen)
        self.all_sprites_gorizontaledoors.draw(screen)
        self.all_sprites_mag.draw(screen)
        self.all_sprites_robber.draw(screen)
        self.all_monsterss.draw(screen)
        self.all_sprites_verticaldoors.draw(screen)
        self.all_sprites_box.draw(screen)
        self.all_sprites_box.draw(screen)
        self.all_sprites_spikes.draw(screen)

    def display_message(self, message, color, pos=None):
        """Отображение сообщения на экране."""
        font = pygame.font.Font(None, 74)  # Размер шрифта
        text = font.render(message, True, color)
        if pos is None:
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        else:
            text_rect = text.get_rect(center=(pos[0], pos[1]))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        # Задержка перед завершением
        pygame.time.wait(1500)

    def show_win_screen(self, time, G):
        """Показ окна победы."""
        self.screen.fill((0, 128, 0))  # Зелёный фон
        self.display_message("Победа!", (255, 255, 255))
        self.show_resalt_screen(time, G)

    def show_resalt_screen(self, time, G):
        """Показ окна результатов."""
        self.screen.fill((169, 69, 69))
        self.display_message("Результаты:", (255, 255, 255), (600, 200))
        self.display_message(f"Собрано монет: {self.coinsCollect.cnt}/{self.coins}", (255, 255, 255), (600, 300))
        self.display_message(f"Времени затрачено: {time} сек", (255, 255, 255), (600, 400))
        res = sqlite_start.get_level_info(G)
        if res is not None:
            self.display_message(f"Рекордное время: {int(res[0])} сек", (255, 255, 255), (600, 500))
            self.display_message(f"Наибольшее количество монет: {res[1]}/{self.coins}", (255, 255, 255), (600, 600))

    def show_lose_screen(self):
        """Показ окна поражения."""
        self.screen.fill((128, 0, 0))  # Красный фон
        self.display_message("Поражение!", (255, 255, 255))


class LevelOne(Level):
    def __init__(self, levelMap, background):
        super().__init__(levelMap, background)

    def paint(self):
        self.init()
        self.time = pygame.time.get_ticks()
        for i in range(len(self.gorizontaldoors)):
            if i == 0:
                cnt = ''
            else:
                cnt = f'{i}'
            self.gorizontaldoors[i].connect(cnt, self.levers[i], "lever")
        self.verticaldoors[0].connect('', self.buttons, "button", 2)
        while self.running:
            eventt = None
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    eventt = event

            # Проверка условий поражения
            if not self.mag.alive or not self.robber.alive:
                sounds.loose_sound.play()
                self.show_lose_screen()
                self.running = False
                break

            # Проверка условий победы
            if self.doors[0].near_door and self.doors[1].near_door:
                time = (pygame.time.get_ticks() - self.time) // 1000
                sqlite_start.update_user_progress(1, self.coinsCollect.cnt, time)
                sounds.win_sound.play()
                self.show_win_screen(time, 1)
                self.running = False
                break

            self.bild(self.screen)
            self.all_sprites_mag.update(eventt)
            self.all_sprites_robber.update(eventt)
            self.all_monsterss.update(eventt)
            self.all_sprites_coins.update(eventt, mag=self.mag, robber=self.robber, coinsCollect=self.coinsCollect)
            self.all_sprites_magicdoor.update(eventt, mag=self.mag, levelMap=self.levelMap)
            self.all_sprites_lever.update(eventt, mag=self.mag, robber=self.robber)
            self.all_sprites_button.update(eventt, mag=self.mag, robber=self.robber)
            self.all_sprites_door.update(eventt, mag=self.mag, robber=self.robber, levelMap=self.levelMap)
            for i in self.gorizontaldoors:
                i.check(self.levelMap)
            self.verticaldoors[0].check(self.levelMap)
            self.clock.tick(commonConsts.FPS)
            pygame.display.flip()


class LevelTwo(Level):
    def __init__(self, levelMap, background):
        super().__init__(levelMap, background)

    def paint(self):
        self.init()
        self.time = pygame.time.get_ticks()
        self.gorizontaldoors[0].connect('2', self.buttons[0], "button")
        self.gorizontaldoors[1].connect('1', self.buttons[2], "button")
        self.verticaldoors[0].connect('', self.buttons[1], "button")
        self.verticaldoors[1].connect('', self.buttons[1], "button")
        self.verticaldoors[2].connect('3', self.buttons[4], "button")
        self.verticaldoors[3].connect('4', self.buttons[3], "button")

        while self.running:
            eventt = None
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    eventt = event

            # Проверка условий поражения
            if not self.mag.alive or not self.robber.alive:
                sounds.loose_sound.play()
                self.show_lose_screen()
                self.running = False
                break

            # Проверка условий победы
            if self.doors[0].near_door and self.doors[1].near_door:
                time = (pygame.time.get_ticks() - self.time) // 1000
                sqlite_start.update_user_progress(2, self.coinsCollect.cnt, time)
                sounds.win_sound.play()
                self.show_win_screen(time, 2)
                self.running = False
                break

            # Основной цикл отрисовки и обновления объектов
            self.bild(self.screen)
            self.all_sprites_mag.update(eventt)
            self.all_sprites_robber.update(eventt)
            self.all_monsterss.update(eventt)
            self.all_sprites_coins.update(eventt, mag=self.mag, robber=self.robber, coinsCollect=self.coinsCollect)
            self.all_sprites_magicdoor.update(eventt, mag=self.mag, levelMap=self.levelMap)
            self.all_sprites_lever.update(eventt, mag=self.mag, robber=self.robber)
            self.all_sprites_button.update(eventt, mag=self.mag, robber=self.robber, boxes=self.boxs)
            self.all_sprites_door.update(eventt, mag=self.mag, robber=self.robber, levelMap=self.levelMap)
            self.all_sprites_box.update(eventt)
            for i in self.gorizontaldoors:
                i.check(self.levelMap)
            for i in self.verticaldoors:
                i.check(self.levelMap)
            self.clock.tick(commonConsts.FPS)
            pygame.display.flip()


class LevelThree(Level):
    def __init__(self, levelMap, background):
        super().__init__(levelMap, background)

    def paint(self):
        self.init()
        self.time = pygame.time.get_ticks()
        self.verticaldoors[0].connect('5', self.levers[0], "lever")
        self.gorizontaldoors[0].connect('2', self.levers[1], "lever")
        self.gorizontaldoors[1].connect('1', self.levers[2], "lever")

        while self.running:
            eventt = None
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    eventt = event

            # Проверка условий поражения
            if not self.mag.alive or not self.robber.alive:
                sounds.loose_sound.play()
                self.show_lose_screen()
                self.running = False
                break

            # Проверка условий победы
            if self.doors[0].near_door and self.doors[1].near_door:
                time = (pygame.time.get_ticks() - self.time) // 1000
                sqlite_start.update_user_progress(3, self.coinsCollect.cnt, time)
                sounds.win_sound.play()
                self.show_win_screen(time, 3)
                self.running = False
                break

            self.bild(self.screen)
            self.all_sprites_mag.update(eventt)
            self.all_sprites_robber.update(eventt)
            self.all_monsterss.update(eventt)
            self.all_sprites_coins.update(eventt, mag=self.mag, robber=self.robber, coinsCollect=self.coinsCollect)
            self.all_sprites_magicdoor.update(eventt, mag=self.mag, levelMap=self.levelMap)
            self.all_sprites_lever.update(eventt, mag=self.mag, robber=self.robber)
            self.all_sprites_button.update(eventt, mag=self.mag, robber=self.robber)
            self.all_sprites_door.update(eventt, mag=self.mag, robber=self.robber, levelMap=self.levelMap)

            self.all_sprites_spikes.update(eventt)
            for i in self.gorizontaldoors:
                i.check(self.levelMap)
            for i in self.verticaldoors:
                i.check(self.levelMap)
            self.time = self.clock.tick(commonConsts.FPS)
            pygame.display.flip()


class LevelFour(Level):
    def __init__(self, levelMap, background):
        super().__init__(levelMap, background)

    def paint(self):
        self.init()
        self.time = pygame.time.get_ticks()

        self.gorizontaldoors[0].connect('1', self.buttons[1], "button")
        self.gorizontaldoors[4].connect('1', self.buttons[1], "button")

        self.gorizontaldoors[1].connect('2', self.buttons[0], "button")
        self.gorizontaldoors[3].connect('2', self.buttons[0], "button")
        self.gorizontaldoors[9].connect('2', self.buttons[0], "button")

        self.gorizontaldoors[5].connect('3', self.buttons[2], "button")
        self.gorizontaldoors[6].connect('3', self.buttons[2], "button")

        self.verticaldoors[0].connect('4', self.buttons[3], "button")
        self.gorizontaldoors[7].connect('4', self.buttons[3], "button")

        self.gorizontaldoors[2].connect('7', self.levers[0], "lever")

        self.gorizontaldoors[8].connect('5', self.buttons[4], "button")
        self.gorizontaldoors[10].connect('5', self.buttons[4], "button")
        self.verticaldoors[1].connect('8', self.buttons[4], "button")

        self.gorizontaldoors[13].connect('8', self.levers[1], "lever")

        self.verticaldoors[2].connect('9', self.buttons[5], "button")
        self.verticaldoors[3].connect('9', self.buttons[5], "button")

        self.gorizontaldoors[11].connect('10', self.buttons[6], "button")

        self.gorizontaldoors[12].connect('11', self.buttons[7], "button")

        while self.running:
            eventt = None
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    eventt = event

            # Проверка условий поражения
            if not self.mag.alive or not self.robber.alive:
                sounds.loose_sound.play()
                self.show_lose_screen()
                self.running = False
                break

            # Проверка условий победы
            if self.doors[0].near_door and self.doors[1].near_door:
                time = (pygame.time.get_ticks() - self.time) // 1000
                sqlite_start.update_user_progress(4, self.coinsCollect.cnt, time)
                sounds.win_sound.play()
                self.show_win_screen(time, 4)
                self.running = False
                break

            self.bild(self.screen)
            self.all_sprites_mag.update(eventt)
            self.all_sprites_robber.update(eventt)
            self.all_monsterss.update(eventt)
            self.all_sprites_coins.update(eventt, mag=self.mag, robber=self.robber, coinsCollect=self.coinsCollect)
            self.all_sprites_magicdoor.update(eventt, mag=self.mag, levelMap=self.levelMap)
            self.all_sprites_lever.update(eventt, mag=self.mag, robber=self.robber)
            self.all_sprites_button.update(eventt, mag=self.mag, robber=self.robber)
            self.all_sprites_door.update(eventt, mag=self.mag, robber=self.robber, levelMap=self.levelMap)
            self.all_sprites_spikes.update(eventt)

            for i in self.gorizontaldoors:
                i.check(self.levelMap)
            for i in self.verticaldoors:
                i.check(self.levelMap)
            self.clock.tick(commonConsts.FPS)
            pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
