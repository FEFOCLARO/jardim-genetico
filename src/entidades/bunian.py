# src/entidades/bunian.py

import pygame
import random
from math import sin, cos, pi
from pygame import Vector2, Color, Surface
from .espirito_base import EspiritoBase
from ..util.constantes import CORES, PARAMS_GENETICOS

class Bunian(EspiritoBase):
    """
    Bunian: Espírito etéreo da mitologia malaia.
    São seres que existem em um plano paralelo ao nosso,
    podendo se manifestar com diferentes níveis de visibilidade.
    Sua forma é mais humanóide e graciosa, com movimentos fluidos.
    """
    def __init__(self, posicao_inicial: tuple):
        super().__init__(posicao_inicial, "BUNIAN")
        
        # Genes específicos do Bunian que influenciam sua manifestação
        self.genes.update({
            'invisibilidade': random.uniform(*PARAMS_GENETICOS['BUNIAN']['INVISIBILIDADE']),
            'graciosidade': random.uniform(0.6, 1.0),
            'harmonia': random.uniform(0.4, 0.9)  # Afeta a interação com outros
        })
        
        # Estados e atributos específicos
        self.nivel_manifestacao = 1.0  # Quão visível está (1.0 = totalmente visível)
        self.tempo_transicao = 0.0
        self.particulas_luz = []  # Para efeito de brilho
        
        # Cores do Bunian - tons de azul etéreo
        self.cor_base = Color(*CORES['BUNIAN']['NUCLEO'])
        self.cor_aura = Color(*CORES['BUNIAN']['AURA'])
        
        # Superfície adicional para efeitos de transparência
        self.superficie_transicao = Surface((
            self.superficie_nucleo.get_width(),
            self.superficie_nucleo.get_height()
        ), pygame.SRCALPHA)

    def _desenhar_nucleo(self):
        """
        Desenha o núcleo do Bunian com forma humanóide etérea.
        O desenho é mais suave e fluido, representando sua natureza etérea.
        """
        tamanho = self.superficie_nucleo.get_width()
        centro = tamanho // 2
        
        # Ajusta a cor base baseado no nível de manifestação
        cor_atual = self.cor_base.copy()
        cor_atual.a = int(255 * self.nivel_manifestacao)
        
        # Desenha a forma base humanóide
        self._desenhar_forma_humanoide(centro, tamanho, cor_atual)
        
        # Adiciona detalhes etéreos
        self._desenhar_detalhes_etereos(centro, tamanho, cor_atual)

    def _desenhar_forma_humanoide(self, centro, tamanho, cor):
        """
        Desenha uma forma humanóide suave e etérea.
        A forma é mais sugestiva do que definida, mantendo o mistério.
        """
        # Silhueta central suave
        altura_corpo = tamanho * 0.6
        largura_corpo = tamanho * 0.3
        
        # Desenha o corpo como uma série de círculos sobrepostos
        # para criar uma forma mais orgânica e fluida
        pontos_corpo = [
            (centro, centro - altura_corpo * 0.4),  # Cabeça
            (centro, centro - altura_corpo * 0.2),  # Pescoço
            (centro, centro),                       # Tronco
            (centro, centro + altura_corpo * 0.2)   # Base
        ]
        
        for i, (x, y) in enumerate(pontos_corpo):
            raio = largura_corpo * (0.7 if i == 0 else 1.0)  # Cabeça menor
            pygame.draw.circle(
                self.superficie_nucleo,
                cor,
                (int(x), int(y)),
                int(raio * self.genes['tamanho'])
            )

    def _desenhar_detalhes_etereos(self, centro, tamanho, cor):
        """
        Adiciona detalhes etéreos como véus e ondulações luminosas
        que dão ao Bunian sua aparência característica.
        """
        # Cria véus etéreos usando curvas suaves
        pontos_veu = []
        num_pontos = 8
        raio = tamanho * 0.4
        
        for i in range(num_pontos):
            angulo = (i / num_pontos) * 2 * pi + self.fase_animacao
            offset = sin(angulo * 3 + self.fase_animacao) * 5
            x = centro + cos(angulo) * (raio + offset)
            y = centro + sin(angulo) * (raio + offset)
            pontos_veu.append((x, y))
        
        # Desenha véus conectando os pontos
        if len(pontos_veu) > 2:
            pygame.draw.lines(
                self.superficie_nucleo,
                cor,
                True,  # Fecha o polígono
                pontos_veu,
                int(2 * self.genes['graciosidade'])
            )

    def _desenhar_aura(self):
        """
        Desenha a aura do Bunian, que é mais suave e etérea,
        com padrões ondulantes que sugerem sua natureza dimensional.
        """
        tamanho = self.superficie_aura.get_width()
        centro = tamanho // 2
        
        # Cria múltiplas camadas de aura com padrões ondulantes
        for i in range(4):
            raio_base = tamanho * (0.2 + i * 0.1)
            pontos_aura = []
            num_pontos = 12
            
            for j in range(num_pontos):
                angulo = (j / num_pontos) * 2 * pi
                ondulacao = sin(angulo * 3 + self.fase_animacao) * 10
                raio = raio_base + ondulacao
                x = centro + cos(angulo) * raio * self.pulso_aura
                y = centro + sin(angulo) * raio * self.pulso_aura
                pontos_aura.append((x, y))
            
            # Ajusta a cor da aura baseado na camada
            cor_aura = self.cor_aura.copy()
            cor_aura.a = int(100 * (1 - i * 0.2) * self.nivel_manifestacao)
            
            # Desenha a camada da aura
            if len(pontos_aura) > 2:
                pygame.draw.polygon(
                    self.superficie_aura,
                    cor_aura,
                    pontos_aura
                )

    def _desenhar_efeitos(self):
        """
        Desenha efeitos especiais como ondulações dimensionais
        e pequenas partículas de luz que seguem o Bunian.
        """
        # Atualiza e desenha partículas de luz
        self._atualizar_particulas_luz()
        self._desenhar_particulas_luz()
        
        # Adiciona efeito de ondulação dimensional
        self._desenhar_ondulacao_dimensional()

    def _atualizar_particulas_luz(self):
        """
        Gerencia o ciclo de vida das partículas de luz que
        acompanham o movimento do Bunian.
        """
        # Adiciona novas partículas ocasionalmente
        if random.random() < 0.1:
            self.particulas_luz.append({
                'pos': Vector2(
                    random.gauss(self.superficie_efeitos.get_width() / 2, 10),
                    random.gauss(self.superficie_efeitos.get_height() / 2, 10)
                ),
                'vel': Vector2(random.uniform(-1, 1), random.uniform(-1, 1)),
                'vida': 1.0
            })
        
        # Atualiza partículas existentes
        for particula in self.particulas_luz[:]:
            particula['vida'] -= 0.02
            particula['pos'] += particula['vel']
            if particula['vida'] <= 0:
                self.particulas_luz.remove(particula)

    def _desenhar_particulas_luz(self):
        """
        Desenha as partículas de luz que acompanham o Bunian,
        criando um efeito etéreo e dimensional.
        """
        for particula in self.particulas_luz:
            cor_particula = self.cor_base.copy()
            cor_particula.a = int(255 * particula['vida'] * self.nivel_manifestacao)
            
            pygame.draw.circle(
                self.superficie_efeitos,
                cor_particula,
                particula['pos'],
                2 * particula['vida']
            )

    def atualizar(self, delta_tempo):
        """
        Atualiza o estado do Bunian, incluindo sua manifestação
        e efeitos dimensionais.
        """
        super().atualizar(delta_tempo)
        
        # Atualiza o nível de manifestação
        self._atualizar_manifestacao(delta_tempo)
        
        # Atualiza movimento etéreo
        self._atualizar_movimento_etereo(delta_tempo)

    def _atualizar_manifestacao(self, delta_tempo):
        """
        Gerencia a transição suave entre diferentes níveis
        de manifestação/visibilidade do Bunian.
        """
        self.tempo_transicao += delta_tempo
        
        # Chance de mudar o nível de manifestação
        if random.random() < 0.02:
            novo_nivel = random.uniform(
                0.2 + self.genes['invisibilidade'],
                1.0
            )
            self.nivel_manifestacao += (
                (novo_nivel - self.nivel_manifestacao) * delta_tempo
            )

    def _atualizar_movimento_etereo(self, delta_tempo):
        """
        Aplica um movimento mais fluido e etéreo,
        característico dos Bunian.
        """
        if self.estado == 'VAGANDO':
            # Movimento mais suave e gracioso
            self.direcao += (
                sin(self.fase_animacao) * 0.1 * self.genes['graciosidade']
            )
            
            # Ajusta velocidade baseado na manifestação
            self.velocidade *= 0.95  # Amortecimento suave