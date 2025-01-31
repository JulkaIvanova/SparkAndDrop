from typing import List
from pygame import Rect

from commonConsts import BLOCK_SIZE


class BoxService:
    def __init__(self, level_map):
        self.level_map = level_map
        self.boxes = []

    def addBox(self, box):
        self.boxes.append(box)
    
    def moveBoxes(self, currentSprite, distance: int, right_direction = True, can_fall = True) -> int:
        offset = 0
        box_on_distance = None
        while offset<distance:
            offset+=BLOCK_SIZE
            if offset>distance:
                offset = distance

            dir_offset = offset
            if not right_direction:
                dir_offset = -offset
            # TODO: Доработать, так как при таком подходе может получиться что если два ящика стоят друг на друге толкать мы будем первый попавшийся, а сквозь другой пройдем
            for b in self.boxes:
                if currentSprite == b:
                    continue
                if currentSprite.rect.move(dir_offset, 0).colliderect(b.rect):
                    box_on_distance = b
                    break
            if not box_on_distance is None:
                break

        if box_on_distance is None:
            return distance
        
        if right_direction:
            sprite_box_distance = box_on_distance.rect.left - currentSprite.rect.left - currentSprite.rect.width
        else:
            sprite_box_distance = currentSprite.rect.left - box_on_distance.rect.left - box_on_distance.rect.width
        
        box_on_distance.set_direction(right_direction)
        box_on_distance.move(can_fall=can_fall, distance=distance-sprite_box_distance)

        if right_direction:
            return box_on_distance.rect.left - currentSprite.rect.left - currentSprite.rect.width
        else:
            return currentSprite.rect.left - box_on_distance.rect.left - box_on_distance.rect.width
        
    def stay_on_box(self, currentSprite, offset: int=1) -> bool:
        for b in self.boxes:
            if currentSprite == b:
                continue
            if currentSprite.rect.move(0, offset).colliderect(b.rect):
                return True

        return False
        
    def fallThroughBoxes(self, currentSprite, distance: int) -> int:
        offset = 0
        box_on_distance = None
        while offset<distance:
            offset+=BLOCK_SIZE
            if offset>distance:
                offset = distance

            for b in self.boxes:
                if currentSprite == b:
                    continue
                if currentSprite.rect.move(0, offset).colliderect(b.rect):
                    box_on_distance = b
                    break
            if not box_on_distance is None:
                break

        if box_on_distance is None:
            return distance

        return box_on_distance.rect.top - currentSprite.rect.top - currentSprite.rect.height