import pygame
import constantes as c
import sprites as s
import math

class Bee:
    def __init__(self, screen, x_coord, y_coord, target, speed, dirc, box, Id):
        """
        Função que inicializa as abelhas

        Parameters
        ----------
        screen : pygame.Surface
            Plota as abelhas na tela.
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
        self.target = target
        self.screen = screen
        self.speed = speed
        self.direction = dirc
        self.in_box = box
        self.Id = Id
        # self.turns, self.inbox = self.check_collisions()
        self.rect = self.get_rect()
        
    def draw_bee(self, powerup, counter, eaten, dead):
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
        if (not powerup and not dead) or (eaten[self.Id] and powerup and not dead):
            self.screen.blit(s.ABLINHA[counter//10], (self.x_pos, self.y_pos))

        elif powerup and not dead and not eaten[self.Id]:
            self.screen.blit(s.ABLINHA_POWERUP[counter//10], (self.x_pos, self.y_pos))

        else:
            self.screen.blit(s.ABLINHA_MORTO, (self.x_pos, self.y_pos))
        
    
    def get_rect(self):
        """
        Atualizador de local de colisão com a abelha.

        Returns
        -------
        bee_rect : pygame.Rect
            Retângulo de colisão da abelha.

        """
        
        bee_rect = pygame.rect.Rect((self.center_x - 12, self.center_y - 12), (24, 24))

        return bee_rect

    def check_collisions(self, level):
        """
        Checa por onde a abelha pode andar.

        Parameters
        ----------
        level : list
            Matriz que representa o nível a ser jogado.

        Returns
        -------
        None.

        """
        #Tiles pré-setados
        num1 = c.ALTURA_1
        num2 = c.LARGURA_1
        num3 = c.NORMALIZACAO

        self.turns = [False, False, False, False]
        
        y_1 = math.floor(self.center_y / num1)
        y_1_plus = math.floor((self.center_y + num1) / num1)
        y_1_minus = math.floor((self.center_y - num1) / num1)
        y_3_plus = math.floor((self.center_y + num3) / num1)
        y_3_minus = math.floor((self.center_y - num3) / num1)
        
        x_1 = math.floor(self.center_x / num2)
        x_2_plus = math.floor((self.center_x + num2) / num2)
        x_2_minus = math.floor((self.center_x - num2) / num2)
        x_3_plus = math.floor((self.center_x + num3) / num2)
        x_3_minus = math.floor((self.center_x - num3) / num2)

        if self.center_x // 30 < 15:
            if level[y_1][x_3_minus] < 3 \
                or level[y_1][x_3_minus] == 9 and (
                self.in_box or self.dead):

                self.turns[1] = True

            if level[y_1][x_3_plus] < 3 \
                or level[y_1][x_3_plus] == 9 and (
                self.in_box or self.dead):

                self.turns[0] = True

            if level[y_3_plus][x_1] < 3 \
                or level[y_3_plus][x_1] == 9 and (
                self.in_box or self.dead):

                self.turns[3] = True

            if level[y_3_minus][x_1] < 3 \
                or level[y_3_minus][x_1] == 9 and (
                self.in_box or self.dead):

                self.turns[2] = True
            
            if self.direction == 2 or self.direction == 3:
                if 7 <= self.center_x % num2 <= 10:
                    if level[y_3_plus][x_1] < 3 \
                        or level[y_3_plus][x_1] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[3] = True

                    if level[y_3_minus][x_1] < 3 \
                        or level[y_3_minus][x_1] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[2] = True
                
                if 7 <= self.center_y % num1 <= 10:
                    if level[y_1][x_2_minus] < 3 \
                        or level[y_1][x_2_minus] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[1] = True

                    if level[y_1][x_2_plus] < 3 \
                        or level[y_1][x_2_plus] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[0] = True
                
            if self.direction == 1 or self.direction == 0:
                if 7 <= self.center_x % num2 <= 10:
                    if level[y_1_plus][x_1] < 3 \
                        or level[y_1_plus][x_1] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[3] = True

                    if level[y_1_minus][x_1] < 3 \
                        or level[y_1_minus][x_1] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[2] = True
                
                if 7 <= self.center_y % num1 <= 10:
                    if level[y_1][x_3_minus] < 3 \
                        or level[y_1][x_3_minus] == 9 and (
                            self.in_box or self.dead):
                    
                        self.turns[1] = True

                    if level[y_1][x_3_plus] < 3 \
                        or level[y_1][x_3_plus] == 9 and (
                            self.in_box or self.dead):
                        
                        self.turns[0] = True
                    
