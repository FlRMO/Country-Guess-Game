import pygame

from constantes import *

class Botao:
    '''Classe responsável por representar um botão com texto centralizado
    e possível quebra de linha, que pode ser desenhado na tela.

    Atributos:
        rect (pygame.Rect): área do botão.
        texto (str): texto a ser exibido.
        cor_fundo (tuple): cor do fundo do botão.
        cor_texto (tuple): cor do texto.
        fonte (pygame.font.Font): fonte usada no texto.'''
    
    def __init__(self, rect, texto, cor_fundo, cor_texto, fonte):
        '''Inicializa um botão.

        Args:
            rect (tuple): coordenadas e dimensões do botão (x, y, largura, altura).
            texto (str): texto a ser exibido no botão.
            cor_fundo (tuple): cor do fundo do botão.
            cor_texto (tuple): cor do texto.
            fonte (pygame.font.Font): fonte utilizada para o texto.'''
        
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.fonte = fonte

    def desenhar(self, tela):
        '''Desenha o botão na tela, com cantos arredondados e o texto formatado.

        Args:
            tela (pygame.Surface): superfície onde o botão será desenhado.'''
        
        pygame.draw.rect(tela, self.cor_fundo, self.rect, border_radius=8)
        self._desenhar_texto_multilinha(tela)

    def _desenhar_texto_multilinha(self, tela):
        '''Renderiza o texto do botão com quebras de linha automáticas, mantendo
        a centralização horizontal e vertical.

        Args:
            tela (pygame.Surface): superfície onde o texto será desenhado.'''
        
        palavras = self.texto.split()
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            teste = linha_atual + (" " if linha_atual else "") + palavra
            if self.fonte.size(teste)[0] <= self.rect.width:
                linha_atual = teste
            else:
                linhas.append(linha_atual)
                linha_atual = palavra
        if linha_atual:
            linhas.append(linha_atual)

        altura_total = len(linhas) * self.fonte.get_height()
        y_offset = self.rect.y + (self.rect.height - altura_total) // 2 # Centraliza verticalmente

        for linha in linhas:
            texto_img = self.fonte.render(linha, True, self.cor_texto) # Renderiza linha
            x = self.rect.x + (self.rect.width - texto_img.get_width()) // 2 # Centraliza horizontalmente
            tela.blit(texto_img, (x, y_offset))
            y_offset += self.fonte.get_height()

    def is_hover(self, pos):
        '''Verifica se uma posição (x, y) está dentro do botão.

        Args:
            pos (tuple): posição do mouse.
        Returns:
            bool: True se estiver sobre o botão, False caso contrário.'''
        
        return self.rect.collidepoint(pos)