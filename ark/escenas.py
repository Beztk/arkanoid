# estándar
import os

# librerías de terceros
import pygame as pg

# tus dependencias
from . import ALTO, ANCHO, FPS, VIDAS
from .entidades import ContadorVidas, Ladrillo, Marcador, Pelota, Raqueta


class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        """
        Este método debe ser implementado por todas y cada una de las escenas,
        en función de lo que estén esperando hasta la condición de salida.
        """
        print('Método vacío bucle principal de ESCENA')


class Portada(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        # windows: resources\images\arkanoid_name.png
        # mac/linux: resources/images/arkanoid_name.png
        ruta = os.path.join('resources', 'images', 'arkanoid_name.png')
        self.logo = pg.image.load(ruta)

        ruta = os.path.join('resources', 'fonts', 'CabinSketch-Bold.ttf')
        self.tipo = pg.font.Font(ruta, 35)

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en el bucle principal de PORTADA')
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
        ruta_fondo = os.path.join('resources', 'images', 'background.jpg')
        self.fondo = pg.image.load(ruta_fondo)
        self.jugador = Raqueta()
        self.muro = pg.sprite.Group()
        self.pelota = Pelota(self.jugador)
        self.contador_vidas = ContadorVidas(VIDAS)
        self.marcador = Marcador()

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en el bucle principal de PARTIDA')
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
            self.pantalla.blit(self.jugador.image, self.jugador.rect)

            self.muro.draw(self.pantalla)

            self.pelota.update(juego_iniciado)
            self.pantalla.blit(self.pelota.image, self.pelota.rect)

            golpeados = pg.sprite.spritecollide(self.pelota, self.muro, False)
            if len(golpeados) > 0:
                for ladrillo in golpeados:
                    eliminados = len(self.muro)
                    ladrillo.update(self.muro)
                    if len(self.muro) < eliminados:
                        self.marcador.aumentar(ladrillo.puntos)
                self.pelota.vel_y = -self.pelota.vel_y

            self.marcador.pintar(self.pantalla)

            pg.display.flip()

            if self.pelota.he_perdido:
                # acciones cada vez que pierdo una vida
                salir = self.contador_vidas.perder_vida()
                self.pelota.he_perdido = False
                juego_iniciado = False

    def pintar_fondo(self):
        self.pantalla.fill((0, 0, 99))
        # TODO: mejorar la lógica para "rellenar" el fondo
        self.pantalla.blit(self.fondo, (0, 0))
        self.pantalla.blit(self.fondo, (600, 0))
        self.pantalla.blit(self.fondo, (0, 800))
        self.pantalla.blit(self.fondo, (600, 800))

    def crear_muro(self):
        filas = 6
        columnas = 9
        margen_superior = 100
        tipo = None

        for fila in range(filas):   # 0-3
            for col in range(columnas):
                # por aquí voy a pasar filas*columnas = 24 veces
                if tipo == Ladrillo.ROJO:
                    tipo = Ladrillo.VERDE
                else:
                    tipo = Ladrillo.ROJO
                puntos = (tipo+1)*(20-fila*2)
                ladrillo = Ladrillo(puntos, tipo)
                margen_izquierdo = (ANCHO - columnas * ladrillo.rect.width) / 2
                # x = ancho_lad * col
                # y = alto_lad * fila
                ladrillo.rect.x = ladrillo.rect.width * col + margen_izquierdo
                ladrillo.rect.y = ladrillo.rect.height * fila + margen_superior
                self.muro.add(ladrillo)
                print(tipo, fila, col, puntos)


class MejoresJugadores(Escena):
    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en el bucle principal de MEJORESJUGADORES')
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
            self.pantalla.fill((0, 99, 0))
            pg.display.flip()
