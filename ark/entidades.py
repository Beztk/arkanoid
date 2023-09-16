# estándar
import os

# librerías de terceros
import pygame as pg

from random import randint

# mis imports
from . import ALTO, ANCHO


class Raqueta(pg.sprite.Sprite):
    margen = 25
    velocidad = 50

    def __init__(self):
        super().__init__()
        self.imagenes = []
        for i in range(0, 3):
            ruta_img = os.path.join('resources', 'images', f'electric0{i}.png')
            self.imagenes.append(pg.image.load(ruta_img))
        self.contador = 0
        self.image = self.imagenes[self.contador]

        self.rect = self.image.get_rect(midbottom=(ANCHO/2, ALTO-self.margen))

    def update(self):
        self.contador += 1
        if self.contador == 2:
            self.contador = 0
        self.image = self.imagenes[self.contador]

        pulsadas = pg.key.get_pressed()
        if pulsadas[pg.K_LEFT]:
            self.rect.left = self.rect.left - self.velocidad
        if pulsadas[pg.K_RIGHT]:
            self.rect.right = self.rect.right + self.velocidad

        # Limites del movimiento
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= ANCHO:
            self.rect.right = ANCHO


class Pelota(pg.sprite.Sprite):
    margen = 55
    velocidad = 20
    velreboteY = randint(0, 5)
    vely = randint(-5, 0)
    velx = 0
    while velx == 0:
        velx = randint(-velocidad, velocidad)

    def __init__(self, raqueta):
        super().__init__()
        self.imagenes = []
        for i in range(1, 6):
            img_balls = os.path.join('resources', 'images', f'ball{i}.png')
            self.imagenes.append(pg.image.load(img_balls))
        self.contador = 1
        self.image = self.imagenes[self.contador]

        self.raqueta = raqueta

    def update(self, partida_empezada):
        if not partida_empezada:
            self.rectp = self.image.get_rect(
                midbottom=self.raqueta.rect.midtop)
        else:
            self.rectp.x = self.rectp.x + self.velx
            self.rectp.y = self.rectp.y + self.vely

        if self.rectp.x <= 0:
            self.rectp.x = 0.2
            self.velx = -self.velx
        elif self.rectp.x >= 770:
            self.rectp.x = 770 - 0.2
            self.velx = -self.velx
        elif self.rectp.y <= 0:
            self.rectp.y = 0.2
            self.vely = -self.vely
            self.velreboteY = randint(0, 5)

        self.contador += 1
        if self.contador == 5:
            self.contador = 0
        self.image = self.imagenes[self.contador]


class Ladrillo(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ruta_verde = os.path.join('resources', 'images', 'greenTile.png')
        self.image = pg.image.load(ruta_verde)
        self.rect = self.image.get_rect()

        ruta_roja = os.path.join('resources', 'images', 'redTile.png')
        self.image2 = pg.image.load(ruta_roja)
        self.rect2 = self.image2.get_rect()

    def update(self):
        pass
