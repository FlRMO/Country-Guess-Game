import pygame
from pergunta import Pergunta
from hud import HUD
from botao import Botao
from Organizapais import formatar_bandeiras
from constantes import *

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
        pygame.display.set_caption("Qual é o País?!")
        self.fonte = pygame.font.SysFont(None, 36)

        self.fundo = pygame.image.load("fundos/fundo_jogo.png")
        self.bandeiras = formatar_bandeiras("Bandeiras")
        self.hud = HUD()
        self.pergunta = Pergunta(list(self.bandeiras.keys()), self.bandeiras)

        self.pais_atual, self.imagem_atual, self.opcoes_atuais = self.pergunta.proxima()
        self.pontos = 0
        self.vidas = 3
        self.fim = False
        self.recomecar = False
        self.botoes_opcao = []

    def desenhar_botoes(self):
        botoes = []
        espacoX = XOPCAO[1] - (LARGURAOPCAO + XOPCAO[0])
        espacoY = YOPCAO[1] - (ALTURAOPCAO + YOPCAO[0])

        for i, opcao in enumerate(self.opcoes_atuais): 
            linha = i // 2
            coluna = i % 2
            x = XOPCAO[0] + coluna * (LARGURAOPCAO + espacoX)
            y = YOPCAO[0] + linha * (ALTURAOPCAO + espacoY)

            cor = (100, 149, 255) if pygame.Rect(x, y, LARGURAOPCAO, ALTURAOPCAO).collidepoint(pygame.mouse.get_pos()) else AZUL
            btn = Botao(pygame.Rect(x, y, LARGURAOPCAO, ALTURAOPCAO), opcao, cor, BRANCO, self.fonte)
            btn.desenhar(self.tela)
            botoes.append(btn)

        self.botoes_opcao = botoes

    def reiniciar(self):
        self.pergunta = Pergunta(list(self.bandeiras.keys()), self.bandeiras)
        self.pais_atual, self.imagem_atual, self.opcoes_atuais = self.pergunta.proxima()
        self.pontos = 0
        self.vidas = 3
        self.fim = False
        self.recomecar = False

    def atualizar_pergunta(self):
        if self.vidas <= 0:
            self.fim = True
            self.opcoes_atuais = []
        else:
            self.pergunta.avancar()
            nova = self.pergunta.proxima()
            if nova[0] is None:
                self.fim = True
                self.opcoes_atuais = []
            else:
                self.pais_atual, self.imagem_atual, self.opcoes_atuais = nova

    def executar(self):
        botao_recomecar = None
        aguardando_tempo = False

        while True:
            self.tela.fill(CIANO)
            self.tela.blit(self.fundo, (0, 0))
            if self.imagem_atual:
                self.tela.blit(self.imagem_atual, (XPAIS, YPAIS))

            if self.opcoes_atuais:
                self.desenhar_botoes()

            botao_recomecar = self.hud.desenhar(self.tela, self.pontos, self.vidas, self.fim, self.recomecar)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.recomecar and botao_recomecar and botao_recomecar.collidepoint(evento.pos):
                        self.reiniciar()

                    elif not self.fim and not aguardando_tempo:
                        for botao in self.botoes_opcao:
                            if botao.is_hover(evento.pos):
                                if botao.texto == self.pais_atual:
                                    self.pontos += 1
                                else:
                                    self.vidas -= 1
                                aguardando_tempo = True
                                pygame.time.set_timer(pygame.USEREVENT, 500)

                elif evento.type == pygame.USEREVENT:
                    self.atualizar_pergunta()
                    aguardando_tempo = False
                    self.recomecar = self.fim
                    pygame.time.set_timer(pygame.USEREVENT, 0)

            pygame.display.update()