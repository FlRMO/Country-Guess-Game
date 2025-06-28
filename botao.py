import pygame
from Organizapais import formatar_bandeiras
from constantes import *

class Botao:
    def __init__(self, rect, texto, cor_fundo, cor_texto, fonte):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.fonte = fonte

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_fundo, self.rect, border_radius=8)
        self._desenhar_texto_multilinha(tela)

    def _desenhar_texto_multilinha(self, tela):
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
        y_offset = self.rect.y + (self.rect.height - altura_total) // 2

        for linha in linhas:
            texto_img = self.fonte.render(linha, True, self.cor_texto)
            x = self.rect.x + (self.rect.width - texto_img.get_width()) // 2
            tela.blit(texto_img, (x, y_offset))
            y_offset += self.fonte.get_height()

    def is_hover(self, pos):
        return self.rect.collidepoint(pos)