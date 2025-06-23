import pygame as pg

from pygame.locals import *
from sys import exit
from constantes import *
pg.init()

fonte_padrao = pg.font.SysFont(None, 36)


janela = pg.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pg.display.set_caption('Qual é o País?!')


while True:
    janela.fill(PRETO)
    for evento in pg.event.get():
        if evento.type == QUIT:
            pg.quit()
            exit()

    # AMBIENTES DE JOGOS
    # pg.draw.rect(janela,(200,200,200),(0,0,572,340)) #TEMP

    pg.draw.rect(janela, (CIANO), (0, 0, 572, ALTURAJANELA))  # TEMP

    pg.draw.rect(janela, (AMARELO), (XPAIS, YPAIS, LARGURAPAIS, ALTURAPAIS))

   # pg.draw.rect(janela,(AMARELO),(117,400,390,220)) #TEMP
    pg.draw.rect(janela, (AZUL),
                 (XOPCAO[0], YOPCAO[0], LARGURAOPCAO, ALTURAOPCAO))
    pg.draw.rect(janela, (AZUL),
                 (XOPCAO[0], YOPCAO[1], LARGURAOPCAO, ALTURAOPCAO))
    pg.draw.rect(janela, (AZUL),
                 (XOPCAO[1], YOPCAO[0], LARGURAOPCAO, ALTURAOPCAO))
    pg.draw.rect(janela, (AZUL),
                 (XOPCAO[1], YOPCAO[1], LARGURAOPCAO, ALTURAOPCAO))

    # AMBIENTE DO HUD
    pg.draw.rect(janela, (AMARELO), (XHUD, YHUD, LARGURAHUD, ALTURAHUD))
    pg.draw.rect(janela, (VERMELHO),
                 (XTITULO, YTITULO, LARGURATITULO, ALTURATITULO))
    pg.draw.rect(janela, (CINZA),
                 (XCAIXAPONTO[0], YCAIXAPONTO, LARGURACAIXAPONTO, ALTURACAIXAPONTO))
    pg.draw.rect(janela, (BRANCO),
                 (XPONTO[0], YPONTO, LARGURAPONTO, ALTURAPONTO))
    pg.draw.rect(janela, (CINZA),
                 (XCAIXAPONTO[1], YCAIXAPONTO, LARGURACAIXAPONTO, ALTURACAIXAPONTO))
    pg.draw.rect(janela, (BRANCO),
                 (XPONTO[1], YPONTO, LARGURAPONTO, ALTURAPONTO))
    pg.draw.rect(janela, (VERDE), (XVIDA[0], YVIDA, LARGURAVIDA, ALTURAVIDA))
    pg.draw.rect(janela, (VERDE), (XVIDA[1], YVIDA, LARGURAVIDA, ALTURAVIDA))
    pg.draw.rect(janela, (VERDE), (XVIDA[2], YVIDA, LARGURAVIDA, ALTURAVIDA))
    pg.draw.rect(janela, (ROXO), (XRECOMECAR, YRECOMECAR,
                 LARGURARECOMECAR, ALTURARECOMECAR))

    pg.display.flip()
