import pygame
from constantes import *

class HUD:
    '''Classe que responsável por representar o HUD (barra lateral com pontos, vidas, etc.)
    
    Atributos:
        fonte (pygame.font.SysFont) = Fonte padrão do jogo.
        fonte_titulo (pygame.font.SysFont) = Fonte do título (textos que aparecem no HUD).
        vida_img (pygame.image.load)= Imagem de coração que representa as vidas (possibilidades de erro) do jogo.'''

    def __init__(self):
        '''Inicializa um HUD.'''
        
        self.fonte = pygame.font.SysFont(None, 36)
        self.fonte_titulo = pygame.font.SysFont(None, 46)
        self.vida_img = pygame.image.load("fundos/vida_hud.png")

    def desenhar_texto(self, tela, texto, x, y, cor=PRETO, largura_max=200, altura_max=100, fonte_usada=None):
        '''Renderiza o título do HUD com quebras de linha automáticas, mantendo
        a centralização horizontal.

        Args:
            tela (pygame.Surface): superfície onde o texto será desenhado.
            texto (str): texto que será desenhado.
            x (int): posição do eixo x de onde o texto será desenhado.
            y (int): posição do eixo y de onde o texto será desenhado.
            cor (tuple): tupla contendo a cor do texto, em padrão RGB (R,G,B).
            largura_max (int): largura máxima que o texto que será desenhado deve ter.
            altura_max (int): altura máxima que o texto que será desenhado deve ter.
            fonte_usada (pygame.font.SysFont): fonte que será aplicada no texto que será desenhado.'''
        
        fonte_usada = fonte_usada or self.fonte
        palavras = texto.split()
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            teste = linha_atual + (" " if linha_atual else "") + palavra
            if fonte_usada.size(teste)[0] <= largura_max:
                linha_atual = teste
            else:
                linhas.append(linha_atual)
                linha_atual = palavra
        if linha_atual:
            linhas.append(linha_atual)

        altura_total = len(linhas) * fonte_usada.get_height()
        y_offset = y + (altura_max - altura_total) // 2

        for linha in linhas:
            img = fonte_usada.render(linha, True, cor)
            x_centralizado = x + (largura_max - img.get_width()) // 2
            tela.blit(img, (x_centralizado, y_offset))
            y_offset += fonte_usada.get_height()

    def desenhar(self, tela, pontos, vidas, fim_de_jogo, mostrar_recomecar):
        '''Desenha os componentes do HUD.

        Args:
            tela (pygame.Surface): superfície onde os componentes serão desenhados.
            pontos (int): número que representa a quantidade de acertos.
            vidas (int): entidade que representa as vidas.
            fim_de_jogo (bool): condição que define se o jogo acabou (falta de países ou de vidas).
            mostrar_recomecar (bool): condição que define se deve ou não mostrar o botão de reiniciar o jogo.'''
        
        pygame.draw.rect(tela, CINZA, (XHUD, YHUD, LARGURAHUD, ALTURAHUD))

        titulo = "Fim do Jogo!" if fim_de_jogo else "Acerte o País!"
        self.desenhar_texto(tela, titulo, XTITULO, YTITULO, PRETO, LARGURATITULO, ALTURATITULO, self.fonte_titulo)

        pygame.draw.rect(tela, CIANO, (XCAIXAPONTO, YCAIXAPONTO, LARGURACAIXAPONTO, ALTURACAIXAPONTO))
        self.desenhar_texto(tela, "Pontuação:", XCAIXAPONTO, YCAIXAPONTO, BRANCO, LARGURACAIXAPONTO, ALTURACAIXAPONTO)

        pygame.draw.rect(tela, BRANCO, (XPONTO, YPONTO, LARGURAPONTO, ALTURAPONTO))
        self.desenhar_texto(tela, f"{pontos}/194", XPONTO, YPONTO, PRETO, LARGURAPONTO, ALTURAPONTO)

        for i in range(vidas):
            tela.blit(self.vida_img, (XVIDA[i], YVIDA))

        if mostrar_recomecar: #se mostrar recomeçar é True...
            botao_rect = pygame.Rect(XRECOMECAR, YRECOMECAR, LARGURARECOMECAR, ALTURARECOMECAR)
            cor = (100, 149, 255) if botao_rect.collidepoint(pygame.mouse.get_pos()) else AZUL
            pygame.draw.rect(tela, cor, botao_rect, border_radius=8)
            self.desenhar_texto(tela, "Recomeçar", XRECOMECAR, YRECOMECAR, BRANCO, LARGURARECOMECAR, ALTURARECOMECAR)
            return botao_rect
        return None