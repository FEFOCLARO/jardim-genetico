# src/entidades/espirito_base.py

import pygame
import random
from math import sin, cos, pi
from pygame import Vector2
from ..util.constantes import CONFIGURACAO_ESPIRITOS, CORES, PARAMS_GENETICOS

class EspiritoBase(pygame.sprite.Sprite):
    """
    Classe base para todos os espíritos místicos do jardim.
    Implementa as funcionalidades comuns entre Pooka, Bunian e Huli Jing.
    """
    def __init__(self, posicao_inicial: tuple, tipo: str):
        super().__init__()
        self.tipo = tipo
        
        # Criação das superfícies em camadas para composição visual
        self._criar_superficies()
        
        # Atributos físicos e posicionamento
        self.posicao = Vector2(posicao_inicial)
        self.velocidade = Vector2(0, 0)
        self.direcao = random.uniform(0, 2 * pi)
        
        # Atributos vitais
        self.energia = CONFIGURACAO_ESPIRITOS['ENERGIA_MAXIMA']
        self.idade = 0
        self.tempo_vida = CONFIGURACAO_ESPIRITOS['TEMPO_VIDA_BASE']
        
        # Estado emocional e comportamental
        self.estado = 'VAGANDO'  # Estados: VAGANDO, DESCANSANDO, SOCIALIZANDO
        self.nivel_social = 0.0  # Aumenta ao interagir com outros espíritos
        
        # Inicialização dos genes básicos
        self.genes = self._inicializar_genes()
        
        # Animação e efeitos visuais
        self.fase_animacao = 0.0
        self.pulso_aura = 0.0
        
    def _criar_superficies(self):
        """
        Cria as camadas de superfícies para compor o visual do espírito.
        Usamos várias camadas para criar efeitos visuais complexos.
        """
        tamanho = CONFIGURACAO_ESPIRITOS['TAMANHO_BASE']
        # Superfície para o núcleo do espírito
        self.superficie_nucleo = pygame.Surface((tamanho, tamanho), 
                                              pygame.SRCALPHA)
        # Superfície maior para a aura (efeito de brilho)
        self.superficie_aura = pygame.Surface((tamanho * 2, tamanho * 2), 
                                            pygame.SRCALPHA)
        # Superfície para efeitos especiais (rastros, partículas)
        self.superficie_efeitos = pygame.Surface((tamanho * 3, tamanho * 3), 
                                               pygame.SRCALPHA)
        
        # Superfície final que combina todas as camadas
        self.image = pygame.Surface((tamanho * 3, tamanho * 3), 
                                  pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def _inicializar_genes(self):
        """
        Inicializa os genes básicos que todos os espíritos compartilham.
        Genes específicos serão adicionados nas classes filhas.
        """
        return {
            'tamanho': random.uniform(0.8, 1.2),
            'brilho': random.uniform(0.6, 1.0),
            'velocidade_base': random.uniform(0.7, 1.3),
            'sociabilidade': random.uniform(0.3, 0.9)
        }

    def atualizar(self, delta_tempo):
        """
        Atualiza o estado do espírito a cada frame.
        Gerencia movimento, energia, idade e estados.
        """
        # Atualiza idade e verifica tempo de vida
        self.idade += delta_tempo
        if self.idade >= self.tempo_vida:
            self.kill()
            return
        
        # Atualiza energia baseado no estado
        self._atualizar_energia(delta_tempo)
        
        # Atualiza movimento
        self._atualizar_movimento(delta_tempo)
        
        # Atualiza animações
        self._atualizar_animacao(delta_tempo)
        
        # Atualiza o visual
        self._atualizar_visual()

    def _atualizar_energia(self, delta_tempo):
        """Gerencia o consumo e recuperação de energia"""
        if self.estado == 'DESCANSANDO':
            self.energia = min(self.energia + CONFIGURACAO_ESPIRITOS['TAXA_RECUPERACAO'],
                             CONFIGURACAO_ESPIRITOS['ENERGIA_MAXIMA'])
        else:
            self.energia -= CONFIGURACAO_ESPIRITOS['CUSTO_MOVIMENTO'] * delta_tempo

    def _atualizar_movimento(self, delta_tempo):
        """
        Atualiza a posição e movimento do espírito.
        O movimento é suave e etéreo, adequado para criaturas místicas.
        """
        if self.estado == 'VAGANDO':
            # Movimento suave e fluido
            if random.random() < CONFIGURACAO_ESPIRITOS['CHANCE_MOVIMENTO_ALEATORIO']:
                self.direcao += random.uniform(-0.5, 0.5)
            
            # Calcula nova velocidade
            velocidade_atual = CONFIGURACAO_ESPIRITOS['VELOCIDADE_BASE'] * self.genes['velocidade_base']
            self.velocidade.x = cos(self.direcao) * velocidade_atual
            self.velocidade.y = sin(self.direcao) * velocidade_atual
            
            # Atualiza posição
            self.posicao += self.velocidade * delta_tempo
            
            # Atualiza retângulo de colisão
            self.rect.center = self.posicao

    def _atualizar_animacao(self, delta_tempo):
        """
        Atualiza os efeitos visuais e animações.
        Cria movimentos suaves e orgânicos para os elementos visuais.
        """
        # Animação do pulso da aura
        self.pulso_aura = (sin(self.idade * 2) * 0.2 + 0.8)
        
        # Fase da animação principal
        self.fase_animacao += delta_tempo
        if self.fase_animacao >= 2 * pi:
            self.fase_animacao = 0

    def _atualizar_visual(self):
        """
        Atualiza a aparência do espírito.
        Combina as diferentes camadas visuais para criar o efeito final.
        """
        # Limpa todas as superfícies
        for superficie in [self.superficie_nucleo, self.superficie_aura, 
                         self.superficie_efeitos, self.image]:
            superficie.fill((0, 0, 0, 0))
        
        # Desenha o núcleo
        self._desenhar_nucleo()
        
        # Desenha a aura
        self._desenhar_aura()
        
        # Desenha efeitos especiais
        self._desenhar_efeitos()
        
        # Combina todas as camadas
        self._combinar_camadas()

    def _desenhar_nucleo(self):
        """Desenha o núcleo central do espírito"""
        # Implementação específica será feita nas classes filhas
        pass

    def _desenhar_aura(self):
        """Desenha a aura brilhante ao redor do núcleo"""
        # Implementação específica será feita nas classes filhas
        pass

    def _desenhar_efeitos(self):
        """Desenha efeitos especiais como rastros e partículas"""
        # Implementação específica será feita nas classes filhas
        pass

    def _combinar_camadas(self):
        """Combina todas as camadas visuais na superfície final"""
        centro_x = self.image.get_width() // 2
        centro_y = self.image.get_height() // 2
        
        # Combina as camadas do mais distante para o mais próximo
        self.image.blit(self.superficie_efeitos, (0, 0))
        self.image.blit(self.superficie_aura, 
                       (centro_x - self.superficie_aura.get_width()//2,
                        centro_y - self.superficie_aura.get_height()//2))
        self.image.blit(self.superficie_nucleo,
                       (centro_x - self.superficie_nucleo.get_width()//2,
                        centro_y - self.superficie_nucleo.get_height()//2))