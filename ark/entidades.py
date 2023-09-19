# estándar
import os
from random import randint

# librerías de terceros
import pygame as pg

# mis imports
from . import ALTO, ANCHO, VEL_MAX, VEL_MIN_Y, ALTO_MARCADOR


class Raqueta(pg.sprite.Sprite):
    """
    1. Debe ser de tipo Sprite (herencia) -- DONE
    2. Se puede mover (método)
        2.1 Leer el teclado
        2.2 Límites de movimiento (no debe salir de la pantalla)
    3. Pintarse (método) -- DONE
    4. Volver a la posición inicial (método)
    5. Velocidad  --- DONE
    """

    margen = 25
    velocidad = 20

    def __init__(self):
        super().__init__()

        self.imagenes = []
        for i in range(3):
            ruta_img = os.path.join('resources', 'images', f'electric0{i}.png')
            self.imagenes.append(pg.image.load(ruta_img))

        self.contador = 0
        self.image = self.imagenes[self.contador]

        self.rect = self.image.get_rect(midbottom=(ANCHO/2, ALTO-self.margen))

    def update(self):
        # 00 -> 01 -> 02 -> 00 -> 01 -> 02
        self.contador += 1
        if self.contador > 2:
            self.contador = 0
        self.image = self.imagenes[self.contador]

        pulsadas = pg.key.get_pressed()
        if pulsadas[pg.K_LEFT]:
            self.rect.x -= self.velocidad
            if self.rect.left < 0:
                self.rect.left = 0
        if pulsadas[pg.K_RIGHT]:
            self.rect.x += self.velocidad
            if self.rect.right > ANCHO:
                self.rect.right = ANCHO


class Ladrillo(pg.sprite.Sprite):
    VERDE = 0
    ROJO = 1
    ROJO_ROTO = 2
    IMG_LADRILLO = ['greenTile.png', 'redTile.png', 'redTileBreak.png']

    def __init__(self, puntos, color=VERDE):
        super().__init__()
        self.tipo = color
        self.imagenes = []
        for img in self.IMG_LADRILLO:
            ruta = os.path.join(
                'resources', 'images', img)
            self.imagenes.append(pg.image.load(ruta))
        self.image = self.imagenes[color]
        self.rect = self.image.get_rect()
        self.puntos = puntos

    def update(self, muro):
        if self.tipo == Ladrillo.ROJO:
            self.tipo = Ladrillo.ROJO_ROTO
        else:
            muro.remove(self)
        self.image = self.imagenes[self.tipo]


class Pelota(pg.sprite.Sprite):

    def __init__(self, raqueta):
        super().__init__()
        self.image = pg.image.load(
            os.path.join('resources', 'images', 'ball1.png')
        )
        self.rect = self.image.get_rect(midbottom=raqueta.rect.midtop)
        self.raqueta = raqueta
        self.inicializar_velocidades()
        self.he_perdido = False

    def inicializar_velocidades(self):
        self.vel_x = randint(-VEL_MAX, VEL_MAX)
        self.vel_y = randint(-VEL_MAX, VEL_MIN_Y)

    def update(self, se_mueve_la_pelota):
        if not se_mueve_la_pelota:
            self.rect = self.image.get_rect(midbottom=self.raqueta.rect.midtop)
        else:
            self.rect.x += self.vel_x
            if self.rect.left <= 0 or self.rect.right > ANCHO:
                self.vel_x = -self.vel_x

            self.rect.y += self.vel_y
            if self.rect.top <= ALTO_MARCADOR:
                self.vel_y = -self.vel_y

            if self.rect.top >= ALTO:
                self.inicializar_velocidades()
                self.he_perdido = True

            if pg.sprite.collide_mask(self, self.raqueta):
                self.inicializar_velocidades()


class ContadorVidas:
    def __init__(self, vidas_iniciales):
        self.vidas = vidas_iniciales

    def perder_vida(self):
        self.vidas -= 1
        return self.vidas < 0

    def pintar(self):
        pass


class Marcador:
    def __init__(self):
        self.valor = 0
        fuente = 'LibreFranklin-VariableFont_wght.ttf'
        ruta = os.path.join('resources', 'fonts', fuente)
        self.tipo_letra = pg.font.Font(ruta, 35)

    def aumentar(self, incremento):
        self.valor += incremento

    def pintar(self, pantalla):
        s = pg.rect.Rect(0, 0, ANCHO, ALTO_MARCADOR)
        pg.draw.rect(pantalla, (0, 0, 0), s)
        cadena = str(self.valor)
        texto = self.tipo_letra.render(cadena, True, (230, 189, 55))
        pos_x = 20
        pos_y = 10
        pantalla.blit(texto, (pos_x, pos_y))
