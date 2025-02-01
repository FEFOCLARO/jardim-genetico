# src/entidades/huli_jing.py

import pygame
import random
from math import sin, cos, pi, exp
from pygame import Vector2, Color, Surface
from .espirito_base import EspiritoBase
from ..util.constantes import CORES, PARAMS_GENETICOS, CONFIGURACAO_ESPIRITOS

class HuliJing(EspiritoBase):
    """
    Huli Jing: Espírito raposa da mitologia chinesa.
    Começam como essências espirituais puras e gradualmente
    desenvolvem características vulpinas. São conhecidos por
    sua natureza sagaz e elegante.
    """
    def __init__(self, posicao_inicial: tuple):
        super().__init__(posicao_inicial, "HULI_JING")
        
        # Genes específicos do Huli Jing
        self.genes.update({
            'manifestacao_raposa': random.uniform(
                *PARAMS_GENETICOS['HULI_JING']['MANIFESTACAO']
            ),
            'sabedoria': random.uniform(0.3, 1.0),  # Afeta a forma como se move
            'elegancia': random.uniform(0.5, 1.0)   # Afeta a suavidade das animações
        })
        
        # Características visuais específicas
        self.num_caudas = 1  # Começa com uma cauda
        self.angulo_caudas = []  # Ângulos para animação das caudas
        self.pontos_caudas = []  # Pontos de controle para as caudas
        self.inicializar_caudas()
        
        # Cores específicas em tons âmbar/dourado
        self.cor_base = CORES['HULI_JING']['NUCLEO']
        self.cor_aura = CORES['HULI_JING']['AURA']
        
        # Estados específicos
        self.tempo_meditacao = 0
        self.energia_espiritual = 0
        
    def inicializar_caudas(self):
        """
        Inicializa as estruturas necessárias para renderizar
        as caudas do Huli Jing. O número de caudas aumenta
        com a sabedoria acumulada.
        """
        self.angulo_caudas = [random.uniform(0, 2*pi)]
        self.pontos_caudas = [[Vector2(0, 0) for _ in range(4)]]

    def _desenhar_nucleo(self):
        """
        Desenha o núcleo do Huli Jing, que evolui de uma forma
        espiritual pura para uma com características de raposa.
        """
        tamanho = self.superficie_nucleo.get_width()
        centro = tamanho // 2
        
        # Desenha a essência espiritual básica
        self._desenhar_essencia_basica(centro, tamanho)
        
        # Se tiver manifestação suficiente, adiciona características vulpinas
        if self.genes['manifestacao_raposa'] > 0.3:
            self._desenhar_caracteristicas_raposa(centro, tamanho)

    def _desenhar_essencia_basica(self, centro, tamanho):
        """
        Desenha a forma básica do espírito, que é mais pronunciada
        quando a manifestação raposa é menor.
        """
        # Cria um brilho central suave
        raio_base = tamanho * 0.3 * self.genes['tamanho']
        
        # Várias camadas de círculos com opacidade decrescente
        for i in range(3):
            raio = raio_base * (1 - i * 0.2)
            cor = (*self.cor_base[:3], int(255 * (1 - i * 0.3)))
            
            pygame.draw.circle(
                self.superficie_nucleo,
                cor,
                (centro, centro),
                int(raio)
            )

    def _desenhar_caracteristicas_raposa(self, centro, tamanho):
        """
        Desenha características vulpinas que se tornam mais
        pronunciadas conforme o Huli Jing evolui.
        """
        nivel_manifest = self.genes['manifestacao_raposa']
        
        # Desenha o focinho
        self._desenhar_focinho(centro, tamanho, nivel_manifest)
        
        # Desenha as orelhas
        self._desenhar_orelhas(centro, tamanho, nivel_manifest)
        
        # Desenha as caudas
        self._desenhar_caudas(centro, tamanho, nivel_manifest)

    def _desenhar_focinho(self, centro, tamanho, nivel):
        """
        Desenha o focinho da raposa, que se torna mais definido
        com maior nível de manifestação.
        """
        # Calcula pontos para o focinho triangular
        comprimento = tamanho * 0.2 * nivel
        largura = tamanho * 0.15 * nivel
        
        pontos_focinho = [
            (centro, centro + comprimento),  # Ponta
            (centro - largura, centro),      # Esquerda
            (centro + largura, centro)       # Direita
        ]
        
        # Desenha o focinho como um triângulo suave
        pygame.draw.polygon(
            self.superficie_nucleo,
            self.cor_base,
            pontos_focinho
        )

    def _desenhar_orelhas(self, centro, tamanho, nivel):
        """
        Desenha as orelhas da raposa, que se movem suavemente
        com a animação.
        """
        # Base das orelhas
        altura_orelha = tamanho * 0.3 * nivel
        largura_orelha = tamanho * 0.15 * nivel
        
        # Adiciona movimento suave às orelhas
        angulo_base = sin(self.fase_animacao) * 0.2
        
        for i in [-1, 1]:  # Orelha esquerda e direita
            # Pontos de controle para a orelha
            base = (centro + i * largura_orelha, centro)
            ponta = (
                centro + i * (largura_orelha + sin(angulo_base) * 5),
                centro - altura_orelha
            )
            
            # Desenha a orelha
            pygame.draw.line(
                self.superficie_nucleo,
                self.cor_base,
                base,
                ponta,
                int(3 * nivel)
            )

    def _desenhar_caudas(self, centro, tamanho, nivel):
        """
        Desenha as caudas do Huli Jing, que aumentam em número
        e complexidade conforme sua sabedoria cresce.
        """
        for i, (angulo, pontos) in enumerate(zip(self.angulo_caudas, self.pontos_caudas)):
            # Atualiza os pontos de controle da cauda
            self._atualizar_pontos_cauda(i, centro, tamanho, nivel)
            
            # Desenha a cauda usando curvas de Bézier
            if len(pontos) >= 4:
                pygame.draw.lines(
                    self.superficie_nucleo,
                    self.cor_base,
                    False,
                    [(p.x, p.y) for p in pontos],
                    int(2 * nivel)
                )

    def _desenhar_aura(self):
        """
        Desenha a aura do Huli Jing, que reflete sua natureza
        espiritual e sabedoria acumulada.
        """
        tamanho = self.superficie_aura.get_width()
        centro = tamanho // 2
        
        # A aura se torna mais complexa com mais caudas
        num_camadas = self.num_caudas + 2
        
        for i in range(num_camadas):
            raio = tamanho * (0.2 + i * 0.1) * self.pulso_aura
            
            # Cria uma forma mais complexa para a aura
            pontos_aura = []
            num_pontos = 12 + self.num_caudas * 4
            
            for j in range(num_pontos):
                angulo = (j / num_pontos) * 2 * pi
                distorcao = sin(angulo * self.num_caudas + self.fase_animacao)
                raio_atual = raio * (1 + distorcao * 0.1)
                
                x = centro + cos(angulo) * raio_atual
                y = centro + sin(angulo) * raio_atual
                pontos_aura.append((x, y))
            
            # Desenha a camada da aura
            if len(pontos_aura) > 2:
                cor_aura = (*self.cor_aura[:3], 
                          int(100 * (1 - i/num_camadas)))
                pygame.draw.polygon(
                    self.superficie_aura,
                    cor_aura,
                    pontos_aura
                )

    def atualizar(self, delta_tempo):
        """
        Atualiza o estado do Huli Jing, incluindo sua evolução
        e acúmulo de sabedoria.
        """
        super().atualizar(delta_tempo)
        
        # Atualiza o tempo de meditação
        if self.estado == 'DESCANSANDO':
            self.tempo_meditacao += delta_tempo
            self._verificar_evolucao()
        else:
            self.tempo_meditacao = max(0, self.tempo_meditacao - delta_tempo * 0.5)
        
        # Atualiza animações das caudas
        self._atualizar_animacao_caudas(delta_tempo)
        
        self._atualizar_visual()

    def _verificar_evolucao(self):
        """
        Verifica se o Huli Jing está pronto para evoluir e
        ganhar uma nova cauda.
        """
        if (self.tempo_meditacao > 100 and 
            self.num_caudas < 9 and 
            random.random() < self.genes['sabedoria'] * 0.1):
            
            self.num_caudas += 1
            self.angulo_caudas.append(random.uniform(0, 2*pi))
            self.pontos_caudas.append([Vector2(0, 0) for _ in range(4)])
            self.tempo_meditacao = 0
            
            # Aumenta levemente a sabedoria
            self.genes['sabedoria'] = min(1.0, self.genes['sabedoria'] * 1.1)

    def _atualizar_animacao_caudas(self, delta_tempo):
        """
        Atualiza a animação suave das caudas do Huli Jing.
        """
        for i, angulo in enumerate(self.angulo_caudas):
            # Cada cauda se move de forma ligeiramente diferente
            self.angulo_caudas[i] += (
                sin(self.fase_animacao + i) * 
                0.02 * self.genes['elegancia']
            )