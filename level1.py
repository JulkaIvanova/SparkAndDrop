import ClassSprites
import pygame
import os
import sys

import commonConsts




pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)

def printtext(cnt):
    font = pygame.font.Font(None, 100)
    text = font.render(str(cnt), True, (255, 0, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))

def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class mutableInt:
    def __init__(self):
        self.cnt = 0

# class mutableLevelMap:
#     def __init__(self, level):
#         self.level = level

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
gorizontaldoors = []
levers = []
buttons = []
verticaldoors = []
with open("data\level_1.txt") as f:
    level = f.read()
# cnt = 0
# for i in level:
#     if i == "#":
#         cnt += 1
# d = -1
# k = -1
# t = -1
# o = -1
# level = level.split("\n")
# for i in range(len(level)):
#     if i == d:
#         d = -1
#         continue
#     if t == i:
#         t = -1
#         continue
#     if o == i:
#         o = -1
#         continue
#     for j in range(len(level[i])):
#         if j == k:
#             k = -1
#             continue
#         if level[i][j] == "T":
#             d = i + 1
#             # level[i+1]=level[i+1].split()
#             level[i+1] = level[i+1][:j]+"T"+level[i+1][j+1:]
#         if level[i][j] == "I":
#             t = i + 1
#             # level[i+1]=level[i+1].split()
#             level[i+1] = level[i+1][:j]+"I"+level[i+1][j+1:]
#         if level[i][j] == "|":
#             o = i + 1
#             # level[i+1]=level[i+1].split()
#             level[i+1] = level[i+1][:j]+"|"+level[i+1][j+1:]
#         if level[i][j] == "-":
#             # level[i] = level[i].split()
#             level[i] = level[i][:j+1]+"-"+level[i][j+2:]
#             k = j+1

        
level = level.split("\n")
coins = 0
all_sprites_bloks = pygame.sprite.Group()
all_sprites_coins = pygame.sprite.Group()
all_sprites_door = pygame.sprite.Group()
all_sprites_magicdoor = pygame.sprite.Group()
all_sprites_button = pygame.sprite.Group()
all_sprites_lever = pygame.sprite.Group()
all_sprites_gorizontaledoors = pygame.sprite.Group()
all_sprites_mag = pygame.sprite.Group()
all_sprites_robber = pygame.sprite.Group()
all_sprites_verticaldoors = pygame.sprite.Group()
all_monsterss = pygame.sprite.Group()
for i in range(len(level)):
    for j in range(len(level[i])):
        if level[i][j] == "#":
            ClassSprites.Block(all_sprites_bloks, x = j*40, y = i*40)
        elif level[i][j] == "7":
            ClassSprites.Coin(all_sprites_coins, x = j*40, y = i*40)
            coins += 1
        elif level[i][j] == "I":
            ClassSprites.MagicDoor(all_sprites_magicdoor, x = j*40, y = i*40)
        elif level[i][j] == "T":
            ClassSprites.Door(all_sprites_door, x = j*40, y = i*40)
        elif level[i][j] == "0":
            buttons.append(ClassSprites.Button(all_sprites_button, x = j*40, y = i*40))
        elif level[i][j] == "*":
            levers.append(ClassSprites.Lever(all_sprites_lever, x = j*40, y = i*40))
        elif level[i][j] == "-":
            gorizontaldoors.append(ClassSprites.GorizontalDoor(all_sprites_gorizontaledoors, x = j*40, y = i*40))
        elif level[i][j] == "@":
            robber = ClassSprites.Robber(all_sprites_robber, x = j*40, y = i*40)
        elif level[i][j] == "$":
            mag = ClassSprites.Mag(all_sprites_mag, x = j*40, y = i*40)
        elif level[i][j] == "|":
            verticaldoors.append(ClassSprites.VerticalDoor(all_sprites_verticaldoors, x = j*40, y = i*40))
        elif level[i][j] == "X":
            ClassSprites.Monsters(all_monsterss, x = j*40, y = i*40, levelMap=level)
            
d = -1
k = -1
t = -1
o = -1
for i in range(len(level)):
    if i == d:
        d = -1
        continue
    if t == i:
        t = -1
        continue
    if o == i:
        o = -1
        continue
    for j in range(len(level[i])):
        if j == k:
            k = -1
            continue
        if level[i][j] == "T":
            d = i + 1
            # level[i+1]=level[i+1].split()
            level[i+1] = level[i+1][:j]+"T"+level[i+1][j+1:]
        if level[i][j] == "I":
            t = i + 1
            # level[i+1]=level[i+1].split()
            level[i+1] = level[i+1][:j]+"I"+level[i+1][j+1:]
        if level[i][j] == "|":
            o = i + 1
            # level[i+1]=level[i+1].split()
            level[i+1] = level[i+1][:j]+"|"+level[i+1][j+1:]
        if level[i][j] == "-":
            # level[i] = level[i].split()
            level[i] = level[i][:j+1]+"-"+level[i][j+2:]
            k = j+1

coinsCollect = mutableInt()
for i in range(len(gorizontaldoors)):
    if i == 0:
        cnt = ''
    else:
        cnt = f'{i}'
    gorizontaldoors[i].connect(cnt, levers[i], "lever")
verticaldoors[0].connect('', buttons, "button", 2)
#levelmap = mutableLevelMap(level)
if __name__ == "__main__":
    running = True
    flag = False
    pos = (0, 0)
     
    pygame.display.set_caption("Свой курсор мыши")
    image = load_image("background_lvl_1.jpg")
    image = pygame.transform.scale(image, (1200, 800))
    
    while running:
        eventt = None
        # cnt+=1
        # if cnt>3:
        #     cnt=0
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                eventt = event
        if not(mag.alive) or not(robber.alive):
            running = False
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
        all_monsterss.draw(screen)
        #board.render(screen)
        #if cnt==0:
        all_sprites_mag.update(eventt, levelMap=level)
        all_monsterss.update(eventt, mag=mag, robber=robber, levelMap=level)
        all_sprites_coins.update(eventt, mag=mag, robber=robber, coinsCollect=coinsCollect)
        all_sprites_magicdoor.update(eventt, mag=mag, levelMap=level)
        all_sprites_verticaldoors.draw(screen)
        all_sprites_lever.update(eventt, mag=mag, robber=robber)
        all_sprites_button.update(eventt, mag=mag, robber=robber)
        #mag.draw(screen)
        # screen.blit(mag.image, (mag.xpos, mag.ypos))
        # mag.falling(level)
        # all_sprites_mag[0].falling(level)
        for i in gorizontaldoors:
            i.check(level)
        verticaldoors[0].check(level)
        printtext(str(mag.left_x)+" "+str(mag.right_x)+" "+str(mag.top_y)+" "+str(mag.bottom_y))
        clock.tick(commonConsts.FPS)
        pygame.display.flip()
    
    pygame.quit()