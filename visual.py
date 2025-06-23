import pygame as pg

from pygame.locals import *
from sys import exit

pg.init()

janela = pg.display.set_mode((900, 400))
pg.display.set_caption('Qual é o País?!')

while True:
    janela.fill((0, 0, 0))
    for evento in pg.event.get():
        if evento.type == QUIT:
            pg.quit()
            exit()

    pg.display.flip()
