import pygame
import os
import sys
import sounds


class EndGame:
    def __init__(self):
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
        img = self.load_image("three.png")
        cursor_image = self.load_image("arrow.png")
        cursor_rect = cursor_image.get_rect()
        img = pygame.transform.scale(img, (1200, 800))
        cnt = 0
        running = True
        pygame.display.set_caption("Самое ценное сокровище")

        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    sounds.book_sound.play()
                    if cnt == 0:
                        img = self.load_image("four.png")
                        img = pygame.transform.scale(img, (1200, 800))
                    elif cnt == 1:
                        img = self.load_image("end.png")
                        img = pygame.transform.scale(img, (1200, 800))
                    elif cnt == 2:
                        running = False
                    cnt += 1

            self.screen.blit(img, (0, 0))
            # Обновляем позицию курсора
            cursor_rect.center = pygame.mouse.get_pos()
            # Рисуем новый курсор на фоне
            if cursor_rect.center[0] > 0 and cursor_rect.center[1] > 0 and cursor_rect.center[1] < 799 and cursor_rect.center[0] < 1199:
                self.screen.blit(cursor_image, cursor_rect)
            pygame.display.flip()