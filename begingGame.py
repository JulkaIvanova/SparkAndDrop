import pygame
import os
import sys
import levels
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





class BegingGame:
    def __init__(self):
        self.board = Board(600, 600)
        self.board.set_view(0, 0, 40)
        pygame.init()
        self.size = self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(self.size)


    def load_image(self, name, colorkey=None):
        fullname = os.path.join("data", name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image
    
    def start(self):
        img = self.load_image("begging.png")
        img = pygame.transform.scale(img, (1200, 800))
        cnt = 0 
        running = True
        flag = False
        pos = (0, 0)
        pygame.display.set_caption("Свой курсор мыши")
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if cnt >= 1:
                        levels.Levels().start()
                    img = self.load_image("two.png")
                    img = pygame.transform.scale(img, (1200, 800))
                    cnt += 1
            self.screen.blit(img, (0, 0))
            

            

            pygame.display.flip()

        pygame.quit()
