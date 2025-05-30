import pygame
import os
import sys
import sounds


class Ruls:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(self.size)

    def load_image(self, name, colorkey=None):
        fullname = os.path.join("data", name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        return pygame.image.load(fullname)

    def start(self):
        cursor_image = self.load_image("arrow.png")
        cursor_rect = cursor_image.get_rect()
        imgs = ['p_1.png', 'p_2.png', 'p_3.png', 'p_4.png', 'p_5.png', 'p_6.png', 'p_7.png', 'p_8.png']
        n = 0
        img = pygame.transform.scale(self.load_image(imgs[n]), (1200, 800))
        running = True
        pygame.display.set_caption("Самое ценное сокровище")
        pygame.display.set_icon(self.load_image("icon.png"))
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    sounds.book_sound.play()
                    if n >= len(imgs) - 1:
                        running = False
                        break
                    n += 1
                    img = pygame.transform.scale(self.load_image(imgs[n]), (1200, 800))
            self.screen.blit(img, (0, 0))
            # Обновляем позицию курсора
            cursor_rect.center = pygame.mouse.get_pos()
            # Рисуем новый курсор на фоне
            if cursor_rect.center[0] > 0 and cursor_rect.center[1] > 0 and cursor_rect.center[1] < 799 and cursor_rect.center[0] < 1199:
                self.screen.blit(cursor_image, cursor_rect)
            pygame.display.flip()
