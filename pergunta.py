import pygame
import random
from constantes import *

class Pergunta:
    '''Representa a lógica de uma pergunta no jogo: sorteio de um país correto
    e geração de 3 alternativas erradas.

    Atributos:
        bandeiras (dict): mapeia nome do país para imagem.
        todos_paises (list): lista embaralhada de países disponíveis.
        indice_atual (int): posição atual na lista de perguntas.'''
    
    def __init__(self, paises, bandeiras):
        '''Inicializa o gerador de perguntas.

        Args:
            paises (list): nomes legíveis dos países.
            bandeiras (dict): mapeia país -> caminho da imagem.'''
        
        self.bandeiras = bandeiras
        self.todos_paises = paises
        self.indice_atual = 0
        random.shuffle(self.todos_paises)

    def proxima(self):
        '''Retorna a próxima pergunta, contendo o país correto, sua bandeira
        e uma lista de 4 opções (1 certa + 3 erradas).

        Returns:
            tuple: (nome do país correto, imagem da bandeira, lista de opções)'''
        
        if self.indice_atual >= len(self.todos_paises):
            return None, None, []

        pais_correto = self.todos_paises[self.indice_atual]
        imagem = pygame.image.load(self.bandeiras[pais_correto])
        
        opcoes = [pais_correto]
        while len(opcoes) < 4:
            candidato = random.choice(list(self.bandeiras.keys()))
            if candidato not in opcoes:
                opcoes.append(candidato)
        random.shuffle(opcoes) # Embaralha a ordem das alternativas

        return pais_correto, imagem, opcoes

    def avancar(self):
        '''Avança para o próximo índice de pergunta.'''
        self.indice_atual += 1