import pygame
import begingGame
import sounds
import ruls
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


import os
import sys

board = Board(600, 600)
board.set_view(0, 0, 40)


pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


if __name__ == "__main__":
    # sqlite_start.create_database()

    running = True
    flag = False
    pos = (0, 0)
    pygame.mixer.music.load('data\\background_music.mp3')
    pygame.display.set_caption("Самое ценное сокровище")
    pygame.display.set_icon(load_image("icon.png"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if board.coordinates(event.pos) in [(12, 13), (12, 14), (13, 13), (13, 14), (14, 13), (14, 14), (15, 13), (15, 14), (16, 13), (16, 14), (17, 13), (17, 14)]:
                    sounds.choose_sound.play()
                    begingGame.BegingGame().start()
                if board.coordinates(event.pos) in [(2, 17), (2, 18), (1, 17), (1, 18)]:
                    sounds.choose_sound.play()
                    ruls.Ruls().start()

        image = load_image("r2.png")
        image = pygame.transform.scale(image, (1200, 800))
        screen.blit(image, pos)
        button = load_image("rules_button.png")
        button = pygame.transform.scale(button, (80, 80))
        screen.blit(button, (40, 680))
        # board.render(screen)
        

        pygame.display.flip()

    pygame.quit()

