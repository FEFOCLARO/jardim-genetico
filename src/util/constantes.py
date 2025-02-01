# src/util/constantes.py

# Configurações da janela e desempenho
CONFIGURACAO_JANELA = {
    'LARGURA': 1280,
    'ALTURA': 720,
    'FPS': 60,
    'TITULO': "Jardim dos Espíritos Místicos"
}

# Cores base para nosso ambiente místico
CORES = {
    # Cores do ambiente
    'FUNDO_NOITE': (20, 20, 35),      # Azul muito escuro para o céu noturno
    'GRAMA_NOTURNA': (25, 35, 25),    # Verde escuro para a grama
    'NEVOA': (180, 180, 255, 30),     # Névoa azulada semitransparente
    
    # Cores base para cada tipo de espírito
    'POOKA': {
        'NUCLEO': (158, 126, 187, 255),    # Roxo místico
        'AURA': (138, 106, 167, 100), # Aura roxa suave
        'RASTRO': (148, 116, 177, 50) # Rastro mais claro
    },
    'BUNIAN': {
        'NUCLEO': (187, 210, 225, 255),    # Azul etéreo
        'AURA': (167, 190, 205, 100), # Aura azul suave
        'RASTRO': (177, 200, 215, 50) # Rastro mais claro
    },
    'HULI_JING': {
        'NUCLEO': (255, 223, 186, 255),    # Âmbar suave
        'AURA': (235, 203, 166, 100), # Aura âmbar suave
        'RASTRO': (245, 213, 176, 50) # Rastro mais claro
    }
}

# Configurações dos espíritos
CONFIGURACAO_ESPIRITOS = {
    'TAMANHO_BASE': 30,           # Tamanho base dos espíritos em pixels
    'VELOCIDADE_BASE': 3,         # Velocidade base de movimento
    'ENERGIA_MAXIMA': 100,        # Energia máxima que um espírito pode ter
    'RAIO_PERCEPCAO': 150,        # Distância que podem perceber outros espíritos
    'TEMPO_VIDA_BASE': 1000,      # Duração base da vida em frames
    
    # Configurações de comportamento
    'CHANCE_MOVIMENTO_ALEATORIO': 0.1,  # Chance de mudar direção aleatoriamente
    'CUSTO_MOVIMENTO': 0.01,            # Quanto de energia gasta ao se mover
    'TAXA_RECUPERACAO': 0.05,           # Quanto de energia recupera ao descansar
}

# Parâmetros genéticos e evolução
PARAMS_GENETICOS = {
    'POOKA': {
        'TRAVESSURA': (0.4, 0.9),      # Min e Max do nível de travessura
        'VELOCIDADE': (2.5, 4.0),       # Min e Max da velocidade
        'SOCIABILIDADE': (0.3, 0.8)     # Min e Max da tendência social
    },
    'BUNIAN': {
        'INVISIBILIDADE': (0.3, 0.7),   # Min e Max da capacidade de ficar invisível
        'VELOCIDADE': (2.0, 3.5),       # Min e Max da velocidade
        'SOCIABILIDADE': (0.5, 0.9)     # Min e Max da tendência social
    },
    'HULI_JING': {
        'MANIFESTACAO': (0.1, 0.5),     # Min e Max do nível de manifestação física
        'VELOCIDADE': (2.8, 3.8),       # Min e Max da velocidade
        'SOCIABILIDADE': (0.4, 0.7)     # Min e Max da tendência social
    },
    'MUTACAO': {
        'TAXA': 0.1,                    # Chance de mutação ao reproduzir
        'INTENSIDADE': 0.2              # Quanto um gene pode mudar na mutação
    }
}

# Configurações do ambiente
CONFIG_AMBIENTE = {
    'NUM_INICIAL_POOKA': 5,
    'NUM_INICIAL_BUNIAN': 5,
    'NUM_INICIAL_HULI_JING': 5,
    'MAX_ESPIRITOS': 30,               # Máximo de espíritos simultâneos
    'INTERVALO_COMIDA': 300,           # Frames entre surgimento de nova comida
    'MAX_COMIDA': 15,                  # Máximo de comida simultânea
    'TAMANHO_GRID': 40                 # Tamanho do grid para otimização espacial
}