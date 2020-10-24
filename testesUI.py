# teste de colisoes e sprites

import sys
import pygame
import time
import math
import random

WIDTH = 640
HEIGHT = 480

UP = 8
LEFT = 4
DOWN = 2
RIGHT = 6

def hex_to_rgb(value):
	value = value.lstrip('#')
	lv = len(value)
	return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

class Color:
	BLACK = (0,0,0)			#000000
	WHITE = (255,255,255)	#FFFFFF
	RED = (255,0,0)			#FF0000
	LIME = (0,255,0)		#00FF00
	BLUE = (0,0,255)		#0000FF
	YELLOW = (255,255,0)	#FFFF00
	CYAN = (0,255,255)		#00FFFF
	MAGENTA = (255,0,255)	#FF00FF
	SILVER = (192,192,192)	#C0C0C0
	GRAY = (128,128,128)	#808080
	MAROON = (128,0,0)		#800000
	OLIVE = (128,128,0)		#808000
	GREEN = (0,128,0)		#008000
	PURPLE = (128,0,128)	#800080
	TEAL = (0,128,128)		#008080
	NAVY = (0,0,128)		#000080

C = Color

class Bar:
	"""barra de vida e atributos
	"""
	def __init__(self,x=1,y=1, color = (0xFF,0,0), name="HP"):
		self.x = x
		self.y = y
		self.h = 19
		self.w = 155
		self.hp = 3
		self.color = color

	def modura(self, buffer):
		pygame.draw.rect(buffer, Color.WHITE, [self.x-1,self.y-1,self.w+2,self.h+2])
		pygame.draw.rect(buffer, Color.BLACK, [self.x,self.y,self.w,self.h])

		myNewSurface = pygame.Surface((self.w, self.h))

		myNewSurface.fill((10,10,50))

		for x in range(self.hp): self.gomo(myNewSurface,x)
		 
		buffer.blit(myNewSurface,[self.x,self.y])

	def gomo(self,buffer,mul=0):
		pad = 3
		sobra = 2
		bx = 0 + pad + mul*15
		by = 0 + pad 
		pygame.draw.rect(buffer, Color.WHITE, [bx,by,13,13 ])
		pygame.draw.rect(buffer, self.color, [bx + sobra,by + 0, 13-sobra,13-sobra ])

class Obstaculo:
	def __init__(self):
		a = random.uniform(10, WIDTH-10)
		b = random.uniform(10, HEIGHT-10)

		self.rect = pygame.Rect(a,b,50,50)

	def draw(self, buffer):
		pygame.draw.rect(buffer,Color.MAROON,self.rect)


class Personagem:
	def __init__(self,x=10,y=10,h=10,w=10):
		self.vel = 5
		self.rect = pygame.Rect(x,y,w,h)
		self.dir = 'Z'
		self.colisores = []
		self.bateu = False

	def setColisores(self,lista_obstaculos):
		try:
			self.colisores = [item.rect for item in lista_obstaculos]
		except Exception as e:
			self.colisores = list()
			print(f"opa, mapa limpo? {e}")
	 

	def handle_keys(self):

		key = pygame.key.get_pressed()

		if key[pygame.K_LEFT] and self.rect.left > 0:

			self.dir = LEFT
			self.rect.move_ip(0-self.vel, 0)

			 
		if key[pygame.K_RIGHT] and self.rect.right < WIDTH:

			self.dir = RIGHT
			self.rect.move_ip(self.vel, 0)

		if key[pygame.K_UP] and self.rect.top > 0: 
			self.dir = UP
			self.rect.move_ip(0, 0-self.vel)
		   
		if key[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
			self.dir = DOWN
			self.rect.move_ip(0, self.vel) 

	def colidir(self):
		self.bateu = ( self.rect.collidelist(self.colisores) > -1 )

		for block in colisores:

			if self.rect.colliderect(block):

				if self.dir == LEFT:
					self.rect.x = block.x + block.w

				if self.dir == RIGHT:
					self.rect.x = block.x - self.rect.w 

				if self.dir == DOWN:
					self.rect.y = block.y - self.rect.h

				if self.dir == UP:
					self.rect.y = block.y + block.h


	def draw(self, buffer):
		color = Color.RED if self.bateu else Color.LIME
		pygame.draw.rect(buffer, color, self.rect)
		 
	def update(self,buffer):
		self.handle_keys()
		self.colidir()
		self.draw(buffer)

# inicia o jogo
pygame.init()

# configura tela
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# titulo da janela
pygame.display.set_caption('Mundo de testes')

# relogio para controle de fps e timers
clock = pygame.time.Clock()

# barras de vida, mana, etc...
bar = Bar(x=10, y=20)
barx = Bar(x=10, y=50, color = Color.BLUE)
barx.hp = 10 #set hp inicial
bary = Bar(10,80, hex_to_rgb("#004e22"))

# instancia o jogador (personagem principal)
jogador = Personagem(300,200,30,30)

# instancia os obstaculos e já cria uma lista deles
obstaculos = [Obstaculo() for _ in range(10)]
 
# listagem dos blocos de colisao
colisores = [obs.rect for obs in obstaculos]

# personagem "conhece" as colisoes
jogador.setColisores(obstaculos)

# configura a fonte padrao:
font = pygame.font.SysFont("sourcecodepro", 15)

while True:

	dt = clock.tick(120) # maximo fps
	
	# preenchendo o fundo com preto
	screen.fill(Color.PURPLE)
	
	# capturando eventos usando o polling
	event = pygame.event.poll()
	event_key = pygame.key.get_pressed()
   
	if event.type == pygame.QUIT:
		print("saindo do programa...")
		break

	if event_key[pygame.K_ESCAPE]: break

	for peso in obstaculos: peso.draw(screen)
 
	screen.blit(font.render(f"x:{jogador.rect.x} - y:{jogador.rect.y}", True, Color.BLACK), [285,425])

	jogador.update(screen)

	bar.modura(screen)
	barx.modura(screen)
	bary.modura(screen)

	pygame.display.update()

print("pronto, encerrado")