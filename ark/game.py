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

        # Escrito de forma abreviada
        # self.escenas = [
        #     Portada(self.pantalla),
        #     Partida(self.pantalla),
        #     MejoresJugadores(self.pantalla)
        # ]

    def jugar(self):
        # FIXME: evitar que el programa se cierre después de la pantalla de mejores jugadores
        for escena in self.escenas:
            he_acabado = escena.bucle_principal()
            if he_acabado:
                print('La escena me pide que acabe el juego')
                break
            # guardar estado actual
        print('He salido del bucle for de las escenas')

        pg.quit()


if __name__ == '__main__':
    print('Arrancamos desde el archivo game.py')
    juego = Arkanoid()
    juego.jugar()
