import pygame as pg

from . import ALTO, ANCHO
from .escenas import MejoresJugadores, Partida, Portada


class Arkanoid:
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))

        portada = Portada(self.pantalla)
        partida = Partida(self.pantalla)
        records = MejoresJugadores(self.pantalla)

        self.escenas = [
            portada,
            partida,
            records
        ]

    def jugar(self):
        for escena in self.escenas:
            he_acabado = escena.bucle_principal()
            if he_acabado:
                break

        pg.quit()


if __name__ == '__main__':
    juego = Arkanoid()
    juego.jugar()
