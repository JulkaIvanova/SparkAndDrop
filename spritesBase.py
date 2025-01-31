import pygame
from boxService import BoxService
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
    
class AnimatedSprite(GameSprite):
    def __init__(self, image: pygame.Surface, x: int, y: int, *group, width=0, height=0):
        super().__init__(image, x, y, *group)
        self.frames = []
        
        self._cut_sheet(image, width, height)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.cur_animation = 0
        self.slowdown_step = 0
        self.animation_slowdown = 10
        self.animations = []
        self.rect.x = x
        self.rect.y = y

    def add_animation(self, frame_seq):
        self.animations.append(frame_seq)

    def play_animation(self, animation_number: int = 0, slowdown = 10):
        if animation_number == self.cur_animation:
            return
        self.animation_slowdown = slowdown
        self.cur_animation = animation_number
        self.cur_frame = -1
        self.slowdown_step = 0


    def _cut_sheet(self, sheet: pygame.Surface, frame_width: int, frame_height: int):        
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()
        if (frame_width==0) or (frame_width>sheet_width):
            frame_width = sheet_width
        if (frame_height==0) or (frame_height>sheet_height):
            frame_height = sheet_height

        self.rect = pygame.Rect(0, 0, frame_width, frame_height)

        if (frame_width==sheet_width) and (frame_height==sheet_height):
            self.frames.append(sheet)
            return

        for i in range(0, sheet_width, frame_width):
            if (i+self.rect.width)>sheet_width:
                break
            for j in range(0, sheet_height, frame_height):
                if (j+self.rect.height)>sheet_height:
                    break
                frame_location = (i, j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def transform_frame(self, original_frame: pygame.Surface) -> pygame.Surface:
        return original_frame

    def update(self, *args):
        if self.cur_animation>=len(self.animations): # если в списке нет указанной анимации, то проигрываем все кадры
            if (self.cur_frame == -1) or (self.cur_frame>=len(self.frames)): # только запустили анимацию, либо прошли весь цикл
                self.cur_frame = 0
                self.slowdown_step=0
            self.slowdown_step+=1
            self.image = self.transform_frame(self.frames[self.cur_frame])
        else:
            if (self.cur_frame == -1) or (self.cur_frame>=len(self.animations[self.cur_animation])): # только запустили анимацию, либо прошли весь цикл
                self.cur_frame = 0
                self.slowdown_step=0
            self.slowdown_step+=1
            self.image = self.transform_frame(self.frames[self.animations[self.cur_animation][self.cur_frame]])

        if self.slowdown_step>=self.animation_slowdown:
            self.slowdown_step = 0
            self.cur_frame+=1 

class  MovableGameSprite(AnimatedSprite):
    def __init__(self, image: pygame.Surface, x: int, y: int, *group, level_map, box_service: BoxService, width=0, height=0, hspeed=0, vspeed=800, jump_height=3*commonConsts.BLOCK_SIZE, right_direction = False):
        super().__init__(image, x, y, *group, width= width, height=height)
        self.hspeed = hspeed
        self.vspeed = vspeed
        self.level_map = level_map
        self.jump_height = jump_height
        self.current_jump_height = 0
        self.jump_in_progress = False
        self.set_direction(right_direction)
        self.box_service = box_service
        self.was_stay = True

    def change_direction(self):
        self.set_direction(not self.right_direction)
        

    def set_direction(self, right: bool):
        self.right_direction = right

    def transform_frame(self, original_frame: pygame.Surface) -> pygame.Surface:
        if self.right_direction:
            return original_frame
        return pygame.transform.flip(original_frame, True, False)
    
    def get_stay_animation(self) -> int:
        return 0
    
    def get_move_animation(self) -> int:
        return 0
    
    def get_jump_animation(self) -> int:
        return 0
    
    def get_fall_animation(self) -> int:
        return 0

    
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
        
        self.play_animation(self.get_fall_animation())
        self.was_stay = False

        #full_distance = True
        blocks = 0
        while offset<distance:
            offset+=commonConsts.BLOCK_SIZE
            if offset>distance:
                offset = distance
            if self.can_stay(self.level_map[self.get_bottom_cell_y(offset)][self.get_left_cell_x()]) or \
               self.can_stay(self.level_map[self.get_bottom_cell_y(offset)][self.get_right_cell_x()]):
                distance = (self.get_bottom_cell_y(1)+blocks + 1) * commonConsts.BLOCK_SIZE - self.rect.bottom
                break
            blocks+=1

        distance = self.box_service.fallThroughBoxes(self, distance)
        self.rect.top += distance

        # if full_distance:
        #     self.rect.top += distance
        # else:
        #     self.set_bottom_cell_y(self.get_bottom_cell_y(1)+blocks)

    def _process_jump(self):
        if not self.jump_in_progress:
            return
        
        self.play_animation(self.get_jump_animation())
        self.was_stay = False

        if not self.can_jump_through(self.level_map[self.get_top_cell_y(-1)][self.get_left_cell_x()]) or \
                not self.can_jump_through(self.level_map[self.get_top_cell_y(-1)][self.get_right_cell_x()]) or \
                self.current_jump_height >= self.jump_height:
            self.jump_in_progress = False
            self.current_jump_height = 0
            return

        distance = self.vspeed / commonConsts.FPS
        if (self.current_jump_height + distance) > self.jump_height:
            distance = self.jump_height - self.current_jump_height

        full_distance = True
        blocks = 0
        offset = 0
        while offset < distance:
            offset += commonConsts.BLOCK_SIZE
            if offset > distance:
                offset = distance
            if not self.can_jump_through(self.level_map[self.get_top_cell_y(-offset)][self.get_left_cell_x()]) or \
                    not self.can_jump_through(self.level_map[self.get_top_cell_y(-offset)][self.get_right_cell_x()]):
                full_distance = False
                break
            blocks += 1
        if full_distance:
            self.rect.top -= distance
            self.current_jump_height += distance
            if self.current_jump_height >= self.jump_height:
                self.jump_in_progress = False
                self.current_jump_height = 0
        else:
            self.set_top_cell_y(self.get_top_cell_y() - blocks)
            self.jump_in_progress = False
            self.current_jump_height = 0

    def do_update(self, *args):
        pass

    def jump(self):
        if self.jump_in_progress:
            return

        if not self.can_stay(self.level_map[self.get_bottom_cell_y(1)][self.get_left_cell_x()]) and \
           not self.can_stay(self.level_map[self.get_bottom_cell_y(1)][self.get_right_cell_x()]) and \
           not self.box_service.stay_on_box(self) :
            return

        self.jump_in_progress = True
        self._process_jump()

    def move(self, can_fall = True, flip_on_stop = False, distance = 0):
        if distance == 0:
            distance = self.hspeed // commonConsts.FPS  # При таком подходе скорость спрайта должна быть кратна fps, иначе она будет урезаться
        if distance == 0:
            return
        
        self.play_animation(self.get_move_animation())
        self.was_stay = False

        #Пока предполагаем, что максимальная высота спрайта два блока
        full_distance = True
        offset=0
        last_success_right = self.get_right_cell_x()
        last_success_left = self.get_left_cell_x()
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
            #if right == self.get_right_cell_x() and left == self.get_left_cell_x():
            #    continue

            if self.right_direction:
                block_front = right
                block_back = left
            else:
                block_back = right
                block_front = left

            if not self.can_move(self.level_map[self.get_bottom_cell_y()][block_front]) or not self.can_move(self.level_map[self.get_top_cell_y()][block_front]):
                if self.right_direction:
                    distance = (last_success_right + 1) * commonConsts.BLOCK_SIZE - self.rect.width - self.rect.left
                    #self.set_right_cell_x(last_success_right)
                else:
                    distance = last_success_left * commonConsts.BLOCK_SIZE - self.rect.left
                    #self.set_left_cell_x(last_success_left)
                if flip_on_stop:
                    self.change_direction()
                break
            if not self.can_stay(self.level_map[self.get_bottom_cell_y()+1][block_front]):
                if not can_fall:
                    full_distance = False
                    if self.right_direction:
                        distance = (last_success_right + 1) * commonConsts.BLOCK_SIZE - self.rect.width - self.rect.left
                        #self.set_right_cell_x(last_success_right)
                    else:
                        distance = last_success_left * commonConsts.BLOCK_SIZE - self.rect.left
                        #self.set_left_cell_x(last_success_left)
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

        distance = self.box_service.moveBoxes(self, distance=distance, right_direction=self.right_direction)
        if distance <= 0:
            if flip_on_stop:
                self.change_direction()

        if self.right_direction:
            self.rect.left = self.rect.left + distance
        else:
            self.rect.left = self.rect.left - distance

    
    def update(self, *args):
        super().update(*args)
        self.was_stay = True
        self.fall()
        self._process_jump()
        self.do_update(*args)
        if self.was_stay:
            self.play_animation(self.get_stay_animation())

    # def is_majority_inside(self, door):
    #     """
    #     Проверяет, находится ли большая часть спрайта внутри двери.
    #
    #     :param door: Спрайт двери.
    #     :return: True, если большая часть спрайта внутри двери, иначе False.
    #     """
    #     intersection = self.rect.clip(door.rect)
    #
    #     sprite_area = self.rect.width * self.rect.height
    #     intersection_area = intersection.width * intersection.height
    #
    #     return intersection_area > 0.5 * sprite_area