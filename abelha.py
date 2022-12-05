import pygame
import constantes as c
import sprites as s
import math

class Bee:
    def __init__(self, screen, level, x_coord, y_coord, target, speed, dirc, box, Id):
        """
        Função que inicializa as abelhas

        Parameters
        ----------
        screen : pygame.Surface
            Plota as abelhas na tela.
        level : list
            Matriz que representa o nível a ser jogado.
        x_coord : int
            Coordenada x inicial das abelhas.
        y_coord : int
            Coordenada y inicial das abelhas.
        target : TYPE
            DESCRIPTION.
        speed : int
            Velocidade das abelhas.
        dirc : int
            Indica em qual direção o fantasma está percorrendo.
        box : bool
            Identfica se um fantasma está na caixa ou não.
        Id : int
            Identificador de uma abelha.

        Returns
        -------
        None.

        """
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 15
        self.center_y = self.y_pos + 15
        self.level = level
        self.target = target
        self.dead =  False
        self.screen = screen
        self.speed = speed
        self.direction = dirc
        self.in_box = box
        self.Id = Id
        self.turns = [False, False, False, False]
        self.inbox = False
        self.rect = self.get_rect(self.x_pos, self.y_pos)
        
    def draw_bee(self, x_pos, y_pos, powerup, counter, eaten, dead, direct):
        """
        Desenha a abelha conforme a situação atual do jogo.

        Parameters
        ----------
        powerup : bool
            Indica se o powerup está ativado ou não.
        counter : int
            Inteiro para auxiliar na decisão da imagem escolhida.
        eaten : bool
            Indica se o fantasma pode ser devorado ou não.
        dead : bool
            Indica se o fantasma foi devorado ou não.

        Returns
        -------
        None.

        """

        self.direction = direct
        self.rect = self.get_rect(self.x_pos, self.y_pos)
        self.dead = dead
        self.x_pos = x_pos
        self.y_pos = y_pos

        if (not powerup and not self.dead) or (eaten[self.Id] and powerup and not self.dead):
            if self.direction == 0:
                self.screen.blit(pygame.transform.flip(s.ABLINHA[counter//10],True, False), (self.x_pos, self.y_pos))
            elif self.direction == 1:
                self.screen.blit(s.ABLINHA[counter // 10], (self.x_pos, self.y_pos))
            elif self.direction == 2:
                self.screen.blit(pygame.transform.rotate(s.ABLINHA[counter // 10], 270), (self.x_pos, self.y_pos))
            elif self.direction == 3:
                self.screen.blit(pygame.transform.rotate(s.ABLINHA[counter // 10], 90), (self.x_pos, self.y_pos))

        elif powerup and not self.dead and not eaten[self.Id]:
            if self.direction == 0:
                self.screen.blit(pygame.transform.flip(s.ABLINHA_POWERUP[counter//10],True, False), (self.x_pos, self.y_pos))
            elif self.direction == 1:
                self.screen.blit(s.ABLINHA_POWERUP[counter // 10], (self.x_pos, self.y_pos))
            elif self.direction == 2:
                self.screen.blit(pygame.transform.rotate(s.ABLINHA_POWERUP[counter // 10], 270), (self.x_pos, self.y_pos))
            elif self.direction == 3:
                self.screen.blit(pygame.transform.rotate(s.ABLINHA_POWERUP[counter // 10], 90), (self.x_pos, self.y_pos))

        else:
            if self.direction == 0:
                self.screen.blit(pygame.transform.flip(s.ABLINHA_MORTO ,True, False), (self.x_pos, self.y_pos))
            elif self.direction == 1:
                self.screen.blit(s.ABLINHA_MORTO, (self.x_pos, self.y_pos))
            elif self.direction == 2:
                self.screen.blit(pygame.transform.rotate(s.ABLINHA_MORTO, 270), (self.x_pos, self.y_pos))
            elif self.direction == 3:
                self.screen.blit(pygame.transform.rotate(s.ABLINHA_MORTO, 90), (self.x_pos, self.y_pos))    
    
    def get_rect(self, x_pos, y_pos):
        """
        Atualizador de local de colisão com a abelha.

        Returns
        -------
        bee_rect : pygame.Rect
            Retângulo de colisão da abelha.

        """
        
        bee_rect = pygame.rect.Rect(((x_pos + 15) - 12, (y_pos + 15) - 12), (24, 24))

        return bee_rect

    def check_collisions(self, level, bee_x, bee_y, speed):
        """
        Checa por onde a abelha pode andar.

        Returns
        -------
        None.

        """
        #Tiles pré-setados
        num1 = c.ALTURA_1
        num2 = c.LARGURA_1
        num3 = c.NORMALIZACAO

        self.speed = speed
        self.x_pos = bee_x
        self.y_pos = bee_y

        center_x = self.x_pos + 15
        center_y = self.y_pos + 15

        self.turns = [False, False, False, False]
        if 0 < center_x // 30 < 15:
            if level[(center_y - num3) // num1][center_x // num2] == 9:
                self.turns[2] = True
            if level[center_y // num1][(center_x - num3) // num2] < 3 \
                    or (level[center_y // num1][(center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[center_y // num1][(center_x + num3) // num2] < 3 \
                    or (level[center_y // num1][(center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(center_y + num3) // num1][center_x // num2] < 3 \
                    or (level[(center_y + num3) // num1][center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(center_y - num3) // num1][center_x // num2] < 3 \
                    or (level[(center_y - num3) // num1][center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 8 <= center_x % num2 <= 9:
                    if level[(center_y + num3) // num1][center_x // num2] < 3 \
                            or (level[(center_y + num3) // num1][center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(center_y - num3) // num1][center_x // num2] < 3 \
                            or (level[(center_y - num3) // num1][center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 8 <= center_y % num1 <= 9:
                    if level[center_y // num1][(center_x - num2) // num2] < 3 \
                            or (level[center_y // num1][(center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[center_y // num1][(center_x + num2) // num2] < 3 \
                            or (level[center_y // num1][(center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 8 <= center_x % num2 <= 9:
                    if level[(center_y + num3) // num1][center_x // num2] < 3 \
                            or (level[(center_y + num3) // num1][center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(center_y - num3) // num1][center_x // num2] < 3 \
                            or (level[(center_y - num3) // num1][center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 8 <= center_y % num1 <= 9:
                    if level[center_y // num1][(center_x - num3) // num2] < 3 \
                            or (level[center_y // num1][(center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[center_y // num1][(center_x + num3) // num2] < 3 \
                            or (level[center_y // num1][(center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 176 < self.x_pos < 280 and 208 < self.y_pos < 264:
            self.in_box = True
        else:
            self.in_box = False

        return self.turns, self.in_box

    def move_1(self, target, turns):
        # r, l, u, d
        if self.direction == 0:
            if target[0] > self.x_pos and turns[0]:
                self.x_pos += self.speed
            elif not turns[0]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif turns[0]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if target[1] > self.y_pos and turns[3]:
                self.direction = 3
            elif target[0] < self.x_pos and turns[1]:
                self.x_pos -= self.speed
            elif not turns[1]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif turns[1]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if target[0] < self.x_pos and turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif target[1] < self.y_pos and turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not turns[2]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif turns[2]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if target[1] > self.y_pos and turns[3]:
                self.y_pos += self.speed
            elif not turns[3]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif turns[3]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = c.LARGURA
        elif self.x_pos > c.LARGURA: 
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_2(self, target, turns):
        # r, l, u, d
        if self.direction == 0:
            if target[0] > self.x_pos and turns[0]:
                self.x_pos += self.speed
            elif not turns[0]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if target[0] < self.x_pos and turns[1]:
                self.x_pos -= self.speed
            elif not turns[1]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if target[1] < self.y_pos and turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not turns[2]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if target[1] > self.y_pos and turns[3]:
                self.y_pos += self.speed
            elif not turns[3]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = c.LARGURA
        elif self.x_pos > c.LARGURA:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_3(self, target, turns):
        # r, l, u, d
        if self.direction == 0:
            if target[0] > self.x_pos and turns[0]:
                self.x_pos += self.speed
            elif not turns[0]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif turns[0]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if target[1] > self.y_pos and turns[3]:
                self.direction = 3
            elif target[0] < self.x_pos and turns[1]:
                self.x_pos -= self.speed
            elif not turns[1]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif turns[1]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if target[1] < self.y_pos and turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not turns[2]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if target[1] > self.y_pos and turns[3]:
                self.y_pos += self.speed
            elif not turns[3]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = c.LARGURA
        elif self.x_pos > c.LARGURA:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_4(self, target, turns):
        # r, l, u, d
        if self.direction == 0:
            if target[0] > self.x_pos and turns[0]:
                self.x_pos += self.speed
            elif not turns[0]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if target[1] > self.y_pos and turns[3]:
                self.direction = 3
            elif target[0] < self.x_pos and turns[1]:
                self.x_pos -= self.speed
            elif not turns[1]:
                if target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if target[0] < self.x_pos and turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif target[1] < self.y_pos and turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not turns[2]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif target[1] > self.y_pos and turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif turns[2]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if target[1] > self.y_pos and turns[3]:
                self.y_pos += self.speed
            elif not turns[3]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif target[1] < self.y_pos and turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif turns[3]:
                if target[0] > self.x_pos and turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif target[0] < self.x_pos and turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = c.LARGURA
        elif self.x_pos > c.LARGURA:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction
