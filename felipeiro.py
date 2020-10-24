import sys
import pygame
import time
import math
import random

TELA_X = 480
TELA_Y = 640

pygame.init()

COLOR_R = (0xFF,0x00,0x00)
COLOR_G = (0x00,0xFF,0x00)
COLOR_B = (0x00,0x00,0xFF)
COLOR_WHITE = (0xFF,0XFF,0xFF)
COLOR_BLACK = (0,0,0)

BLACK = COLOR_BLACK
RED = COLOR_R

screen = pygame.display.set_mode([TELA_Y, TELA_X])

pygame.display.set_caption('Mundo dos Felipeiros')

screen.fill(COLOR_BLACK)

def desenhaCenario(buffer, fundo = None):
    pad = 10
    borda = 4
    
    if fundo:
        screen.blit(fundo, (0,0))
    else:
    
        #pygame.draw.line(buffer, COLOR_WHITE, [pad, pad], [pad, TELA_Y-pad], 2)
        #pygame.draw.line(buffer, COLOR_WHITE, [pad, pad], [TELA_X-pad, pad], 2)
        #pygame.draw.line(buffer, COLOR_WHITE, [TELA_X, pad], [TELA_X-10, pad], 2)
        
        
       
        pygame.draw.rect(buffer, COLOR_WHITE, [pad, pad, TELA_Y-2*pad, TELA_X-2*pad])
        pygame.draw.rect(buffer, COLOR_BLACK, [pad+borda, pad+borda, 
        TELA_Y-2*(pad+borda), TELA_X-2*(pad+borda)])
        #pygame.draw.rect(buffer, COLOR_BLACK, [pad+2, pad+2, TELA_Y-pad-2, TELA_X-pad-2])
        #pygame.draw.ellipse(buffer, COLOR_R, [300, 200, 40, 40])
        #pygame.draw.polygon(buffer, COLOR_G, [[420, 200], [440, 240], [400, 240]])
    

class Personagem(pygame.sprite.Sprite):
    """
    Personagem
    """
    
    def __init__(self, vel=2, posx=10, posy=10):
        pygame.sprite.Sprite.__init__(self)
        self.imageL = pygame.image.load('dinoL.png')
        self.imageR = pygame.image.load('dinoR.png')
        
        self.image = self.imageR
        self.rect = self.image.get_rect()
        self.velocidade = vel
        self.rect.x = posx
        self.rect.y = posy
        self.vel = vel
        self.vida = 3
        self.item = 0

        self.eventoMudaFase = False
    
 
    
    def handle_keys(self):
        
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.image = self.imageL
            self.rect.move_ip(0-self.vel, 0)
            
            
        if key[pygame.K_RIGHT] and self.rect.right < TELA_Y:
            self.image = self.imageR
            self.rect.move_ip(self.vel, 0)
     
        if key[pygame.K_UP] and self.rect.top > 0: 
           self.rect.move_ip(0, 0-self.vel)
           
        if key[pygame.K_DOWN] and self.rect.bottom < TELA_X :
           self.rect.move_ip(0, self.vel) 
     
    def update(self):
        if self.item >= 2:
            self.eventoMudaFase = True
        #self.rect.x += self.velocidade
        #if self.rect.left > 640:
        #    self.rect.right = 0

# alguns bitmaps para o cenário e items do jogo:

fundo = pygame.image.load('samplemap.png')   

coracao = pygame.image.load('coracao.png')

borda = pygame.image.load('borda.png')

cerebroItem = pygame.image.load('cerebroitem.png')

class Inventario:
    """
    mostra os itens que o jogador pegou no topo da tela
    """
    def __init__(self, jogador):
        self.slots = 4
        self.proprietario = jogador
        self.cerebroItem = pygame.image.load('cerebroitem.png')
        self.borda = pygame.image.load('borda.png')
        self.itens = list()
        self.posx = 490
        self.posy = 5
        self.font = pygame.font.SysFont(None, 19)
        self.text = self.font.render("Itens", True, COLOR_B)

    def draw(self, screen):

        x = self.posx # posicao base horizontal
        y = self.posy # posicao base vertical

        if self.proprietario.item > 0:
             screen.blit(self.cerebroItem, (x+10, y+19))
        if  self.proprietario.item > 1:
             screen.blit(self.cerebroItem, (x+40, y+19))

        screen.blit(self.borda, (x, y))
        screen.blit(self.text, [x+45, y+5])  


class cerebro(pygame.sprite.Sprite):

    """
    Cérebro para coletas, quando mais o dino pega, mais inteligente ele fica
    Ele é um item, removido quando o personagem passa por ele atraves
    da funcao de colisoes, usar o self.rect para interface desta função
    """
    def __init__(self, posx=10, posy=10, lista = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('cerebro.png')
        self.rect = self.image.get_rect()
        self.velocidade = 1
        self.rect.x = posx
        self.posx = posx
        self.rect.y = posy
        self.x = 0
        self.fase = random.random()
        self.emMovimento = True

        if lista is not None:
            lista.add(self)
      
    def update(self):

        espaco = 20

        if self.emMovimento:
        
            self.rect.x = self.posx + math.cos(2*self.x+self.fase)*espaco
            self.x += 0.01
            
            if self.x > 2*math.pi:
                self.x = 0
        else:
            pass # fica na posição atual

    def pega(self):
        self.rect.x = -1000
        self.kill()
 
class morcegao(pygame.sprite.Sprite):
    """
    morcegão é um dos inimigos
    ele não faz nada, apenas retira 1 de vida ao colidir com ele e em seguida ele some
    """

    count = 0

    def __init__(self, x=300, y=200, x_vel=1, y_vel=1, lista=None):
        pygame.sprite.Sprite.__init__(self)
        morcegao.count+=1
        self.id = morcegao.count
        self.image = pygame.image.load('morcegao.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = x_vel
        self.velocity_y = y_vel
        self.posx = float(x_vel)
        self.vida = 1

        print(f"bicho - nasci:{self.id}")

        if lista is not None:
            lista.add(self)
    
    def die(self): # morre diabo:
        self.rect.x = -1000 # gambiarra clássica
        self.vida = 0
        self.kill()
        print(f"bicho - ai, morri {self.id}")
       
      
    def update(self):
 
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # mudando a direção no eixo x nas bordas
        if self.rect.x > 600: self.velocity_x *= -1
        elif self.rect.x < 0: self.velocity_x *= -1

        # mudando a direção no eixo y nas bordas
        if self.rect.y > 440: self.velocity_y *= -1
        elif self.rect.y < 0: self.velocity_y *= -1
        
      
class Artefato(pygame.sprite.Sprite):

    def __init__(self,arquivo, x=10, y=10, listagem = None, habilitado = False):
        super().__init__()

        try:
            self.image = pygame.image.load(arquivo)
            self.rect = self.image.get_rect()

        except pygame.error as message:
            print(f"falha ao carrega o sprite: {arquivo} -- {message}")
            return

        if listagem is not None:
            listagem.add(self)
       
        self.rect.x = -9999
        self.rect.y = y
        self.habilitado = habilitado
        self.inicialx = x


    def draw(self, screen):
        pass
        #if self.habilitado:
        #    screen.blit(self.image, self.rect)
            
    def update(self):
        if self.habilitado:
            self.rect.x = self.inicialx
        else:
            self.rect.x = -9999


        
def barraDeVida(buffer,personagem):

    if personagem.vida > 0:
        buffer.blit(coracao, (10,10))

    if personagem.vida > 1:
        buffer.blit(coracao, (42,10))
        
    if personagem.vida > 2:
        buffer.blit(coracao, (74,10))
    
def barraDeItem(buffer,personagem):
     if personagem.item > 0:
         screen.blit(cerebroItem,(500,24))
     if personagem.item > 1:
         screen.blit(cerebroItem,(530,24))
        
        
class Bola:
    """ Estilo Allegro do C/C++"""
    
    def __init__(self, x=300, y=200, x_vel = 1, y_vel=1, dim=40, cor=(255,0,0)):
        # variáveis da bola
        self.position_x = x # inicial
        self.position_y = y # inicial
        self.velocity_x = x_vel
        self.velocity_y = y_vel
        self.diametro = dim
        self.cor = cor
    
        self.colisor = pygame.Rect(self.position_x, self.position_y, self.diametro-5, self.diametro-5)
    
    def draw(self, buffer):
        pos = [self.position_x, self.position_y, self.diametro, self.diametro]
        self.colisor.x = self.position_x
        self.colisor.y = self.position_y
        pygame.draw.ellipse(buffer, self.cor, pos)
     
    def auto_move(s):
        s.position_x += s.velocity_x
        s.position_y += s.velocity_y

        # mudando a direção no eixo x nas bordas
        if s.position_x > 600: s.velocity_x *= -1
        elif s.position_x < 0: s.velocity_x *= -1

        # mudando a direção no eixo y nas bordas
        if s.position_y > 440: s.velocity_y *= -1
        elif s.position_y < 0: s.velocity_y *= -1
    

class Texto:
    def __init__(self, str, x=10, y=10, color=(0,0,0), fundo=True):
    
        self.font = pygame.font.SysFont("sourcecodepro", 15)
        self.str = str
        self.text = self.font.render(str, True, color)
        self.x = x
        self.y = y
        self.fundo = fundo
    
    def printf(self, buffer):
        tam = 9*len(self.str)
        pad = 2
        if self.fundo:
            pygame.draw.rect(buffer, COLOR_WHITE, [self.x-pad, self.y-pad, tam+pad*2,20+pad])
        buffer.blit(self.text, [self.x, self.y])
        

# inicializar componentes:

bolinha = Bola()
bolão = Bola(100,100,0.2,0.3,dim=30, cor=COLOR_G)
jogador = Personagem(2,1,10)

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(jogador)

# coloca items no mapa:
cerebroA = cerebro(130,343, all_sprites_list)
cerebroB = cerebro(430,243, all_sprites_list)
 
# coloca bichos no mapa:
morcegoA = morcegao(40,90, lista=all_sprites_list)
morcegoB = morcegao(130,140, lista=all_sprites_list)
 
listaItens = [cerebroA, cerebroB]
listaBichos = [morcegoA, morcegoB]

portal = Artefato("portal.png", 500, 180, all_sprites_list)

def processaColisoes(jogador, items, bichos, artefatos=None):
     
    for bicho in bichos:
        
        if jogador.rect.colliderect(bicho.rect):
            bicho.die()
            jogador.vida -= 1

    for item in items:
        if jogador.rect.colliderect(item.rect):
            item.pega()
            jogador.item += 1
    
    if artefatos is not None:
        for item in artefatos:
          if jogador.rect.colliderect(item.rect):
            pass


colisores = [x.rect for x in [morcegoA, morcegoB, cerebroA, cerebroB]]


meuTexto = Texto("Encontre os cérebros para aumenta a rede neural",100,440)
equacoa = Texto("resolver 2X + 1 = 0",100,460,color=COLOR_R, fundo=False)
items = Texto("itens", 528, 5, color = COLOR_B, fundo=False)

barraItems = Inventario(jogador)

def dist(x,y,x2,y2):
    return math.sqrt((x-x2)**2 + (y-y2)**2)

def distRect(rectA,rectB):
    x, y = rectA.midtop[0], rectA.midleft[1]
    x2, y2 = rectB.midtop[0], rectB.midleft[1]

    return math.sqrt((x-x2)**2 + (y-y2)**2)

def eventoFaseNova(screen):
     portal.habilitado = True
     # colisao simples (radial) :
     if distRect(jogador.rect, portal.rect) < 10:
        print("fim da fase")

# Main Loop:
clock = pygame.time.Clock()

while True:

    dt = clock.tick(120) # maximo fps
    
    # preenchendo o fundo com preto
    screen.fill(BLACK)
    
    # capturando eventos usando o polling
    event = pygame.event.poll()
   
    # evento QUIT (ao clicar no x da janela):
    if event.type == pygame.QUIT:
        print("saindo do programa...")
        # sair do loop e termina o programa
        break
    
    jogador.handle_keys()
    
    desenhaCenario(screen, fundo)

    all_sprites_list.update()
    all_sprites_list.draw(screen)

    processaColisoes(jogador, listaItens, listaBichos)
   
    barraDeVida(screen,jogador)
    barraItems.draw(screen)   
    
    meuTexto.printf(screen) # objetivo da fase
    equacoa.printf(screen)

    if jogador.eventoMudaFase:
        eventoFaseNova(screen)
        
    pygame.display.update() # exibe o screen (buffer) na tela

print("pronto")
