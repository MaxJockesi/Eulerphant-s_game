import pygame
import constantes as c
import sprites as s
import os, sys, math

class Bee:
    def __init__(self, screen, x_coord, y_coord, powerup, target, speed, counter, dirc, dead, box, Id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 15
        self.center_y = self.y_pos + 15
        self.target = target
        self.screen = screen
        self.speed = speed
        self.dead = dead
        self.direction = dirc
        self.counter = counter
        self.in_box = box
        self.powerup = powerup
        self.id = Id
        # self.turns, self.inbox = self.check_collisions()
        self.rect = self.get_rect()
        
    def draw_bee(self):

        if (not self.powerup and not self.dead) or (self.eaten[self.Id] and self.powerup and not self.dead):
            self.screen.blit(s.ABLINHA[self.counter//10], (self.x_pos, self.y_pos))

        elif self.powerup and not self.dead and not self.eaten[self.Id]:
            self.screen.blit(s.ABLINHA_POWERUP[self.counter//10], (self.x_pos, self.y_pos))

        else:
            self.screen.blit(s.ABLINHA_MORTO, (self.x_pos, self.y_pos))
        
    
    def get_rect(self):
        
        bee_rect = pygame.rect.Rect((self.center_x - 12, self.center_y - 12), (24, 24))

        return bee_rect

    def check_collisions(self):

    #    if 0 < self.player_x < 464:

    #        if self.level[math.floor(centery/c.ALTURA_1)][math.floor(centerx/c.LARGURA_1)] == 1:
    #            self.level[math.floor(centery/c.ALTURA_1)][math.floor(centerx/c.LARGURA_1)] = 0
    #            score += 10

    #        if self.level[math.floor(centery/c.ALTURA_1)][math.floor(centerx/c.LARGURA_1)] == 2:
    #            self.level[math.floor(centery/c.ALTURA_1)][math.floor(centerx/c.LARGURA_1)] = 0
    #            score += 50
    #            self.powerup = True
    #            self.power_count = 0
    #            self.eaten_bees = [False, False, False, False]
        pass
