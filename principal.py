import pygame
from abelha import Bee 
import constantes as c
import sprites as s
import os, sys, math, copy

class Game:
    def __init__(self):
        """
        Função que inicia e declara as constantes do jogo, criando a tela e
        dispondo os personagens e parâmetros.

        Returns
        -------
        None.

        """
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((c.LARGURA, c.ALTURA))
        pygame.display.set_caption(c.TITULO_JOGO)
        
        self.clock = pygame.time.Clock()
        self.is_running = True
        
        self.font = pygame.font.match_font(c.FONTE)
        self.upload_files()
        self.level = copy.deepcopy(c.BOARDS)
        
        self.player_x = c.PLAYER_X
        self.player_y = c.PLAYER_Y
        
        self.direction = 0
        self.counter = 0
        self.powerup = False
        self.power_count = 0
        
        self.eaten_bees = []
        self.targets = []
        self.turns_allowed = []
        self.bee_speeds = []
        
        self.moving = False
        self.lives = 3
        self.startup_counter = 0
        self.score = 0
        self.direction_command = 0
        self.game_over = False
        self.game_won = False
        
        for i in range(1,5):
            self.targets.append((self.player_x, self.player_y))
            self.eaten_bees.append(False)
            self.turns_allowed.append(False) 
            self.bee_speeds.append(c.BEE_SPEED)
            exec(f'self.bee{i}_direct = c.BEE{i}_DIRECTION')
            exec(f'self.bee{i}_x = c.BEE{i}_X')
            exec(f'self.bee{i}_y = c.BEE{i}_Y') 
            exec(f'self.bee{i}_turns = [False, False, False, False]')
            exec(f'self.bee{i}_dead = c.BEE{i}_DEAD')
            exec(f'self.bee{i}_box = False')
            exec(f'self.bee{i} = Bee(self.screen, self.level, c.BEE{i}_X, c.BEE{i}_Y, self.targets[{i} - 1],  \
                 self.bee_speeds[{i - 1}], self.bee{i}_direct, self.bee{i}_box, {i} - 1)')
        
    def new_game(self):
        """
        Função que instancia as sprites do jogo.

        Returns
        -------
        None.

        """

        self.run()
    
    def run(self):
        """
        Função que determina a dinâmica temporal do jogo.

        Returns
        -------
        None.

        """
        self.playing = True
        self.flicker = False
        while self.playing:
            self.clock.tick(c.FPS)

            if self.counter < 19:
                self.counter += 1
                if self.counter > 3:
                    self.flicker = False
            else:
                self.counter = 0
                self.flicker = True

            if self.powerup and self.power_count < 300:
                self.power_count += 1
            elif self.powerup and self.power_count >= 300:

                pygame.mixer.music.stop()
                self.power_count = 0
                self.powerup = False
                self.eaten_bees = [False, False, False, False]
            
            if self.startup_counter < 90 and not self.game_over and not self.game_won:
                self.moving = False
                self.startup_counter += 1
            else:
                self.moving = True
            
            if self.powerup:
                self.bee_speeds = [1, 1, 1, 1]
            else:
                self.bee_speeds = [2, 2, 2, 2]

            if self.bee1.dead:
                self.bee_speeds[0] = 4
            if self.bee2.dead:
                self.bee_speeds[1] = 4
            if self.bee3.dead:
                self.bee_speeds[2] = 4
            if self.bee4.dead:
                self.bee_speeds[3] = 4

            self.game_won = True
            for i in range(len(self.level)):
                if 1 in self.level[i] or 2 in self.level[i]:
                    self.game_won = False

            self.turns_allowed = self.check_position(self.player_x, self.player_y)

            self.bee1_turns, self.bee1_box = self.bee1.check_collisions(self.level, self.bee1_x, self.bee1_y, self.bee_speeds[0])
            self.bee2_turns, self.bee2_box = self.bee2.check_collisions(self.level, self.bee2_x, self.bee2_y, self.bee_speeds[1])
            self.bee3_turns, self.bee3_box = self.bee3.check_collisions(self.level, self.bee3_x, self.bee3_y, self.bee_speeds[2])
            self.bee4_turns, self.bee4_box = self.bee4.check_collisions(self.level, self.bee4_x, self.bee4_y, self.bee_speeds[3])

            self.bee1_rect = self.bee1.get_rect(self.bee1_x, self.bee1_y)
            self.bee2_rect = self.bee2.get_rect(self.bee2_x, self.bee2_y)
            self.bee3_rect = self.bee3.get_rect(self.bee3_x, self.bee3_y)
            self.bee4_rect = self.bee4.get_rect(self.bee4_x, self.bee4_y)

            if self.moving:
                self.player_x, self.player_y = self.move_player(self.player_x, self.player_y)
                
                if not self.bee1.dead and not self.bee1_box:
                    self.bee1_x, self.bee1_y, self.bee1_direct = self.bee1.move_1(self.targets[0], self.bee1_turns)
                elif self.bee1.dead and not self.bee1_box:
                    self.bee1_x, self.bee1_y, self.bee1_direct = self.bee1.move_1(self.targets[0], self.bee1_turns)
                elif self.bee1_box and not self.bee1.dead:
                    self.bee1_x, self.bee1_y, self.bee1_direct = self.bee1.move_1(self.targets[0], self.bee1_turns)

                if not self.bee2.dead and not self.bee2_box: 
                    self.bee2_x, self.bee2_y, self.bee2_direct = self.bee2.move_2(self.targets[1], self.bee2_turns)
                elif self.bee2.dead and not self.bee2_box:
                    self.bee2_x, self.bee2_y, self.bee2_direct = self.bee2.move_1(self.targets[1], self.bee2_turns)
                elif self.bee2_box and not self.bee2.dead:
                    self.bee2_x, self.bee2_y, self.bee2_direct = self.bee2.move_1(self.targets[1], self.bee2_turns)

                if not self.bee3.dead and not self.bee3_box:
                    self.bee3_x, self.bee3_y, self.bee3_direct = self.bee3.move_3(self.targets[2], self.bee3_turns)
                elif self.bee3.dead and not self.bee3_box:
                    self.bee3_x, self.bee3_y, self.bee3_direct = self.bee3.move_1(self.targets[2], self.bee3_turns)
                elif self.bee3_box and not self.bee3.dead:
                    self.bee3_x, self.bee3_y, self.bee3_direct = self.bee3.move_1(self.targets[2], self.bee3_turns)

                if not self.bee4.dead and not self.bee4_box:
                    self.bee4_x, self.bee4_y, self.bee4_direct = self.bee4.move_4(self.targets[3], self.bee4_turns)
                elif self.bee4.dead and not self.bee4_box:
                    self.bee4_x, self.bee4_y, self.bee4_direct = self.bee4.move_1(self.targets[3], self.bee4_turns)
                elif self.bee4_box and not self.bee4.dead:
                    self.bee4_x, self.bee4_y, self.bee4_direct = self.bee4.move_1(self.targets[3], self.bee4_turns)

            self.score = self.check_collisions(self.score)
            self.targets = self.get_target()
            self.plot_sprites()

            if not self.powerup:
                if (self.player_hitbox.colliderect(self.bee1_rect) and not self.bee1.dead) or \
                    (self.player_hitbox.colliderect(self.bee2_rect) and not self.bee2.dead) or \
                    (self.player_hitbox.colliderect(self.bee3_rect) and not self.bee3.dead) or \
                    (self.player_hitbox.colliderect(self.bee4_rect) and not self.bee4.dead):

                    if self.lives > 0:
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound(os.path.join(self.audiodir, c.MUSIC_LOSE_LIFE)).play()
                        self.lives -= 1
                        self.startup_counter = 0

                        self.player_x = c.PLAYER_X
                        self.player_y = c.PLAYER_Y
                        self.direction = 0
                        self.direction_command = 0
                        self.powerup = False
                        self.power_count = 0

                        self.eaten_bees = [False, False, False, False]

                        for i in range(1,5):
                            exec(f'self.bee{i}_x = c.BEE{i}_X')
                            exec(f'self.bee{i}_y = c.BEE{i}_Y')
                            exec(f'self.bee{i}_direct = c.BEE{i}_DIRECTION')
                            exec(f'self.bee{i}_dead = c.BEE{i}_DEAD')

                    else:
                        self.moving = False
                        self.game_over = True
                        self.startup_counter = 0

            if self.powerup and self.player_hitbox.colliderect(self.bee1_rect) and self.eaten_bees[0] and not self.bee1.dead:
                if self.lives > 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound(os.path.join(self.audiodir, c.MUSIC_LOSE_LIFE)).play()
                    self.lives -= 1
                    self.startup_counter = 0

                    self.player_x = c.PLAYER_X
                    self.player_y = c.PLAYER_Y
                    self.direction = 0
                    self.direction_command = 0
                    self.powerup = False
                    self.power_count = 0

                    self.eaten_bees = [False, False, False, False]

                    for i in range(1,5):
                        exec(f'self.bee{i}_x = c.BEE{i}_X')
                        exec(f'self.bee{i}_y = c.BEE{i}_Y')
                        exec(f'self.bee{i}_direct = c.BEE{i}_DIRECTION')
                        exec(f'self.bee{i}_dead = c.BEE{i}_DEAD')
                
                else:
                        self.moving = False
                        self.game_over = True
                        self.startup_counter = 0
        
            if self.powerup and self.player_hitbox.colliderect(self.bee2_rect) and self.eaten_bees[1] and not self.bee2.dead:
                if self.lives > 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound(os.path.join(self.audiodir, c.MUSIC_LOSE_LIFE)).play()
                    self.lives -= 1
                    self.startup_counter = 0

                    self.player_x = c.PLAYER_X
                    self.player_y = c.PLAYER_Y
                    self.direction = 0
                    self.direction_command = 0
                    self.powerup = False
                    self.power_count = 0

                    self.eaten_bees = [False, False, False, False]

                    for i in range(1,5):
                        exec(f'self.bee{i}_x = c.BEE{i}_X')
                        exec(f'self.bee{i}_y = c.BEE{i}_Y')
                        exec(f'self.bee{i}_direct = c.BEE{i}_DIRECTION')
                        exec(f'self.bee{i}_dead = c.BEE{i}_DEAD')
                
                else:
                        self.moving = False
                        self.game_over = True
                        self.startup_counter = 0
        
            if self.powerup and self.player_hitbox.colliderect(self.bee3_rect) and self.eaten_bees[2] and not self.bee3.dead:
                if self.lives > 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound(os.path.join(self.audiodir, c.MUSIC_LOSE_LIFE)).play()
                    self.lives -= 1
                    self.startup_counter = 0

                    self.player_x = c.PLAYER_X
                    self.player_y = c.PLAYER_Y
                    self.direction = 0
                    self.direction_command = 0
                    self.powerup = False
                    self.power_count = 0

                    self.eaten_bees = [False, False, False, False]

                    for i in range(1,5):
                        exec(f'self.bee{i}_x = c.BEE{i}_X')
                        exec(f'self.bee{i}_y = c.BEE{i}_Y')
                        exec(f'self.bee{i}_direct = c.BEE{i}_DIRECTION')
                        exec(f'self.bee{i}_dead = c.BEE{i}_DEAD')
                
                else:
                        self.moving = False
                        self.game_over = True
                        self.startup_counter = 0
        
            if self.powerup and self.player_hitbox.colliderect(self.bee4_rect) and self.eaten_bees[3] and not self.bee4.dead:
                if self.lives > 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound(os.path.join(self.audiodir, c.MUSIC_LOSE_LIFE)).play()
                    self.lives -= 1
                    self.startup_counter = 0

                    self.player_x = c.PLAYER_X
                    self.player_y = c.PLAYER_Y
                    self.direction = 0
                    self.direction_command = 0
                    self.powerup = False
                    self.power_count = 0

                    self.eaten_bees = [False, False, False, False]

                    for i in range(1,5):
                        exec(f'self.bee{i}_x = c.BEE{i}_X')
                        exec(f'self.bee{i}_y = c.BEE{i}_Y')
                        exec(f'self.bee{i}_direct = c.BEE{i}_DIRECTION')
                        exec(f'self.bee{i}_dead = c.BEE{i}_DEAD')
                
                else:
                        self.moving = False
                        self.game_over = True
                        self.startup_counter = 0
             
            if self.powerup and self.player_hitbox.colliderect(self.bee1_rect) and not self.bee1.dead and not self.eaten_bees[0]:
                self.bee1_dead = True
                self.eaten_bees[0] = True
                self.score += (2 ** self.eaten_bees.count(True)) * 100

            if self.powerup and self.player_hitbox.colliderect(self.bee2_rect) and not self.bee2.dead and not self.eaten_bees[1]:
                self.bee2_dead = True
                self.eaten_bees[1] = True
                self.score += (2 ** self.eaten_bees.count(True)) * 100

            if self.powerup and self.player_hitbox.colliderect(self.bee3_rect) and not self.bee3.dead and not self.eaten_bees[2]:
                self.bee3_dead = True
                self.eaten_bees[2] = True
                self.score += (2 ** self.eaten_bees.count(True)) * 100
            
            if self.powerup and self.player_hitbox.colliderect(self.bee4_rect) and not self.bee4.dead and not self.eaten_bees[3]:
                self.bee4_dead = True
                self.eaten_bees[3] = True
                self.score += (2 ** self.eaten_bees.count(True)) * 100

            
            self.events()

            for i in range(4):
                if self.direction_command == i and self.turns_allowed[i]:
                    self.direction = i
        
            if self.player_x > c.LARGURA:
                self.player_x = -40
            elif self.player_x < -40:
                self.player_x = (c.LARGURA - 3)
            
    def events(self):
        """
        Função que define os eventos de movimento do jogador e quando sair do
        jogo.

        Returns
        -------
        None.

        """
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.is_running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction_command = 2
                elif event.key == pygame.K_DOWN:
                    self.direction_command = 3
                elif event.key == pygame.K_RIGHT:
                    self.direction_command = 0
                elif event.key == pygame.K_LEFT:
                    self.direction_command = 1

            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.show_pause()
                if event.key == pygame.K_UP and self.direction_command == 2:
                    self.direction_command = self.direction
                elif event.key == pygame.K_DOWN and self.direction_command == 3:
                    self.direction_command = self.direction
                elif event.key == pygame.K_RIGHT and self.direction_command == 0:
                    self.direction_command = self.direction
                elif event.key == pygame.K_LEFT and self.direction_command == 1:
                    self.direction_command = self.direction
    
    def plot_sprites(self):
        """
        Função que coloca as sprites do jogador, do nível e dos adversários
        na tela.

        Returns
        -------
        None.

        """
        self.screen.fill(c.PRETO) #limpa a tela
        self.draw_bord(self.level) #desenha o nivel
        self.player_hitbox = pygame.draw.circle(self.screen, c.PRETO, (self.player_x + 15, self.player_y + 15), 14, 1)
        self.draw_player() #desenha o player

        #Desenha as abelhas
        for i in range(1,5):
            exec(f'self.bee{i}.draw_bee(self.bee{i}_x, self.bee{i}_y, self.powerup, self.counter, self.eaten_bees, self.bee{i}_dead, self.bee{i}_direct)')

        if self.bee1.in_box and self.bee1_dead:
            self.bee1_dead = False
        if self.bee2.in_box and self.bee2_dead:
            self.bee2_dead = False
        if self.bee3.in_box and self.bee3_dead:
            self.bee3_dead = False
        if self.bee4.in_box and self.bee4_dead:
            self.bee4_dead = False

        pygame.display.flip()
    
    def upload_files(self):
        """
        Função que carrega os áudios e imagens necessários para o jogo.

        Returns
        -------
        None.

        """
        imagesdir = os.path.join(os.getcwd(), "imagens")
        self.audiodir = os.path.join(os.getcwd(), "audios")
        self.spritesheet = os.path.join(imagesdir, c.SPRITESHEET)
        self.start_logo = os.path.join(imagesdir, c.LOGO)
        self.start_logo = pygame.image.load(self.start_logo).convert()

    def show_text(self, txt, size, color, x, y):
        """
        Função que mostra um texto do jogo na tela.

        Parameters
        ----------
        txt : string
            Texto a ser exibido.
        size : int
            Tamanho do texto a ser exibido(em pixels).
        color : tuple
            Tupla de 3 inteiros que representa uma cor na combinação RGB.
        x : int
            representa em que posição na coordenada x o texto deve ser colocado.
        y : int
            representa em que posição na coordenada y o texto deve ser colocado.

        Returns
        -------
        None.

        """
        font = pygame.font.Font(self.font, size)
        text = font.render(txt, False, color)
        text_rect = text.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text, text_rect)
    
    def show_logo(self, x, y):
        """
        Gera o logo do jogo.

        Parameters
        ----------
        x : int
            Coordenada x do logo.
        y : int
            Coordenada y do logo.

        Returns
        -------
        None.

        """
        start_logo_rect = self.start_logo.get_rect()
        start_logo_rect.midtop = (x, y)
        self.screen.blit(self.start_logo, start_logo_rect)

    def show_menu(self):
        """
        Gera o menu de Eulerphant's game.

        Returns
        -------
        None.

        """

        pygame.mixer.music.load(os.path.join(self.audiodir, c.MUSIC_START))
        pygame.mixer.music.play()

        self.show_logo(c.LARGURA/2, 20)

        self.show_text(
            "Pressione qualquer tecla para começar", 
            32, 
            c.AMARELO, 
            c.LARGURA/2, 
            300
        )        
        
        self.show_text(
            "Desenvolvido por Fernando, Max, Esther e Miguel", 
            16, 
            c.BRANCO, 
            c.LARGURA/2, 
            520
        )
        
        pygame.display.flip()
        self.wait_command()
    
    def show_pause(self):
        """
        Gera a tela de pausa do jogo.

        Returns
        -------
        None.

        """

        self.screen.fill(c.PRETO) 

        self.show_text(
            "Pause",
            40,
            c.AMARELO,
            c.LARGURA/2,
            300
        )

        self.show_text(
            "Pressione qualquer tecla para continuar", 
            25, 
            c.AMARELO, 
            c.LARGURA/2, 
            340
        )

        pygame.display.flip()
        self.wait_command()

    def wait_command(self):
        """
        Função auxiliar para eventos do pygame.

        Returns
        -------
        None.

        """
        waiting = True
        while waiting:
            self.clock.tick(c.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.is_running = False
                if event.type == pygame.KEYUP:
                    waiting = False
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound(os.path.join(self.audiodir, c.START_KEY)).play()
    
    def wait_space(self):
        """
        Função auxiliar para eventos do pygame.

        Returns
        -------
        None.

        """
        waiting = True
        while waiting:
            self.clock.tick(c.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and (self.game_over or self.game_won):
                        
                        self.game_over = False
                        self.game_won = False
                        self.startup_counter = 0
                        self.player_x = c.PLAYER_X
                        self.player_y = c.PLAYER_Y
                        self.direction = 0
                        self.direction_command = 0
                        self.powerup = False
                        self.power_count = 0

                        self.eaten_bees = [False, False, False, False]

                        for i in range(1,5):
                            exec(f'self.bee{i}_x = c.BEE{i}_X')
                            exec(f'self.bee{i}_y = c.BEE{i}_Y')
                            exec(f'self.bee{i}_direct = c.BEE{i}_DIRECTION')
                            exec(f'self.bee{i}_dead = c.BEE{i}_DEAD')
                        
                        self.score = 0
                        self.lives = 3
                        self.level = copy.deepcopy(c.BOARDS)
                        
                        waiting = False
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound(os.path.join(self.audiodir, c.START_KEY)).play()
    
    def show_game_over(self):
        """
        Função que gera a tela de game over.

        Returns
        -------
        None.

        """
        pygame.mixer.music.load(os.path.join(self.audiodir, c.MUSIC_GAME_OVER))
        pygame.mixer.music.play()

        self.screen.fill(c.PRETO) 

        self.show_text(
            "Game Over", 
            40, 
            c.AMARELO, 
            c.LARGURA/2, 
            300
        )

        self.show_text(
            "Pressione espaço para jogar de novo", 
            32, 
            c.AMARELO, 
            c.LARGURA/2, 
            340
        )        

        pygame.display.flip()
        self.wait_space()
    
    def show_game_won(self):
        """
        Função que gera a tela de game over.

        Returns
        -------
        None.

        """
        pygame.mixer.music.load(os.path.join(self.audiodir, c.MUSIC_WON))
        pygame.mixer.music.play()

        self.screen.fill(c.PRETO) 

        self.show_text(
            "Game Won", 
            40, 
            c.AMARELO, 
            c.LARGURA/2, 
            280
        )

        self.show_text(
            f"Score: {self.score}",
            30,
            c.AMARELO,
            c.LARGURA/2, 
            320
        )

        self.show_text(
            "Pressione espaço para jogar de novo", 
            32, 
            c.AMARELO, 
            c.LARGURA/2, 
            360
        )        

        pygame.display.flip()
        self.wait_space()
    
    def draw_bord(self, lvl):
        """
        Função que recebe uma matriz que representa o nível e o gera na tela.

        Parameters
        ----------
        lvl : list
            Matriz de inteiros em que cada inteiro corresponde a um desenho na
            tela.

        Returns
        -------
        None.

        """
        num1 = c.ALTURA_1
        num2 = c.LARGURA_1
        color = c.AZUL

        self.draw_misc()

        for i in range(len(lvl)):
            for j in range(len(lvl[i])):
                if lvl[i][j] == 1:
                    pygame.draw.circle(self.screen, c.BRANCO, (j * num2 + (0.5 * num2), i*num1 + (0.5*num1)), 3)
                if lvl[i][j] == 2 and not self.flicker:
                    pygame.draw.circle(self.screen, c.BRANCO, (j * num2 + (0.5 * num2), i*num1 + (0.5*num1)), 6)
                if lvl[i][j] == 3:
                    pygame.draw.line(self.screen, color, (j * num2 + (0.5 * num2), i*num1), (j * num2 + (0.5 * num2), i * num1 + num1), 2)
                if lvl[i][j] == 4:
                    pygame.draw.line(self.screen, color, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 2)
                if lvl[i][j] == 5:
                    pygame.draw.arc(self.screen, color, [(j*num2 - (num2 * 0.4)), (i*num1 +(0.5*num1)), num2, num1], 0, c.PI/2, 2)
                if lvl[i][j] == 6:
                    pygame.draw.arc(self.screen, color, [(j*num2 + (num2 * 0.5)), (i*num1 +(0.5*num1)), num2, num1], c.PI/2, c.PI, 2)
                if lvl[i][j] == 7:
                    pygame.draw.arc(self.screen, color, [(j*num2 + (num2 * 0.5)), (i*num1 - (0.4 * num1)), num2, num1], c.PI, 3*c.PI/2, 2)
                if lvl[i][j] == 8:
                    pygame.draw.arc(self.screen, color, [(j*num2 - (num2 * 0.4)), (i*num1 - (0.4 * num1)), num2, num1], 3*c.PI/2, 2*c.PI, 2)
                if lvl[i][j] == 9:
                    pygame.draw.line(self.screen, c.BRANCO, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 2)

    def draw_player(self):
        """
        Muda a posição da imagem do jogador caso ele mude de direção.

        Returns
        -------
        None.

        """
        # 0 = direita, 1 = esquerda, 2 = cima, 3 = baixo

        if self.direction == 0:
            self.screen.blit(pygame.transform.flip(s.PLAYER_IMAGES[self.counter // 5],True, False), (self.player_x, self.player_y))
        elif self.direction == 1:
            self.screen.blit(s.PLAYER_IMAGES[self.counter // 5], (self.player_x, self.player_y))
        elif self.direction == 2:
            self.screen.blit(pygame.transform.rotate(s.PLAYER_IMAGES[self.counter // 5], 270), (self.player_x, self.player_y))
        elif self.direction == 3:
            self.screen.blit(pygame.transform.rotate(s.PLAYER_IMAGES[self.counter // 5], 90), (self.player_x, self.player_y))

    def check_position(self, playerx, playery):
        """
        Função que verifica onde é permitido o elefante jogar, dependendo da
        atual posição.

        Parameters
        ----------
        playerx : int
            Coordenada x atual do jogador.
        playery : int
            Coordenada y atual do jogador.

        Returns
        -------
        turns : list
            Lista de booleanos que indica por qual direção o jogador pode andar.

        """
        turns = [False, False, False, False]
        centerx = playerx + 15
        centery = playery + 15
        num1 = c.ALTURA_1
        num2 = c.LARGURA_1
        num3 = c.NORMALIZACAO

        centery1 = math.floor(centery / num1)
        centery1_minus = math.floor((centery - num1) / num1)
        centery1_plus = math.floor((centery + num1) / num1)
        centery3_plus = math.floor((centery + num3) / num1)
        centery3_minus = math.floor((centery - num3) / num1)
        
        centerx2 = math.floor(centerx / num2)
        centerx2_plus = math.floor((centerx + num2) / num2)
        centerx2_minus = math.floor((centerx - num2) / num2)
        centerx3_minus = math.floor((centerx - num3) / num2)
        centerx3_plus = math.floor((centerx + num3) / num2)
        
        if centerx // 30 < 15:
            if self.direction == 0:
                if self.level[centery1][centerx3_minus] < 3:
                    turns[1] = True
            if self.direction == 1:
                if self.level[centery1][centerx3_plus] < 3:
                    turns[0] = True
            if self.direction == 2:
                if self.level[centery3_plus][centerx2] < 3:
                    turns[3] = True
            if self.direction == 3:
                if self.level[centery3_minus][centerx2] < 3:
                    turns[2] = True
            
            if self.direction == 2 or self.direction == 3:
                if 7 <= centerx % num2 <= 10:
                    if self.level[centery3_plus][centerx2] < 3:
                        turns[3] = True
                    if self.level[centery3_minus][centerx2] < 3:
                        turns[2] = True

                if 7 <= centery % num1 <= 10:
                    if self.level[centery1][centerx2_minus] < 3:
                        turns[1] = True
                    if self.level[centery1][centerx2_plus] < 3:
                        turns[0] = True
            
            if self.direction == 0 or self.direction == 1:
                if 7 <= centerx % num2 <= 10:
                    if self.level[centery1_plus][centerx2] < 3:
                        turns[3] = True
                    if self.level[centery1_minus][centerx2] < 3:
                        turns[2] = True

                if 7 <= centery % num1 <= 10:
                    if self.level[centery1][centerx3_minus] < 3:
                        turns[1] = True
                    if self.level[centery1][centerx3_plus] < 3:
                        turns[0] = True
                

        else:
            turns[0] = True
            turns[1] = True

        return turns

    def move_player(self, playerx, playery):
        """
        Função que move para onde o jogador queira, se possível.

        Parameters
        ----------
        playerx : int
            Coordenada x atual do jogador.
        playery : int
            Coordenada y atual do jogador.

        Returns
        -------
        playerx : int
            Nova coordenada x do jogador.
        playery : int
            Nova coordenada y do jogador.

        """

        if self.direction == 0 and self.turns_allowed[0]:
            playerx += c.PLAYER_SPEED
        elif  self.direction == 1 and self.turns_allowed[1]:
            playerx -= c.PLAYER_SPEED
        if self.direction == 2 and self.turns_allowed[2]:
            playery -= c.PLAYER_SPEED
        elif  self.direction == 3 and self.turns_allowed[3]:
            playery += c.PLAYER_SPEED
        
        return playerx, playery

    def check_collisions(self, score):
        """
        Atualiza o score a depender das colisões do jogador com outrem. Também
        muda o centro de colisões do jogador conforme ele anda.
        
        Parameters
        ----------
        score : int
            Score atual.

        Returns
        -------
        score: int
            Novo score.

        """
        centerx = self.player_x + 15
        centery = self.player_y + 15

        if 0 < self.player_x < 464:

            if self.level[math.floor(centery/c.ALTURA_1)][math.floor(centerx/c.LARGURA_1)] == 1:
                pygame.mixer.Sound(os.path.join(self.audiodir, c.MUSIC_PEANUT)).play()
                self.level[math.floor(centery/c.ALTURA_1)][math.floor(centerx/c.LARGURA_1)] = 0
                score += 10

            if self.level[math.floor(centery/c.ALTURA_1)][math.floor(centerx/c.LARGURA_1)] == 2:
                
                pygame.mixer.music.stop()
                pygame.mixer.music.load(os.path.join(self.audiodir, c.MUSIC_POWERUP))
                pygame.mixer.music.play()

                self.level[math.floor(centery/c.ALTURA_1)][math.floor(centerx/c.LARGURA_1)] = 0
                score += 50
                self.powerup = True
                self.power_count = 0
                self.eaten_bees = [False, False, False, False]
        
        return score

    def draw_misc(self):
        """
        Função que desenha outros detalhes da tela (score, vida).

        Returns
        -------
        None.

        """
        self.show_text(
            f'Score: {self.score:07}', 
            16,
            c.BRANCO,
            58,
            528)
        
        if self.powerup:
            pygame.draw.circle(self.screen, c.AZUL, (124, 536), 8)
        
        for i in range(self.lives):
            self.screen.blit(pygame.transform.scale(s.PLAYER_IMAGES[0], (20, 20)), (150 + (i * 30), 526))
        
        if self.game_over:
            self.is_running = False
            self.show_game_over()
        
        if self.game_won:
            self.is_running = False
            self.show_game_won()

    def get_target(self):
        
        if self.player_x < 240:
            runaway_x = 480
        else:
            runaway_x = 0
        
        if self.player_y < 256:
            runaway_y = 512
        else:
            runaway_y = 0

        return_target = (202, 228)

        if self.powerup:
            if not self.bee1.dead:
                bee1_target = (runaway_x, runaway_y)
            else:
                bee1_target = return_target

            if not self.bee2.dead:
                bee2_target = (runaway_x, self.player_y)
            else:
                bee2_target = return_target

            if not self.bee3.dead:
                bee3_target = (self.player_x, runaway_y)
            else:
                bee3_target = return_target

            if not self.bee4.dead:
                bee4_target = (240, 256)
            else:
                bee4_target = return_target
        else:
            if not self.bee1.dead:
                if self.bee1_box:
                    bee1_target = (c.LARGURA//2 - 15, 0)
                else:
                    bee1_target = (self.player_x, self.player_y)
            else:
                bee1_target = return_target

            if not self.bee2.dead:
                if self.bee2_box:
                    bee2_target = (c.LARGURA//2 - 15, 0)
                else:
                    bee2_target = (self.player_x, self.player_y)
            else:
                bee2_target = return_target

            if not self.bee3.dead:
                if self.bee3_box:
                    bee3_target = (c.LARGURA//2 - 15, 0)
                else:
                    bee3_target = (self.player_x, self.player_y)
            else:
                bee3_target = return_target

            if not self.bee4.dead:
                if self.bee4_box:
                    bee4_target = (c.LARGURA//2 - 15, 0)
                else:
                    bee4_target = (self.player_x, self.player_y)
            else:
                bee4_target = return_target

        return [bee1_target, bee2_target, bee3_target, bee4_target]

g = Game()
g.show_menu()

while g.is_running:

    g.new_game()

pygame.quit()


    











