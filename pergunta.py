import pygame
import random
from Organizapais import formatar_bandeiras
from constantes import *

class Pergunta:
    '''Seleciona o país da rodada, embaralha e monta as 4 alternativas'''
    def __init__(self, paises, bandeiras):
        self.bandeiras = bandeiras
        self.todos_paises = paises
        self.indice_atual = 0
        random.shuffle(self.todos_paises)

    def proxima(self):
        if self.indice_atual >= len(self.todos_paises):
            return None, None, []

        pais_correto = self.todos_paises[self.indice_atual]
        imagem = pygame.image.load(self.bandeiras[pais_correto])
        
        opcoes = [pais_correto]
        while len(opcoes) < 4:
            candidato = random.choice(list(self.bandeiras.keys()))
            if candidato not in opcoes:
                opcoes.append(candidato)
        random.shuffle(opcoes)

        return pais_correto, imagem, opcoes

    def avancar(self):
        self.indice_atual += 1