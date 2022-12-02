import pygame
import os

#Euler's Fante
PLAYER_IMAGES = []

imagesdir = os.path.join(os.getcwd(), "imagens")

for i in range(1, 5):
    PLAYER_IMAGES.append(pygame.transform.scale(pygame.image.load(os.path.join(imagesdir, f"Euler'sFant_{i}.png")), (30, 30)))
