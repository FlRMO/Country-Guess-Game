import pygame
import random
from Organizapais import formatar_bandeiras
from constantes import *


pygame.init()

tela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption("Qual é o País?!")


fonte = pygame.font.SysFont(None, 36)
fonte_titulo = pygame.font.SysFont(None, 46)


fundo_jogo = pygame.image.load('fundos/fundo_jogo.png')
vida_hud = pygame.image.load('fundos/vida_hud.png')


bandeiras = formatar_bandeiras('Bandeiras')
todos_paises = list(bandeiras.keys())
random.shuffle(todos_paises)
indice_atual = 0
vidas_restantes = 3
pontos = 0
fim_de_jogo = False
mostrar_botao_recomecar = False


def desenhar_texto(texto, x, y, cor=PRETO, largura_max=200, altura_max=100, fonte_usada=None):
    fonte_usada = fonte_usada or fonte  

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


def nova_pergunta():
    global indice_atual

    
    if indice_atual >= len(todos_paises):
        return None, None, []

    pais_correto = todos_paises[indice_atual]
    imagem = pygame.image.load(bandeiras[pais_correto])

    opcoes = [pais_correto]
    while len(opcoes) < 4:
        candidato = random.choice(list(bandeiras.keys()))
        if candidato not in opcoes:
            opcoes.append(candidato)

    random.shuffle(opcoes)
    
    return pais_correto, imagem, opcoes


def desenhar_alternativas(opcoes):
    botoes = []
    largura_botao = LARGURAOPCAO
    altura_botao = ALTURAOPCAO
    espacoX = XOPCAO[1] - (LARGURAOPCAO + XOPCAO[0])
    espacoY = YOPCAO[1] - (ALTURAOPCAO + YOPCAO[0])
    colunas = 2
    pos_x0 = XOPCAO[0]
    pos_y0 = YOPCAO[0]

    mouse_pos = pygame.mouse.get_pos()

    for i, opcao in enumerate(opcoes):
        linha = i // colunas
        coluna = i % colunas

        x = pos_x0 + coluna * (largura_botao + espacoX)
        y = pos_y0 + linha * (altura_botao + espacoY)

        ret = pygame.Rect(x, y, largura_botao, altura_botao)

        
        cor_botao = (100, 149, 255) if ret.collidepoint(mouse_pos) else AZUL  # Azul claro se hover
        pygame.draw.rect(tela, cor_botao, ret, border_radius=8)

        desenhar_texto(opcao, x, y, BRANCO, largura_botao, altura_botao)
        botoes.append((ret, opcao))

    return botoes


def desenhar_hud():
    
    hud_rect = pygame.Rect(XHUD, YHUD, LARGURAHUD, ALTURAHUD)
    pygame.draw.rect(tela, CINZA, hud_rect)

    
    titulo_texto = "Acerte o País!" if not fim_de_jogo else "Fim do Jogo!"
    desenhar_texto(titulo_texto, XTITULO, YTITULO, PRETO,
                   LARGURATITULO, ALTURATITULO, fonte_titulo)

    
    caixa_pontos = pygame.Rect(
        XCAIXAPONTO, YCAIXAPONTO, LARGURACAIXAPONTO, ALTURACAIXAPONTO)
    pygame.draw.rect(tela, CIANO, caixa_pontos)
    desenhar_texto("Pontuação:", XCAIXAPONTO, YCAIXAPONTO,
                   BRANCO, LARGURACAIXAPONTO, ALTURACAIXAPONTO)

    
    tela_pontos = pygame.Rect(XPONTO, YPONTO, LARGURAPONTO, ALTURAPONTO)
    pygame.draw.rect(tela, BRANCO, tela_pontos)
    desenhar_texto(f"{pontos}/194", XPONTO, YPONTO,
                   PRETO, LARGURAPONTO, ALTURAPONTO)

   
    for i in range(vidas_restantes):
        tela.blit(vida_hud, (XVIDA[i], YVIDA))

    
    if mostrar_botao_recomecar:
        botao_rect = pygame.Rect(
            XRECOMECAR, YRECOMECAR, LARGURARECOMECAR, ALTURARECOMECAR)

        mouse_pos = pygame.mouse.get_pos()
        cor_botao = (100, 149, 255) if botao_rect.collidepoint(mouse_pos) else AZUL  # Hover azul claro

        pygame.draw.rect(tela, cor_botao, botao_rect, border_radius=8)
        desenhar_texto("Recomeçar", XRECOMECAR, YRECOMECAR,
                    BRANCO, LARGURARECOMECAR, ALTURARECOMECAR)
        return botao_rect
    return None


pais_atual, imagem_atual, opcoes_atuais = nova_pergunta()

botao_recomecar = None
rodando = True
while rodando:
    tela.fill(CIANO)
    tela.blit(fundo_jogo, (0, 0))
    tela.blit(imagem_atual, (XPAIS, YPAIS))

    opcoes = []
    if opcoes_atuais:
        opcoes = desenhar_alternativas(opcoes_atuais)


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if mostrar_botao_recomecar and botao_recomecar and botao_recomecar.collidepoint(evento.pos):
                random.shuffle(todos_paises)
                indice_atual = 0
                vidas_restantes = 3
                pontos = 0
                fim_de_jogo = False
                mostrar_botao_recomecar = False
                pais_atual, imagem_atual, opcoes_atuais = nova_pergunta()

            
            elif opcoes_atuais:
                for ret, nome in opcoes:
                    if ret.collidepoint(evento.pos):
                        if nome == pais_atual:
                            pontos += 1
                            indice_atual += 1  
                        else:
                            vidas_restantes -= 1
                        pygame.time.set_timer(pygame.USEREVENT, 500)


        elif evento.type == pygame.USEREVENT:
            nova = nova_pergunta()
            if nova[0] is None or vidas_restantes <= 0:
                fim_de_jogo = True
                mostrar_botao_recomecar = True
                opcoes_atuais = []  
            else:
                pais_atual, imagem_atual, opcoes_atuais = nova

            pygame.time.set_timer(pygame.USEREVENT, 0)

    botao_recomecar = desenhar_hud()
    pygame.display.update()

pygame.quit()
