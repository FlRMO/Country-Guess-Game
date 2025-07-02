import pygame
from pergunta import Pergunta
from hud import HUD
from botao import Botao
from Organizapais import formatar_bandeiras
from constantes import *

class Jogo:
    '''Classe principal do jogo, responsável por gerenciar o loop, lógica e interface.'''

    def __init__(self):
        '''Inicializa todos os componentes do jogo: janela, fontes, HUD, perguntas,
        bandeiras, pontuação, vidas e estado de fim.'''

        pygame.init()
        self.tela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
        pygame.display.set_caption("Qual é o País?!")
        self.fonte = pygame.font.SysFont(None, 36)

        self.fundo = pygame.image.load("fundos/fundo_jogo.png")
        self.bandeiras = formatar_bandeiras("Bandeiras") # Dicionário com nomes e caminhos das bandeiras
        self.hud = HUD()
        self.pergunta = Pergunta(list(self.bandeiras.keys()), self.bandeiras)

        self.pais_atual, self.imagem_atual, self.opcoes_atuais = self.pergunta.proxima()
        self.pontos = 0
        self.vidas = 3
        self.fim = False
        self.recomecar = False
        self.botoes_opcao = []

    def desenhar_botoes(self):
        '''Gera e desenha os botões das opções de resposta na tela.'''

        botoes = []
        espacoX = XOPCAO[1] - (LARGURAOPCAO + XOPCAO[0])
        espacoY = YOPCAO[1] - (ALTURAOPCAO + YOPCAO[0])

        for i, opcao in enumerate(self.opcoes_atuais): 
            linha = i // 2
            coluna = i % 2
            x = XOPCAO[0] + coluna * (LARGURAOPCAO + espacoX)
            y = YOPCAO[0] + linha * (ALTURAOPCAO + espacoY)

            '''# Destaca se o mouse estiver sobre o botão'''
            cor = (100, 149, 255) if pygame.Rect(x, y, LARGURAOPCAO, ALTURAOPCAO).collidepoint(pygame.mouse.get_pos()) else AZUL
            btn = Botao(pygame.Rect(x, y, LARGURAOPCAO, ALTURAOPCAO), opcao, cor, BRANCO, self.fonte)
            btn.desenhar(self.tela)
            botoes.append(btn)

        self.botoes_opcao = botoes

    def reiniciar(self):
        '''Reinicia todos os estados do jogo para uma nova partida.'''

        self.pergunta = Pergunta(list(self.bandeiras.keys()), self.bandeiras)
        self.pais_atual, self.imagem_atual, self.opcoes_atuais = self.pergunta.proxima()
        self.pontos = 0
        self.vidas = 3
        self.fim = False
        self.recomecar = False

    def atualizar_pergunta(self):
        '''Avança para a próxima pergunta, atualizando bandeira e opções.
        Caso não haja mais perguntas ou vidas, finaliza o jogo.'''

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
        '''Loop principal do jogo. Controla eventos, atualizações e renderização da tela.'''

        botao_recomecar = None
        aguardando_tempo = False # Controla tempo entre perguntas

        while True:
            self.tela.fill(CIANO)
            self.tela.blit(self.fundo, (0, 0)) # Fundo da interface
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
                     # Clique no botão de recomeçar
                    if self.recomecar and botao_recomecar and botao_recomecar.collidepoint(evento.pos):
                        self.reiniciar()

                    # Clique em opção de resposta
                    elif not self.fim and not aguardando_tempo:
                        for botao in self.botoes_opcao:
                            if botao.is_hover(evento.pos):
                                if botao.texto == self.pais_atual:
                                    self.pontos += 1 # Acertou
                                else:
                                    self.vidas -= 1 # Errou
                                aguardando_tempo = True
                                pygame.time.set_timer(pygame.USEREVENT, 500) # Aguarda 0,5s

                elif evento.type == pygame.USEREVENT:
                    self.atualizar_pergunta()
                    aguardando_tempo = False
                    self.recomecar = self.fim # Exibe botão de recomeçar se jogo tiver terminado
                    pygame.time.set_timer(pygame.USEREVENT, 0)

            pygame.display.update()