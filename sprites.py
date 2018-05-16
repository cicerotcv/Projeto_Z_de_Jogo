'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e Alexandre Cury

Jogo baseado na videoaula da ONG 'KidsCanCode', que ensina jovens à programar
	Canal no youtube: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
	Playlist usada para essa programação: https://www.youtube.com/playlist?list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq
	Fontes feitas por Brian Kent (Ænigma) 

Jogo feito em 2018

Aproveite!!!
'''

import pygame as pg
from configuracoes import *
vec = pg.math.Vector2

# Classe dedicada ao spritesheet:
class Spritesheet():
	def __init__(self, arquivo):
		self.spritesheet = pygame.image.load(arquivo).convert()

	# pega uma imagem do spritesheet
	def pegar_imagem(self, x, y, largura, altura):
		image = pygame.Surface ((largura, altura))
		image.blit(self.spritesheet, (0,0), (x, y, largura, altura))
		return image

# Sprite do jogador
class Jogador(pg.sprite.Sprite):
	def __init__(self, jogo):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.vida = 20
		self.pular = False
		self.image = pg.image.load("img/FatYoshi.png")
		self.rect = self.image.get_rect()
		self.posi = vec(largura * 1 / 2, altura - 50)
		self.velo = vec(0, 0)
		self.acele = vec(0, 0)
		self.pulador = 0

	# Movimento do personagem com teclas pressionadas
	def update(self):
		self.acele = vec(0, grav_jogador)
		keys = pg.key.get_pressed()
		if keys[pg.K_a]:
			self.acele.x = -acele_jogador
		if keys[pg.K_d]:
			self.acele.x = acele_jogador

		# Adiciona fricção à aceleração (útil no gelo)
		self.acele.x += self.velo.x * atrito_jogador
		# Velocidade somada com a aceleração
		self.velo += self.acele
		# Sorvetão (Indica a pórxima posição do personagem)
		self.posi += self.velo + 0.5 * self.acele
		# Define a posição do centro do personagem embaixo
		self.rect.midbottom = self.posi
		# Colisão com máscaras
		self.mask = pg.mask.from_surface(self.image)

	# Pulo do personagem
	def pulo(self):
		self.pular = False
		# Pular apenas com plataforma
		self.rect.y += 1
		colisao = pg.sprite.spritecollide(self, self.jogo.plataforma, False)
		self.rect.y -= 1

		# Zera o pulador se tem colisão
		if colisao:
		 	self.pular = True
		 	self.pulador = 0

		# Pula apenas se o número de pulos for menor que 2
		if self.pulador < 2:
			self.pular = True

		if self.pular:
			self.velo.y = -pulo_jogador
			self.pulador += 1

	def pulo_parar_meio(self):
		if self.pular:
			if self.velo.y < -5:
				self.velo.y = -5

# Sprite das plataformas
class Plataforma(pg.sprite.Sprite):
	def __init__(self, x, y, l, a):
		pg.sprite.Sprite.__init__(self)
		# self.image = pg.image.load("img/chao.png")
		self.image = pg.Surface((l, a))
		self.image.fill(ama_esc)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# Sprite do inimigo
class Inimigo(pg.sprite.Sprite):
	def __init__(self, jogo, posix, posiy):
		self.groups = jogo.todos_sprites, jogo.inimigos
		pg.sprite.Sprite.__init__(self, self.groups)
		self.jogo = jogo
		self.vida = 10
		self.image = pg.image.load("img/Golem.png")
		self.rect = self.image.get_rect()
		self.posi = vec(posix, posiy)
		self.velo = vec(0, 0)
		self.acele = vec(-10, 0)

	def update(self):
		# Gravidade
		self.acele = vec(0, grav_jogador)
		# Adiciona fricção à aceleração (útil no gelo)
		self.acele.x += self.velo.x * atrito_inimigo
		# Velocidade somada com a aceleração
		self.velo += self.acele
		# Sorvetão (Indica a pórxima posição do personagem)
		self.posi += self.velo + 0.5 * self.acele
		# Define a posição do centro
		self.rect.midbottom = self.posi
		# Colisão com máscara
		self.mask = pg.mask.from_surface(self.image)

# Sprite do tiro
class Tiro_reto(pg.sprite.Sprite):

	def __init__(self,jogo):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.posi = self.jogo.jogador.posi[:] + vec(10, -30)
		self.image = pg.image.load('img/Fireball.png')
		self.rect = self.image.get_rect()
		self.velo = vec(10, 0)
		self.jogo.todos_sprites.add(self)
		self.jogo.tiros.add(self)

	def update(self):
		self.posi += self.velo
		self.rect.center = self.posi

# Sprite da granada
class Tiro_parabola(pg.sprite.Sprite):
	def __init__(self,jogo):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.posi = self.jogo.jogador.posi[:] + vec(10, -30)
		self.image = pg.image.load('img/granada.png')
		self.rect = self.image.get_rect()
		self.velo = vec(10, -10)
		self.acele = vec(0, grav_jogador)
		self.jogo.todos_sprites.add(self)
		self.jogo.tiros.add(self)

	def update(self):
		self.velo.y += self.acele.y
		self.posi += self.velo + self.acele//2
		self.rect.center = self.po