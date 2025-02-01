import pygame
import random
from pygame import Vector2
from ..entidades.pooka import Pooka
from ..entidades.bunian import Bunian
from ..entidades.huli import HuliJing
from ..util.constantes import CONFIG_AMBIENTE, CONFIGURACAO_JANELA, CORES

class AmbienteMistico:
    """
    Ambiente principal onde os espíritos místicos existem e interagem.
    Gerencia a física, colisões e renderização do mundo.
    """
    def __init__(self, configuracoes):
        self.espiritos = pygame.sprite.Group()
        self.configuracoes = configuracoes
        self.grid = self._criar_grid()
        self.tempo_simulacao = 0
        self.geracao_atual = 0
        self.inicializar_espiritos()
        
    def _criar_grid(self):
        """
        Cria uma grid que divide o espaço em células. Isso nos ajuda a:
        1. Otimizar detecção de colisões.
        2. Organizar recursos no ambiente
        3. Controlar densidade de população em diferentes áreas
        """
        linhas = CONFIGURACAO_JANELA['ALTURA'] // CONFIG_AMBIENTE['TAMANHO_GRID']
        colunas = CONFIGURACAO_JANELA['LARGURA'] // CONFIG_AMBIENTE['TAMANHO_GRID']
        return [[[] for _ in range(colunas)] for _ in range(linhas)]
        
    def inicializar_espiritos(self):
        """
        Cria os espíritos iniciais baseado nas configurações
        Cada espírito começa em uma posição aleatória mas com movimento limitado.
        """
        largura = CONFIGURACAO_JANELA['LARGURA']
        altura = CONFIGURACAO_JANELA['ALTURA']
        

        
        # Cria Pookas
        for _ in range(self.configuracoes['num_pooka']):
                pos = self._encontrar_posicao_valida()
                espirito = Pooka(pos)
                espirito.velocidade = Vector2(0, 0)
                self.espiritos.add(espirito)
                self._adicionar_ao_grid(espirito)
            
        # Cria Bunians
        for _ in range(self.configuracoes['num_bunian']):
                pos = self._encontrar_posicao_valida()
                espirito = Bunian(pos)
                espirito.velocidade = Vector2(0, 0)
                self.espiritos.add(espirito)
                self._adicionar_ao_grid(espirito)
            
        # Cria Huli Jings
        for _ in range(self.configuracoes['num_huli_jing']):
                pos = self._encontrar_posicao_valida()
                espirito = HuliJing(pos)
                espirito.velocidade = Vector2(0, 0)
                self.espiritos.add(espirito)
                self._adicionar_ao_grid(espirito)
    
    # Verifica posição válida pra espírito, evita sobreposição
    def _encontrar_posicao_valida(self):
        """
        Encontra uma posição inicial válida para um espírito,
        evitando sobreposições e mantendo distância mínima entre eles.
        """
        while True:
            x = random.randint(50, CONFIGURACAO_JANELA['LARGURA'] - 50)
            y = random.randint(50, CONFIGURACAO_JANELA['ALTURA'] - 50)
            pos = (x, y)
            
            # Verifica se está longe o suficiente de outros espíritos
            if self._posicao_valida(pos):
                return pos
    
    def _posicao_valida(self, pos):
        """Verifica se uma posição está adequadamente distante de outros espíritos"""
        distancia_minima = CONFIG_AMBIENTE['TAMANHO_GRID']
        for espirito in self.espiritos:
            dx = pos[0] - espirito.posicao.x
            dy = pos[1] - espirito.posicao.y
            if (dx * dx + dy * dy) < distancia_minima * distancia_minima:
                return False
        return True

    # Métodos de Gerenciamento de Grid
    
    def _adicionar_ao_grid(self, espirito):
        """Adiciona um espírito ao grid na posição correspondente"""
        x = int(espirito.posicao.x // CONFIG_AMBIENTE['TAMANHO_GRID'])
        y = int(espirito.posicao.y // CONFIG_AMBIENTE['TAMANHO_GRID'])
        x = max(0, min(x, len(self.grid[0]) - 1))
        y = max(0, min(y, len(self.grid) - 1))
        self.grid[y][x].append(espirito)
        espirito.grid_pos = (x, y)

    def _remover_do_grid(self, espirito):
        """Remove um espírito de sua célula atual no grid"""
        if hasattr(espirito, 'grid_pos'):
            x, y = espirito.grid_pos
            if espirito in self.grid[y][x]:
                self.grid[y][x].remove(espirito)

    def _atualizar_posicao_grid(self, espirito):
        """Atualiza a posição do espírito no grid quando ele se move"""
        novo_x = int(espirito.posicao.x // CONFIG_AMBIENTE['TAMANHO_GRID'])
        novo_y = int(espirito.posicao.y // CONFIG_AMBIENTE['TAMANHO_GRID'])
        novo_x = max(0, min(novo_x, len(self.grid[0]) - 1))
        novo_y = max(0, min(novo_y, len(self.grid) - 1))
        
        if not hasattr(espirito, 'grid_pos') or (novo_x, novo_y) != espirito.grid_pos:
            self._remover_do_grid(espirito)
            self.grid[novo_y][novo_x].append(espirito)
            espirito.grid_pos = (novo_x, novo_y)

    def _obter_vizinhos(self, espirito):
        """Retorna uma lista de espíritos vizinhos"""
        vizinhos = []
        x, y = espirito.grid_pos
        raio = 1
        
        for dy in range(-raio, raio + 1):
            for dx in range(-raio, raio + 1):
                nova_y = y + dy
                nova_x = x + dx
                if (0 <= nova_y < len(self.grid) and 
                    0 <= nova_x < len(self.grid[0])):
                    for outro in self.grid[nova_y][nova_x]:
                        if outro != espirito:
                            vizinhos.append(outro)
        return vizinhos
    
    # Métodos de atualização
    
    def atualizar(self, delta_tempo):
        """Atualiza o estado da simulação"""
        self.tempo_simulacao += delta_tempo
        
        for espirito in self.espiritos:
            self._atualizar_posicao_grid(espirito)
            self._processar_comportamento(espirito, delta_tempo)
            espirito.atualizar(delta_tempo)

    def _processar_comportamento(self, espirito, delta_tempo):
        """Processa o comportamento de um espírito"""
        vizinhos = self._obter_vizinhos(espirito)
        self._aplicar_regras_movimento(espirito, vizinhos)
        
        if espirito.velocidade.length() > 0:
            espirito.velocidade = espirito.velocidade.normalize() * 2

    def _aplicar_regras_movimento(self, espirito, vizinhos):
        """Aplica as regras básicas de movimento"""
        if not vizinhos:
            return
            
        separacao = Vector2(0, 0)
        for vizinho in vizinhos:
            dist = espirito.posicao.distance_to(vizinho.posicao)
            if dist < CONFIG_AMBIENTE['TAMANHO_GRID']:
                separacao += (espirito.posicao - vizinho.posicao).normalize()
        
        if separacao.length() > 0:
            espirito.velocidade += separacao.normalize()

        
        # Limita a velocidade
        if espirito.velocidade.length() > 0:
            espirito.velocidade = espirito.velocidade.normalize() * 2

    # I. Desenha o fundo base
    
    def _desenhar_nevoa(self, superficie, posicao, raio):
        """
        Desenha um efeito de névoa suave usando círculos com alpha.
        
        Args:
            superficie: A superfície pygame onde a névoa será desenhada
            posicao: Tupla (x, y) indicando o centro da névoa
            raio: Tamanho do raio da névoa em pixels
        """
        # Criamos uma superfície temporária do tamanho da névoa
        nevoa = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
        
        # Extraímos apenas os componentes RGB da cor da névoa
        cor_base = CORES['NEVOA'][:3]
        
        # Criamos círculos concêntricos do maior para o menor
        for r in range(raio, 0, -2):
            # Calculamos a opacidade baseada na distância do centro
            opacidade = int(25 * (r / raio))
            
            # Criamos a cor atual combinando RGB com a opacidade
            cor_atual = (*cor_base, opacidade)
            
            # Desenhamos o círculo na superfície temporária
            pygame.draw.circle(
                nevoa,           # Superfície onde desenhar
                cor_atual,       # Cor com transparência
                (raio, raio),   # Centro do círculo
                r               # Raio do círculo atual
            )
        
        # Finalmente, desenhamos a névoa na superfície principal
        superficie.blit(nevoa, (posicao[0] - raio, posicao[1] - raio))
    
    def _interpolar_cor(self, cor1, cor2, fator):
        """
        Cria uma transição suave entre duas cores
        """
        return tuple(
        int(c1 + (c2 - c1) * fator)
        for c1, c2 in zip(cor1, cor2)
    )
    

        

        