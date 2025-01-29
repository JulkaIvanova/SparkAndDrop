import pygame
import os
import sys
import ClassLevel
import sounds
import endGame
import sqlite_start

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    pygame.Rect(
                        self.left + j * self.cell_size,
                        self.top + i * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                    1,
                )

    def coordinates(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if x >= self.width or y >= self.height or x < 0 or y < 0:
            return
        return (x, y)

def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image



class Levels:
    def __init__(self):
        self.board = Board(600, 600)
        self.board.set_view(0, 0, 40)
        pygame.init()
        self.size = self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        self.level = None

    # def load_image(self, name, colorkey=None):
    #     fullname = os.path.join("data", name)
    #     if not os.path.isfile(fullname):
    #         print(f"Файл с изображением '{fullname}' не найден")
    #         sys.exit()
    #     image = pygame.image.load(fullname)
    #     return image
    
    def start(self):
        running = True
        pos = (0, 0)
        cnt = 0
        pygame.display.set_caption("Свой курсор мыши")
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.board.coordinates(event.pos) in [(8, 4), (9, 4), (10, 4), (11, 4), (8, 5), (9, 5), (10, 5), (11, 5), (8, 6), (9, 6), (10, 6), (11, 6), (8, 7), (9, 7), (10, 7), (11, 7)]:
                        sounds.choose_sound.play()
                        if self.level is not None and self.level.running:
                            continue
                        with open("data\level_1.txt") as f:
                            level = f.read()   
                        self.level = ClassLevel.LevelOne(levelMap=level.split("\n"), background=load_image("background_lvl_1.jpg")).paint()
                        print("1")
                    elif self.board.coordinates(event.pos) in [(18, 4), (19, 4), (20, 4), (21, 4), (18, 5), (19, 5), (20, 5), (21, 5), (18, 6), (19, 6), (20, 6), (21, 6), (18, 7), (19, 7), (20, 7), (21, 7)]:
                        sounds.choose_sound.play()
                        # if self.level is not None and self.level.running:
                        #     continue
                        if not sqlite_start.check_level_completion(1):
                            continue
                        with open("data\level_2.txt") as f:
                            level = f.read()   
                        self.level = ClassLevel.LevelTwo(levelMap=level.split("\n"), background=load_image("background_lvl_2.jpg")).paint()
                        print("2")
                    elif self.board.coordinates(event.pos) in [(18, 11), (19, 11), (20, 11), (21, 11), (18, 12), (19, 12), (20, 12), (21, 12), (18, 13), (19, 13), (20, 13), (21, 13), (18, 14), (19, 14), (20, 14), (21, 14)]:
                        sounds.choose_sound.play()
                        if not sqlite_start.check_level_completion(2):
                            continue
                        with open("data\level_3.txt") as f:
                            level = f.read()   
                        self.level = ClassLevel.LevelThree(levelMap=level.split("\n"), background=load_image("background_lvl_3.jpg")).paint()
                        print("3")
                    elif self.board.coordinates(event.pos) in [(8, 11), (9, 11), (10, 11), (11, 11), (8, 12), (9, 12), (10, 12), (11, 12), (8, 13), (9, 13), (10, 13), (11, 13), (8, 14), (9, 14), (10, 14), (11, 14)]:
                        sounds.choose_sound.play()
                        if not sqlite_start.check_level_completion(3):
                            continue
                        with open("data\level_4.txt") as f:
                            level = f.read()   
                        self.level = ClassLevel.LevelFour(levelMap=level.split("\n"), background=load_image("background_lvl_4.jpg")).paint()
                        print("4")
                        if not sqlite_start.check_level_completion(4):
                            continue
                        endGame.EndGame().start()
                    elif self.board.coordinates(event.pos) in [(13, 16), (13, 17), (14, 16), (14, 17), (15, 16), (15, 17), (16, 16), (16, 17)]:
                        sounds.choose_sound.play()
                        running = False
                        print("exit")
            img = load_image("levels.png")
            img = pygame.transform.scale(img, (1200, 800))
            self.screen.blit(img, (0, 0))
            # self.board.render(self.screen)
            

            

            pygame.display.flip()
        # pygame.quit()
