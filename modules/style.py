# ==============================================================================
# Arquivo: style.py
# Localização: /hospital_vida_plena_dashboard/modules/
# Descrição: Este módulo centraliza todas as configurações de estilo visual
#            da aplicação, incluindo a paleta de cores e o código CSS.
#            Importar variáveis deste ficheiro garante uma identidade visual
#            consistente em todas as páginas do painel.
# ==============================================================================

# --- 1. Definição da Paleta de Cores ---
# Escolhemos uma paleta "Dark Mode" focada em UX, com alto contraste para
# garantir a máxima legibilidade dos dados e textos.
CORES_DARK_MODE = {
    "texto_principal": "#E0E0E0",      # Texto principal (cinza claro)
    "texto_secundario": "#B0BEC5",   # Tom suave para subtítulos e textos de apoio
    "fundo_principal": "#121212",       # Fundo principal (preto profundo)
    "fundo_secundario": "#1E1E2F",    # Fundo para cards e elementos destacados (azul escuro)
    "borda": "#4A5568",              # Borda sutil para separar elementos
    "azul_destaque": "#00BCD4",     # Azul ciano vibrante para títulos e interações
    "verde_sucesso": "#4CAF50",     # Verde para indicadores positivos
    "verde_claro": "#81C784",         # Verde claro para complementar paletas de gráficos
    "amarelo_alerta": "#FDD835",     # Amarelo para pontos de atenção
    "vermelho_critico": "#FC8181",     # Vermelho/rosa claro para alertas críticos
    "laranja_dados": "#FF9800"      # Laranja quente para visualizações de dados
}

# --- 2. Definição do Bloco de CSS ---
# Utilizamos uma f-string do Python para criar um bloco de CSS que será
# injetado diretamente na aplicação Streamlit. Isto permite-nos customizar
# elementos que não são diretamente acessíveis pela API do Streamlit.
CSS_STYLE = f"""
<style>
    /* Importa uma fonte profissional (Roboto) do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* Define a fonte padrão e a cor do texto para toda a aplicação */
    html, body, [class*="st-"] {{
        font-family: 'Roboto', sans-serif;
        color: {CORES_DARK_MODE['texto_principal']};
    }}

    /* Define a cor de fundo principal da aplicação */
    .stApp {{
        background-color: {CORES_DARK_MODE['fundo_principal']};
    }}

    /* Estiliza os cards de métricas (KPIs) para um visual moderno */
    [data-testid="stMetric"] {{
        background-color: {CORES_DARK_MODE['fundo_secundario']};
        border: 1px solid {CORES_DARK_MODE['borda']};
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: all 0.3s ease-in-out; /* Efeito suave ao passar o rato */
    }}
    [data-testid="stMetric"]:hover {{
        box-shadow: 0 10px 15px rgba(0,0,0,0.3);
        transform: translateY(-5px); /* Efeito de "flutuar" */
    }}

    /* Customiza as cores dos textos dentro dos cards de métricas */
    [data-testid="stMetricLabel"] {{
        color: {CORES_DARK_MODE['texto_secundario']};
        font-size: 1.1rem;
    }}
    [data-testid="stMetricValue"] {{
        color: {CORES_DARK_MODE['texto_principal']};
        font-size: 2.5rem;
        font-weight: 700;
    }}

    /* Estiliza os títulos principais (h1, h2, h3) */
    h1 {{
        color: {CORES_DARK_MODE['azul_destaque']};
        font-weight: 700;
        text-align: center;
    }}
    h2 {{
        color: {CORES_DARK_MODE['texto_secundario']};
        text-align: center;
    }}
    h3 {{
        color: {CORES_DARK_MODE['azul_destaque']};
        border-bottom: 2px solid {CORES_DARK_MODE['borda']};
        padding-bottom: 5px;
    }}
</style>
"""
