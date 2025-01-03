import ClassSprites
import pygame
import os
import sys




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

clock = pygame.time.Clock()  
board = Board(600, 600)
board.set_view(0, 0, 40)
with open("data\level_1.txt") as f:
    level = f.read()
# cnt = 0
# for i in level:
#     if i == "#":
#         cnt += 1
level = level.split("\n")
print(level)
all_sprites_bloks = pygame.sprite.Group()
all_sprites_coins = pygame.sprite.Group()
all_sprites_door = pygame.sprite.Group()
all_sprites_magicdoor = pygame.sprite.Group()
all_sprites_button = pygame.sprite.Group()
all_sprites_lever = pygame.sprite.Group()
all_sprites_gorizontaledoors = pygame.sprite.Group()
all_sprites_mag = pygame.sprite.Group()
all_sprites_robber = pygame.sprite.Group()
for i in range(len(level)):
    for j in range(len(level[i])):
        if level[i][j] == "#":
            ClassSprites.Block(all_sprites_bloks, x = j*40, y = i*40)
        elif level[i][j] == "7":
            ClassSprites.Coin(all_sprites_coins, x = j*40, y = i*40)
        elif level[i][j] == "I":
            ClassSprites.MagicDoor(all_sprites_magicdoor, x = j*40, y = i*40)
        elif level[i][j] == "T":
            ClassSprites.Door(all_sprites_door, x = j*40, y = i*40)
        elif level[i][j] == "0":
            ClassSprites.Button(all_sprites_button, x = j*40, y = i*40)
        elif level[i][j] == "*":
            ClassSprites.Lever(all_sprites_lever, x = j*40, y = i*40)
        elif level[i][j] == "-":
            ClassSprites.GorizontalDoor(all_sprites_gorizontaledoors, x = j*40, y = i*40)
        elif level[i][j] == "@":
            ClassSprites.Robber(all_sprites_robber, x = j*40, y = i*40)
        elif level[i][j] == "$":
            mag = ClassSprites.Mag(all_sprites_mag, x = j*40, y = i*40, clock=clock)    

if __name__ == "__main__":
    running = True
    flag = False
    pos = (0, 0)
     
    pygame.display.set_caption("Свой курсор мыши")
    image = load_image("background_lvl_1.jpg")
    image = pygame.transform.scale(image, (1200, 800))
    eventt = None
    while running:
        # cnt+=1
        # if cnt>3:
        #     cnt=0
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                eventt = event


        
        screen.blit(image, pos)
        all_sprites_bloks.draw(screen)
        all_sprites_coins.draw(screen)
        all_sprites_door.draw(screen)
        all_sprites_magicdoor.draw(screen)
        all_sprites_button.draw(screen)
        all_sprites_lever.draw(screen)
        all_sprites_gorizontaledoors.draw(screen)
        all_sprites_mag.draw(screen)
        all_sprites_robber.draw(screen)
        # board.render(screen)
        #if cnt==0:
        all_sprites_mag.update(eventt, levelMap=level)
        #mag.draw(screen)
        # screen.blit(mag.image, (mag.xpos, mag.ypos))
        # mag.falling(level)
        # all_sprites_mag[0].falling(level)

        pygame.display.flip()

    pygame.quit()