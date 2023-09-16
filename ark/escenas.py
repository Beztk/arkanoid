# estándar
import os

# librerías de terceros
import pygame as pg

# tus dependencias
from . import ALTO, ANCHO, FPS
from .entidades import Raqueta, Pelota, Ladrillo


class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        print('Método vacío bucle principal de ESCENA')


class Portada(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta = os.path.join('resources', 'images', 'arkanoid_name.png')
        self.logo = pg.image.load(ruta)

        ruta = os.path.join('resources', 'fonts', 'CabinSketch-Bold.ttf')
        self.tipo = pg.font.Font(ruta, 35)

    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    salir = True
            self.pantalla.fill((99, 0, 0))
            self.pintar_logo()
            self.pintar_mensaje()
            pg.display.flip()
        return False

    def pintar_logo(self):
        ancho, alto = self.logo.get_size()
        pos_x = (ANCHO - ancho) / 2
        pos_y = (ALTO - alto) / 2
        self.pantalla.blit(self.logo, (pos_x, pos_y))

    def pintar_mensaje(self):
        mensaje = "Pulsa <ESPACIO> para comenzar la partida"
        texto = self.tipo.render(mensaje, True, (255, 255, 255))
        pos_x = (ANCHO - texto.get_width()) / 2
        pos_y = ALTO * 3 / 4
        self.pantalla.blit(texto, (pos_x, pos_y))


class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta_fondo = os.path.join('resources', 'images', 'Fondo.jpg')
        self.fondo = pg.image.load(ruta_fondo)
        self.jugador = Raqueta()
        self.pelota = Pelota(self.jugador)
        self.muro = pg.sprite.Group()

    def bucle_principal(self):
        super().bucle_principal()
        self.crear_muro()
        salir = False
        juego_iniciado = False
        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    juego_iniciado = True

            self.pintar_fondo()
            self.jugador.update()
            self.pantalla.blit(self.jugador.image,
                               self.jugador.rect)
            self.pelota.update(juego_iniciado)
            self.pantalla.blit(self.pelota.image,
                               self.pelota.rectp)

            self.muro.draw(self.pantalla)

            pg.display.flip()

    def pintar_fondo(self):
        self.pantalla.fill((0, 99, 0))
        self.pantalla.blit(self.fondo, (0, 0))

    def crear_muro(self):
        filas = 4
        columnas = 6
        margen_superior = 20

        for f in range(filas):
            for c in range(columnas):
                ladrillo = Ladrillo()
                margen_izquierdo = (ANCHO - columnas * ladrillo.rect.width) / 2
                ladrillo.rect.x = ladrillo.rect.width * c + margen_izquierdo
                ladrillo.rect.y = ladrillo.rect.height * f + margen_superior
                self.muro.add(ladrillo)


class MejoresJugadores(Escena):
    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
            self.pantalla.fill((0, 0, 99))
            pg.display.flip()
