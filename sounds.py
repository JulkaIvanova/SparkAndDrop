import pygame

pygame.init()

win_sound = pygame.mixer.Sound('data\\win_sound.wav')
win_sound.set_volume(1.5)
loose_sound = pygame.mixer.Sound('data\\loose_sound.wav')
loose_sound.set_volume(1.5)
book_sound = pygame.mixer.Sound('data\\book_sound.wav')
book_sound.set_volume(1.5)
jump_sound = pygame.mixer.Sound('data\\jump_sound.wav')
jump_sound.set_volume(1.5)
choose_sound = pygame.mixer.Sound('data\\choose_soud.wav')
choose_sound.set_volume(1.5)
coin_sound = pygame.mixer.Sound('data\\coin_sound.wav')
coin_sound.set_volume(1.5)
fight_sound = pygame.mixer.Sound('data\\fight_sound.wav')
fight_sound.set_volume(1.5)
