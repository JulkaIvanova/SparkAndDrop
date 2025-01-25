import pygame
import os
import sys
import levels
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
            

            

            pygame.display.flip()

# if __name__ == "__main__":   
#     EndGame().start() 