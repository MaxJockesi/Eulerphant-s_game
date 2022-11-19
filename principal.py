import pygame
import constantes as c
import sprites
import os, sys

class Game:
    def __init__(self):
        #criando a tela do jogo
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((c.LARGURA, c.ALTURA))
        pygame.display.set_caption(c.TITULO_JOGO)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.font = pygame.font.match_font(c.FONTE)
        self.upload_files()
    
    def new_game(self):
        #Instancia as classes das sprites
        self.all_sprites = pygame.sprite.Group()
        self.run()
    
    def run(self):
        #loop do jogo
        self.playing = True
        while self.playing:
            self.clock.tick(c.FPS)
            self.events()
            self.update_sprites()
            self.plot_sprites()
    
    def events(self):
        #define eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.is_running = False
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.show_pause()
    
    def update_sprites(self):
        #atualiza os sprites
        self.all_sprites.update()
    
    def plot_sprites(self):
        #desenha as sprites
        self.screen.fill(c.PRETO) #limpa a tela
        self.all_sprites.draw(self.screen) #desenha as sprites na tela
        pygame.display.flip()
    
    def upload_files(self):
        #carrega os arquivis de audio e imagens
        imagesdir = os.path.join(os.getcwd(), "imagens")
        self.audiodir = os.path.join(os.getcwd(), "audios")
        self.spritesheet = os.path.join(imagesdir, c.SPRITESHEET)
        self.start_logo = os.path.join(imagesdir, c.LOGO)
        self.start_logo = pygame.image.load(self.start_logo).convert()

    def show_text(self, txt, size, color, x, y):
        #exibe um texto na tela do jogo
        font = pygame.font.Font(self.font, size)
        text = font.render(txt, False, color)
        text_rect = text.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text, text_rect)
    
    def show_logo(self, x, y):
        start_logo_rect = self.start_logo.get_rect()
        start_logo_rect.midtop = (x, y)
        self.screen.blit(self.start_logo, start_logo_rect)

    def show_menu(self):

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
            "Desenvolvido por Fernando de Magalhães, Max e Ester", 
            19, 
            c.BRANCO, 
            c.LARGURA/2, 
            570
        )
        
        pygame.display.flip()
        self.wait_command()
    
    def show_pause(self):

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
    
    def show_game_over(self):

        self.show_text(
            "Game Over", 
            40, 
            c.AMARELO, 
            c.LARGURA/2, 
            300
        )

        self.show_text(
            "Pressione qualquer tecla", 
            32, 
            c.AMARELO, 
            c.LARGURA/2, 
            340
        )        

        pygame.display.flip()
        self.wait_command()


g = Game()
g.show_menu()

while g.is_running:
    g.new_game()
    g.show_game_over()

    











