# src/interface/menu_inicial.py

import pygame
import random
from pygame import Vector2
import pygame.gfxdraw
from ..util.constantes import CORES, CONFIGURACAO_JANELA

class MenuInicial:
    """
    Menu inicial do Jardim dos Espíritos Místicos.
    Apresenta uma introdução atmosférica ao mundo místico
    e permite ao usuário configurar a simulação inicial.
    """
    def __init__(self):
        # Inicialização básica
        self.tela = pygame.display.set_mode((
            CONFIGURACAO_JANELA['LARGURA'],
            CONFIGURACAO_JANELA['ALTURA']
        ))
        
        # Preparação das fontes para diferentes elementos
        self.fonte_titulo = pygame.font.Font(None, 72)
        self.fonte_subtitulo = pygame.font.Font(None, 36)
        self.fonte_texto = pygame.font.Font(None, 28)
        
        # Estados e animações
        self.tempo = 0
        self.alpha_titulo = 0  # Para fade in do título
        self.particulas = []   # Para efeitos visuais
        
        # Configurações iniciais da simulação
        self.configuracoes = {
            'num_pooka': 3,
            'num_bunian': 3,
            'num_huli_jing': 3
        }
        
        # Elementos da interface
        self.botoes = self._criar_botoes()
        
    def _criar_botoes(self):
        """
        Cria os elementos interativos da interface.
        Retorna um dicionário com todos os botões e suas propriedades.
        """
        largura_botao = 200
        altura_botao = 40
        espacamento = 20
        
        centro_x = CONFIGURACAO_JANELA['LARGURA'] // 2
        base_y = CONFIGURACAO_JANELA['ALTURA'] * 0.6
        
        return {
            'pooka': {
                'rect': pygame.Rect(
                    centro_x - largura_botao - espacamento - 100,
                    base_y,
                    largura_botao,
                    altura_botao
                ),
                'texto': 'Pooka: {}'
            },
            'bunian': {
                'rect': pygame.Rect(
                    centro_x - largura_botao//2,
                    base_y,
                    largura_botao,
                    altura_botao
                ),
                'texto': 'Bunian: {}'
            },
            'huli_jing': {
                'rect': pygame.Rect(
                    centro_x + espacamento + 100,
                    base_y,
                    largura_botao,
                    altura_botao
                ),
                'texto': 'Huli Jing: {}'
            },
            'iniciar': {
                'rect': pygame.Rect(
                    centro_x - largura_botao//2,
                    base_y + altura_botao + espacamento * 2,
                    largura_botao,
                    altura_botao
                ),
                'texto': 'Iniciar Jornada'
            }
        }

    def _atualizar_particulas(self, delta_tempo):
        """
        Atualiza o sistema de partículas que cria um efeito
        místico no fundo do menu.
        """
        # Adiciona novas partículas ocasionalmente
        if random.random() < 0.1:
            self.particulas.append({
                'pos': Vector2(
                    random.randint(0, CONFIGURACAO_JANELA['LARGURA']),
                    CONFIGURACAO_JANELA['ALTURA'] + 10
                ),
                'vel': Vector2(
                    random.uniform(-0.5, 0.5),
                    random.uniform(-2, -1)
                ),
                'vida': 1.0,
                'cor': random.choice([
                    CORES['POOKA']['NUCLEO'],
                    CORES['BUNIAN']['NUCLEO'],
                    CORES['HULI_JING']['NUCLEO']
                ])
            })
        
        # Atualiza partículas existentes
        for particula in self.particulas[:]:
            particula['pos'] += particula['vel']
            particula['vida'] -= 0.005
            if particula['vida'] <= 0:
                self.particulas.remove(particula)

    def _desenhar_fundo(self):
        """
        Desenha o fundo atmosférico com gradiente e partículas.
        """
        # Gradiente de fundo
        for y in range(CONFIGURACAO_JANELA['ALTURA']):
            cor = self._interpolar_cor(
                (20, 20, 35),  # Cor do topo
                (35, 25, 45),  # Cor da base
                y / CONFIGURACAO_JANELA['ALTURA']
            )
            pygame.draw.line(
                self.tela,
                cor,
                (0, y),
                (CONFIGURACAO_JANELA['LARGURA'], y)
            )
        
        # Desenha partículas
        for particula in self.particulas:
            cor = list(particula['cor'])
            cor[3] = int(255 * particula['vida'])
            pygame.gfxdraw.filled_circle(
                self.tela,
                int(particula['pos'].x),
                int(particula['pos'].y),
                2,
                cor
            )

    def _desenhar_interface(self):
        """
        Desenha todos os elementos da interface do menu.
        """
        # Desenha título com fade in
        titulo = self.fonte_titulo.render(
            "Jardim dos Espíritos Místicos",
            True,
            (255, 255, 255)
        )
        titulo.set_alpha(self.alpha_titulo)
        titulo_rect = titulo.get_rect(
            center=(
                CONFIGURACAO_JANELA['LARGURA']//2,
                CONFIGURACAO_JANELA['ALTURA']//4
            )
        )
        self.tela.blit(titulo, titulo_rect)
        
        # Desenha botões
        for nome, botao in self.botoes.items():
            # Verifica hover
            hover = botao['rect'].collidepoint(pygame.mouse.get_pos())
            
            # Desenha fundo do botão
            cor_botao = (60, 50, 80) if hover else (45, 35, 65)
            pygame.draw.rect(self.tela, cor_botao, botao['rect'])
            
            # Desenha texto do botão
            if nome in ['pooka', 'bunian', 'huli_jing']:
                texto = botao['texto'].format(
                    self.configuracoes[f'num_{nome}']
                )
            else:
                texto = botao['texto']
                
            texto_surface = self.fonte_texto.render(
                texto,
                True,
                (255, 255, 255)
            )
            texto_rect = texto_surface.get_rect(
                center=botao['rect'].center
            )
            self.tela.blit(texto_surface, texto_rect)

    def mostrar(self):
        """
        Exibe o menu inicial e processa interações.
        Retorna as configurações escolhidas quando o usuário inicia.
        """
        clock = pygame.time.Clock()
        executando = True
        
        while executando:
            delta_tempo = clock.tick(60) / 1000.0
            self.tempo += delta_tempo
            
            # Fade in do título
            if self.alpha_titulo < 255:
                self.alpha_titulo = min(255, self.alpha_titulo + 2)
            
            # Atualiza partículas
            self._atualizar_particulas(delta_tempo)
            
            # Processa eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                    
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # Processa cliques nos botões
                    for nome, botao in self.botoes.items():
                        if botao['rect'].collidepoint(evento.pos):
                            if nome == 'iniciar':
                                return self.configuracoes
                            elif nome in self.configuracoes:
                                # Ajusta número de espíritos (com limites)
                                if evento.button == 1:  # Clique esquerdo
                                    self.configuracoes[f'num_{nome}'] = min(
                                        5,
                                        self.configuracoes[f'num_{nome}'] + 1
                                    )
                                elif evento.button == 3:  # Clique direito
                                    self.configuracoes[f'num_{nome}'] = max(
                                        1,
                                        self.configuracoes[f'num_{nome}'] - 1
                                    )
            
            # Desenha tudo
            self._desenhar_fundo()
            self._desenhar_interface()
            
            pygame.display.flip()