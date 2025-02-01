# src/entidades/pooka.py

import pygame
import random
from math import sin, cos, pi
from pygame import Vector2, Color
from .espirito_base import EspiritoBase
from ..util.constantes import CORES, PARAMS_GENETICOS, CONFIGURACAO_ESPIRITOS

class Pooka(EspiritoBase):
    """
    Pooka: Espírito travesso da mitologia celta.
    Conhecido por suas transformações e natureza brincalhona,
    o Pooka se manifesta como uma luz púrpura que ocasionalmente
    revela traços de suas formas animais (coelho/cavalo).
    """
    def __init__(self, posicao_inicial: tuple):
        # Inicializa a classe base
        super().__init__(posicao_inicial, "POOKA")
        
        # Genes específicos do Pooka
        self.genes.update({
            'travessura': random.uniform(*PARAMS_GENETICOS['POOKA']['TRAVESSURA']),
            'forma_animal': random.random(),  # 0 = mais coelho, 1 = mais cavalo
            'intensidade_transformacao': 0.0  # Quanto da forma animal está visível
        })
        
        # Estados específicos do Pooka
        self.tempo_ultima_travessura = 0
        self.em_transformacao = False
        self.angulo_orelhas = 0.0  # Para animação das orelhas
        
        # Cores específicas do Pooka
        self.cor_base = Color(*CORES['POOKA']['NUCLEO'])
        self.cor_aura = Color(*CORES['POOKA']['AURA'])

    def _desenhar_nucleo(self):
        """
        Desenha o núcleo do Pooka, que pode mostrar traços
        sutis de coelho ou cavalo dependendo de seus genes.
        """
        tamanho = CONFIGURACAO_ESPIRITOS['TAMANHO_BASE']
        centro = tamanho // 2
        
        # Desenha o núcleo básico (círculo luminoso)
        pygame.draw.circle(
            self.superficie_nucleo,
            self.cor_base,
            (centro, centro),
            int(tamanho * 0.4 * self.genes['tamanho'])
        )
        
        # Adiciona traços animais baseados nos genes
        if self.genes['intensidade_transformacao'] > 0.2:
            self._desenhar_tracos_animais(centro, tamanho)

    def _desenhar_tracos_animais(self, centro, tamanho):
        """
        Desenha sutis características de coelho ou cavalo.
        A forma varia suavemente baseada nos genes e estado.
        """
        if self.genes['forma_animal'] < 0.5:  # Mais traços de coelho
            # Desenha orelhas longas e finas
            angulo_base = self.angulo_orelhas + sin(self.fase_animacao) * 0.2
            for i in [-1, 1]:  # Orelha esquerda e direita
                ponta_orelha = (
                    centro + cos(angulo_base) * tamanho * 0.5 * i,
                    centro - sin(angulo_base) * tamanho * 0.6
                )
                pygame.draw.line(
                    self.superficie_nucleo,
                    self.cor_base,
                    (centro, centro - tamanho * 0.2),
                    ponta_orelha,
                    int(3 * self.genes['intensidade_transformacao'])
                )
        else:  # Mais traços de cavalo
            # Desenha uma crina etérea
            for i in range(5):
                offset = sin(self.fase_animacao + i) * 5
                ponto1 = (centro - tamanho * 0.3, centro - tamanho * 0.2 + i * 4)
                ponto2 = (centro - tamanho * 0.1 + offset, centro - tamanho * 0.3 + i * 4)
                pygame.draw.line(
                    self.superficie_nucleo,
                    self.cor_base,
                    ponto1,
                    ponto2,
                    int(2 * self.genes['intensidade_transformacao'])
                )

    def _desenhar_aura(self):
        """
        Desenha a aura mística do Pooka, que pulsa e cintila
        baseado em seu nível de energia e estado emocional.
        """
        tamanho = self.superficie_aura.get_width()
        centro = tamanho // 2
        raio_base = tamanho * 0.3
        
        # Cria múltiplas camadas de aura com diferentes opacidades
        for i in range(3):
            raio = raio_base * (1 + i * 0.3) * self.pulso_aura
            cor_atual = (*CORES['POOKA']['AURA'][:3],
                int(100 * (1 - i * 0.3)))
            
            pygame.draw.circle(
                self.superficie_aura,
                cor_atual,
                (centro, centro),
                int(raio)
            )

    def _desenhar_efeitos(self):
        """
        Desenha efeitos especiais como rastros de luz e
        pequenas faíscas mágicas que o Pooka deixa ao se mover.
        """
        if self.velocidade.length() > 0.5:
            self._desenhar_rastro_magico()
        if self.genes['travessura'] > 0.6:
            self._desenhar_faiscas()

    def _desenhar_rastro_magico(self):
        """Desenha um rastro mágico que segue o movimento do Pooka"""
        tamanho = self.superficie_efeitos.get_width()
        centro = tamanho // 2
    
    def _desenhar_faiscas(self):
        """
         Desenha pequenas faíscas mágicas ao redor do Pooka quando ele está travesso.
         As faíscas são pequenos pontos de luz que aparecem em posições aleatórias
         próximas ao núcleo do espírito, criando um efeito de energia mágica brincalhona.
        """
        
        tamanho = self.superficie_efeitos.get_width()
        centro = tamanho // 2
        raio_efeito = tamanho * 0.4
        
        # Numero de faíscas baseado no nível de travessura
        num_faiscas = int(5 * self.genes['travessura'])
        
        for _ in range(num_faiscas):
            # Posição aleatória em torno do centro
            angulo = random.uniform(0, 2 * pi)
            distancia = random.uniform(0, raio_efeito)
            x = centro + cos(angulo) * distancia
            y = centro + sin(angulo) * distancia
        
            # Tamanho aleatório para cada faísca
            tamanho_faisca = random.uniform(1, 3)
        
            # A opacidade varia com o tempo para criar um efeito cintilante
            opacidade = int(200 * (0.5 + 0.5 * sin(self.fase_animacao * 5)))
            cor_faisca = (*self.cor_base[:3], opacidade)
        
            # Desenha a faísca como um pequeno círculo brilhante
            pygame.draw.circle(
                self.superficie_efeitos,
                cor_faisca,
                (int(x), int(y)),
                tamanho_faisca
            )            
        
        # Calcula pontos do rastro baseado na direção do movimento
        dir_normalizada = self.velocidade.normalize()
        for i in range(5):
            pos = Vector2(
                centro - dir_normalizada.x * (i * 8),
                centro - dir_normalizada.y * (i * 8)
            )
            
            opacidade = int(50 * (1 - i/5))
            cor_rastro = (*self.cor_base[:3], opacidade)
            
            pygame.draw.circle(
                self.superficie_efeitos,
                cor_rastro,
                pos,
                int(4 * (1 - i/5))
            )

    def atualizar(self, delta_tempo):
        """
        Atualiza o estado do Pooka, incluindo suas transformações
        e comportamentos específicos.
        """
        super().atualizar(delta_tempo)
        
        # Atualiza a transformação
        self._atualizar_transformacao(delta_tempo)
        
        # Chance de fazer travessuras baseada nos genes
        self._tentar_travessura(delta_tempo)
        
        self._atualizar_visual()

    def _atualizar_transformacao(self, delta_tempo):
        """
        Gerencia a transformação gradual entre formas.
        O Pooka pode mostrar mais ou menos características animais.
        """
        if random.random() < 0.01:  # Chance de iniciar transformação
            self.em_transformacao = not self.em_transformacao
        
        # Suaviza a transição entre formas
        alvo = 0.8 if self.em_transformacao else 0.0
        self.genes['intensidade_transformacao'] += (
            (alvo - self.genes['intensidade_transformacao']) * delta_tempo * 2
        )

    def _tentar_travessura(self, delta_tempo):
        """
        Tenta realizar uma travessura baseada nos genes de travessura.
        As travessuras são puramente visuais, como brilhos e faíscas.
        """
        self.tempo_ultima_travessura += delta_tempo
        if (self.tempo_ultima_travessura > 5.0 and 
            random.random() < self.genes['travessura'] * 0.1):
            self.tempo_ultima_travessura = 0
            self.em_transformacao = True