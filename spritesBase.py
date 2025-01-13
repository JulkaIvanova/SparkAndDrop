import pygame
import commonConsts


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int, *group, width=0, height=0):
        super().__init__(*group)
        self.image = image
        if (width>0) or (height>0):
            if width==0:
                width=height
            if height==0:
                height=width
            self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def get_left_cell_x(self, offset = 0):
        return int((self.rect.left + offset) // commonConsts.BLOCK_SIZE)

    def get_right_cell_x(self, offset = 0):
        return int((self.rect.right - 1 + offset) // commonConsts.BLOCK_SIZE)

    def get_top_cell_y(self, offset = 0):
        return int((self.rect.top + offset) // commonConsts.BLOCK_SIZE)

    def get_bottom_cell_y(self, offset = 0):
        return int((self.rect.bottom - 1 + offset) // commonConsts.BLOCK_SIZE)
    
    # Следующие 4 функции принимают на вход иддекс блока и выравнивают по нему левый, правый, верхний или нижний край спрайта
    def set_left_cell_x(self, value):
        self.rect.left = value * commonConsts.BLOCK_SIZE

    def set_right_cell_x(self, value):
        self.rect.right = value * commonConsts.BLOCK_SIZE + commonConsts.BLOCK_SIZE

    def set_top_cell_y(self, value):
        self.rect.top = value * commonConsts.BLOCK_SIZE

    def set_bottom_cell_y(self, value):
        self.rect.bottom = value * commonConsts.BLOCK_SIZE + commonConsts.BLOCK_SIZE
    
class  MovableGameSprite(GameSprite):
    def __init__(self, image: pygame.Surface, x: int, y: int, *group, level_map, width=0, height=0, hspeed=0, vspeed=800, jump_height=3*commonConsts.BLOCK_SIZE, right_direction = False, left_direction_image: pygame.Surface = None):
        super().__init__(image, x, y, *group, width= width, height=height)
        self.hspeed = hspeed
        self.vspeed = vspeed
        self.level_map = level_map
        self.right_image = self.image
        self.left_image = left_direction_image
        self.jump_height = jump_height
        self.current_jump_height = 0
        self.jump_in_progress = False
        if self.left_image == None:
            self.left_image = pygame.transform.flip(self.image, True, False)

        self.set_direction(right_direction)

    def change_direction(self):
        self.set_direction(not self.right_direction)
        

    def set_direction(self, right: bool):
        self.right_direction = right
        if self.right_direction:
            self.image = self.right_image
        else:
            self.image = self.left_image
    
    def can_move(self, block_content):
        return True
    
    def can_stay(self, block_content):
        return True
    
    def can_jump_through(self, block_content):
        return not self.can_stay(block_content)
    
    def fall(self):
        if self.jump_in_progress:
            return
        
        distance = self.vspeed / commonConsts.FPS
        offset = 0
        if self.can_stay(self.level_map[self.get_bottom_cell_y(1)][self.get_left_cell_x()]) or self.can_stay(self.level_map[self.get_bottom_cell_y(1)][self.get_right_cell_x()]):
            return

        full_distance = True
        blocks = 0
        while offset<distance:
            offset+=commonConsts.BLOCK_SIZE
            if offset>distance:
                offset = distance
            if self.can_stay(self.level_map[self.get_bottom_cell_y(offset)][self.get_left_cell_x()]) or self.can_stay(self.level_map[self.get_bottom_cell_y(offset)][self.get_right_cell_x()]):
                full_distance = False
                break
            blocks+=1
        if full_distance:
            self.rect.top += distance
        else:
            self.set_bottom_cell_y(self.get_bottom_cell_y(1)+blocks)

    def _process_jump(self):
        if not self.jump_in_progress:
            return
        
        if not self.can_jump_through(self.level_map[self.get_top_cell_y(-1)][self.get_left_cell_x()]) or \
           not self.can_jump_through(self.level_map[self.get_top_cell_y(-1)][self.get_right_cell_x()]) or \
            self.current_jump_height>=self.jump_height:
            self.jump_in_progress = False
            self.current_jump_height = 0
            return

        distance = self.vspeed / commonConsts.FPS
        if (self.current_jump_height+distance)>self.jump_height:
            distance = self.jump_height - self.current_jump_height

        full_distance = True
        blocks = 0
        offset = 0
        while offset<distance:
            offset+=commonConsts.BLOCK_SIZE
            if offset>distance:
                offset = distance
            if not self.can_jump_through(self.level_map[self.get_top_cell_y(-offset)][self.get_left_cell_x()]) or \
               not self.can_jump_through(self.level_map[self.get_top_cell_y(-offset)][self.get_right_cell_x()]):
                full_distance = False
                break
            blocks+=1
        if full_distance:
            self.rect.top -= distance
            self.current_jump_height +=distance
            if self.current_jump_height>=self.jump_height:
                self.jump_in_progress = False
                self.current_jump_height = 0
        else:
            self.set_top_cell_y(self.get_top_cell_y()-blocks)
            self.jump_in_progress = False
            self.current_jump_height = 0
        
    def do_update(self):
        pass

    def jump(self):
        if self.jump_in_progress:
            return
        
        if not self.can_stay(self.level_map[self.get_bottom_cell_y(1)][self.get_left_cell_x()]) and not self.can_stay(self.level_map[self.get_bottom_cell_y(1)][self.get_right_cell_x()]):
            return

        self.jump_in_progress = True
        self._process_jump()

    def move(self, can_fall = True, flip_on_stop = False, distance = 0):
        if distance == 0:
            distance = self.hspeed // commonConsts.FPS  # При таком подходе скорость спрайта должна быть кратна fps, иначе она будет урезаться
        if distance == 0:
            return    
        
        #Пока предполагаем, что максимальная высота спрайта два блока
        full_distance = True
        offset=0
        last_success_right = self.get_right_cell_x()
        last_success_left = self.get_right_cell_x()
        while offset<distance:
            offset+=commonConsts.BLOCK_SIZE
            if offset>distance:
                offset = distance
            if self.right_direction:    
                right = self.get_right_cell_x(offset)
                left = self.get_left_cell_x(offset)
            else:
                right = self.get_right_cell_x(-offset)
                left = self.get_left_cell_x(-offset)
            # Если блок в котором находится спрайт не изменится, то проверки не нужны
            if right == self.get_right_cell_x() and left == self.get_left_cell_x():
                continue
            
            if self.right_direction:
                block_front = right
                block_back = left    
            else:
                block_back = right
                block_front = left

            if not self.can_move(self.level_map[self.get_bottom_cell_y()][block_front]) or not self.can_move(self.level_map[self.get_top_cell_y()][block_front]):
                full_distance = False
                if self.right_direction:
                    self.set_right_cell_x(last_success_right)
                else:
                    self.set_left_cell_x(last_success_left)
                if flip_on_stop:
                    self.change_direction()
                break
            if not self.can_stay(self.level_map[self.get_bottom_cell_y()+1][block_front]):
                if not can_fall:
                    full_distance = False
                    if self.right_direction:
                        self.set_right_cell_x(last_success_right)
                    else:
                        self.set_left_cell_x(last_success_left)
                    if flip_on_stop:
                        self.change_direction()
                        break
                else:
                    if not self.can_stay(self.level_map[self.get_bottom_cell_y()+1][block_back]):
                        #full_distance = False
                        #if self.right_direction:
                        #    self.set_right_cell_x(right)
                        #else:
                        #    self.set_left_cell_x(left)
                        self.fall()
                        #break
            last_success_right = right
            last_success_left = left
                
        if full_distance:
            if self.right_direction:
                self.rect.left = self.rect.left + distance
            else:
                self.rect.left = self.rect.left - distance

    
    def update(self, *args):
        self.fall()
        self._process_jump()
        self.do_update(*args)   