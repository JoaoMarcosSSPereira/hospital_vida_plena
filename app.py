# ==============================================================================
# Arquivo: app.py
# Localização: /hospital_vida_plena_dashboard/
# Descrição: Página de entrada (landing page) da aplicação. Este é o primeiro
#            script que o Streamlit executa. A sua função é apresentar o
#            projeto e orientar o utilizador para as páginas de análise.
# ==============================================================================
import streamlit as st
from modules.style import CSS_STYLE

# --- 1. Configuração da Página ---
# Define o layout, o título que aparece na aba do navegador e o estado inicial
# da barra lateral. `set_page_config` deve ser o primeiro comando Streamlit no script.
st.set_page_config(
    layout="wide",
    page_title="JM ANALYTICS | Hospital Vida Plena",
    initial_sidebar_state="expanded"
)

# --- 2. Aplicação do Estilo Visual ---
# Importa a string CSS do nosso módulo de estilo e aplica-a à página.
# Isto garante uma identidade visual consistente em toda a aplicação.
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# --- 3. Conteúdo da Página Principal ---
# Esta secção constrói o conteúdo visual da página de entrada.

# Título principal da aplicação.
st.title("Painel de Comando Estratégico - Hospital Vida Plena")

# Imagem de cabeçalho para impacto visual.
# CORREÇÃO: O parâmetro 'use_column_width' foi substituído por 'use_container_width'
# para seguir as boas práticas atuais do Streamlit e eliminar o DeprecationWarning.
st.image("https://placehold.co/1200x400/1E1E2F/00BCD4?text=Hospital+Vida+Plena", use_container_width=True)

# Cabeçalho de boas-vindas e texto introdutório.
st.header("Bem-vindo ao Centro de Inteligência de Dados da JM ANALYTICS")

# O `st.markdown` com três aspas (""") permite escrever blocos de texto longos.
# Usamos `st.info` para criar uma caixa de destaque visualmente apelativa.
st.info("""
    Este painel é a nossa ferramenta central para a análise de performance do Hospital Vida Plena.
    Utilize o menu de navegação à esquerda para explorar as diferentes áreas de análise:

    - **Visão Geral:** KPIs e métricas de alto nível sobre a operação do hospital.
    - **Análise Financeira:** Detalhes sobre faturação, custos e performance por convénio.

    Este projeto representa a nossa capacidade de transformar dados brutos em insights estratégicos e acionáveis.
""")

# --- 4. Instruções e Rodapé ---
st.markdown("---")
st.subheader("Como Navegar")
st.markdown("Para começar, selecione uma das páginas de análise no menu da barra lateral à esquerda.")


