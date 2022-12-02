import pygame
import os

imagesdir = os.path.join(os.getcwd(), "imagens")

#Euler's Fante
PLAYER_IMAGES = []

for i in range(1, 5):
    PLAYER_IMAGES.append(pygame.transform.scale(pygame.image.load(os.path.join(imagesdir, f"Euler'sFant_{i}.png")), (30, 30)))


ABLINHA = []

for i in range(1, 3):
    ABLINHA.append(pygame.transform.scale(pygame.image.load(os.path.join(imagesdir, f"AB'_{i}.png")), (30, 30)))


ABLINHA_POWERUP = []

for i in range(1, 3):
    ABLINHA_POWERUP.append(pygame.transform.scale(pygame.image.load(os.path.join(imagesdir, f"AB'Powerup_{i}.png")), (30, 30)))


ABLINHA_MORTO = pygame.transform.scale(pygame.image.load(os.path.join(imagesdir, "Dead.png")), (30, 30))