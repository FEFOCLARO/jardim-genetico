# src/main.py

import pygame
import sys
from pathlib import Path
from .interface.menu_inicial import MenuInicial
from .core.ambiente import AmbienteMistico
from .util.constantes import CONFIGURACAO_JANELA

class SimulacaoJardimMistico:
    """
    Classe principal que gerencia toda a simulação do jardim místico.
    Coordena a interação entre menus, ambiente e espíritos.
    """
    def __init__(self):
        # Inicialização do Pygame e configuração da janela
        pygame.init()
        pygame.display.set_caption(CONFIGURACAO_JANELA['TITULO'])
        
        # Configuração da janela principal
        self.tela = pygame.display.set_mode((
            CONFIGURACAO_JANELA['LARGURA'],
            CONFIGURACAO_JANELA['ALTURA']
        ))
        
        # Controle de tempo e FPS
        self.clock = pygame.time.Clock()
        self.delta_tempo = 0
        
        # Estados da simulação
        self.rodando = True
        self.estado_atual = "MENU"  # Estados: MENU, SIMULACAO, PAUSA
        
        # Componentes principais
        self.menu = MenuInicial()
        self.ambiente = None
        self.configuracoes = None

    def iniciar(self):
        """
        Inicia o ciclo principal da simulação.
        Primeiro mostra o menu inicial, depois gerencia o loop principal.
        """
        # Mostra o menu inicial e obtém configurações
        self.configuracoes = self.menu.mostrar()
        
        # Se o menu foi fechado sem configurações, encerra
        if self.configuracoes is None:
            return
        
        # Cria o ambiente com as configurações escolhidas
        self.ambiente = AmbienteMistico(self.configuracoes)
        self.estado_atual = "SIMULACAO"
        
        # Inicia o loop principal
        self.loop_principal()

    def loop_principal(self):
        """
        Loop principal que gerencia toda a simulação.
        Processa eventos, atualiza estados e renderiza.
        """
        while self.rodando:
            # Controle de tempo
            self.delta_tempo = self.clock.tick(CONFIGURACAO_JANELA['FPS']) / 1000.0
            
            # Processamento de eventos
            self.processar_eventos()
            
            # Atualização de estado
            self.atualizar()
            
            # Renderização
            self.renderizar()

    def processar_eventos(self):
        """
        Processa todos os eventos do Pygame.
        Gerencia input do usuário e eventos do sistema.
        """
        for evento in pygame.event.get():
            # Evento de fechar janela
            if evento.type == pygame.QUIT:
                self.rodando = False
                
            # Eventos de teclado
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.estado_atual == "SIMULACAO":
                        self.estado_atual = "PAUSA"
                    elif self.estado_atual == "PAUSA":
                        self.estado_atual = "SIMULACAO"

    def atualizar(self):
        """
        Atualiza o estado da simulação.
        Diferente comportamento baseado no estado atual.
        """
        if self.estado_atual == "SIMULACAO":
            if self.ambiente:
                self.ambiente.atualizar(self.delta_tempo)

    def renderizar(self):
        """
        Renderiza o estado atual na tela.
        Gerencia diferentes camadas de renderização.
        """
        # Limpa a tela
        self.tela.fill((20, 20, 35))  # Cor de fundo base
        
        # Renderiza baseado no estado atual
        if self.estado_atual == "SIMULACAO":
            if self.ambiente:
                self.ambiente.renderizar(self.tela)
        
        # Atualiza a tela
        pygame.display.flip()

    def encerrar(self):
        """
        Realiza a limpeza necessária antes de encerrar.
        """
        pygame.quit()
        sys.exit()

def main():
    """
    Função principal que inicia toda a simulação.
    """
    simulacao = SimulacaoJardimMistico()
    
    try:
        simulacao.iniciar()
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        simulacao.encerrar()

if __name__ == "__main__":
    main()