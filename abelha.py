import pygame
import constantes as c
import sprites as s
import math

class Bee:
    def __init__(self, screen, x_coord, y_coord, target, speed, dirc, box, Id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 15
        self.center_y = self.y_pos + 15
        self.target = target
        self.screen = screen
        self.speed = speed
        self.direction = dirc
        self.in_box = box
        self.Id = Id
        # self.turns, self.inbox = self.check_collisions()
        self.rect = self.get_rect()
        
    def draw_bee(self, powerup, counter, eaten, dead):

        if (not powerup and not dead) or (eaten[self.Id] and powerup and not dead):
            self.screen.blit(s.ABLINHA[counter//10], (self.x_pos, self.y_pos))

        elif powerup and not dead and not eaten[self.Id]:
            self.screen.blit(s.ABLINHA_POWERUP[counter//10], (self.x_pos, self.y_pos))

        else:
            self.screen.blit(s.ABLINHA_MORTO, (self.x_pos, self.y_pos))
        
    
    def get_rect(self):
        
        bee_rect = pygame.rect.Rect((self.center_x - 12, self.center_y - 12), (24, 24))

        return bee_rect

    def check_collisions(self, level):

        num1 = 16
        num2 = 16
        num3 = 9

        self.turns = [False, False, False, False]

        if self.center_x // 30 < 15:
            if level[math.floor(self.center_y / num1)][math.floor((self.center_x - num3) / num2)] < 3 \
                or level[math.floor(self.center_y / num1)][math.floor((self.center_x - num3) / num2)] == 9 and (
                self.in_box or self.dead):

                self.turns[1] = True

            if level[math.floor(self.center_y / num1)][math.floor((self.center_x + num3) / num2)] < 3 \
                or level[math.floor(self.center_y / num1)][math.floor((self.center_x + num3) / num2)] == 9 and (
                self.in_box or self.dead):

                self.turns[0] = True

            if level[math.floor((self.center_y + num3) / num1)][math.floor(self.center_x / num2)] < 3 \
                or level[math.floor((self.center_y + num3) / num1)][math.floor(self.center_x / num2)] == 9 and (
                self.in_box or self.dead):

                self.turns[3] = True

            if level[math.floor((self.center_y - num3) / num1)][math.floor(self.center_x / num2)] < 3 \
                or level[math.floor((self.center_y - num3) / num1)][math.floor(self.center_x / num2)] == 9 and (
                self.in_box or self.dead):

                self.turns[2] = True
            
            if self.direction == 2 or self.direction == 3:
                if 7 <= self.center_x % num2 <= 10:
                    if level[math.floor((self.center_y + num3) / num1)][math.floor(self.center_x / num2)] < 3 \
                        or level[math.floor((self.center_y + num3) / num1)][math.floor(self.center_x / num2)] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[3] = True

                    if level[math.floor((self.center_y - num3) / num1)][math.floor(self.center_x / num2)] < 3 \
                        or level[math.floor((self.center_y - num3) / num1)][math.floor(self.center_x / num2)] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[2] = True
                
                if 7 <= self.center_y % num1 <= 10:
                    if level[math.floor(self.center_y / num1)][math.floor((self.center_x - num2) / num2)] < 3 \
                        or level[math.floor(self.center_y / num1)][math.floor((self.center_x - num2) / num2)] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[1] = True

                    if level[math.floor(self.center_y / num1)][math.floor((self.center_x + num2) / num2)] < 3 \
                        or level[math.floor(self.center_y / num1)][math.floor((self.center_x + num2) / num2)] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[0] = True
                
            if self.direction == 1 or self.direction == 0:
                if 7 <= self.center_x % num2 <= 10:
                    if level[math.floor((self.center_y + num1) / num1)][math.floor(self.center_x / num2)] < 3 \
                        or level[math.floor((self.center_y + num1) / num1)][math.floor(self.center_x / num2)] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[3] = True

                    if level[math.floor((self.center_y - num1) / num1)][math.floor(self.center_x / num2)] < 3 \
                        or level[math.floor((self.center_y - num1) / num1)][math.floor(self.center_x / num2)] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[2] = True
                
                if 7 <= self.center_y % num1 <= 10:
                    if level[math.floor(self.center_y / num1)][math.floor((self.center_x - num3) / num2)] < 3 \
                        or level[math.floor(self.center_y / num1)][math.floor((self.center_x - num3) / num2)] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[1] = True

                    if level[math.floor(self.center_y / num1)][math.floor((self.center_x + num3) / num2)] < 3 \
                        or level[math.floor(self.center_y / num1)][math.floor((self.center_x + num3) / num2)] == 9 and (
                            self.in_box or self.dead):
                        
                        self.turns[0] = True
                    
