# ==============================================================================
# Arquivo: 2_analise_financeira.py
# Localização: /hospital_vida_plena_dashboard/pages/
# Descrição: Segunda página do painel de comando, dedicada à análise
#            financeira detalhada da operação do Hospital Vida Plena.
#            Inclui filtros interativos para uma exploração dinâmica dos dados.
# ==============================================================================
import streamlit as st
import pandas as pd
from modules.data_loader import carregar_dados
from modules.plotting import plotar_bar_chart_horizontal
from modules.style import CSS_STYLE

# --- 1. Configuração Inicial da Página ---
# Define o layout da página e o título que aparecerá na aba do navegador.
st.set_page_config(layout="wide", page_title="Análise Financeira | Hospital Vida Plena")

# Aplica o nosso estilo CSS customizado para garantir a consistência visual.
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# --- 2. Carregamento dos Dados ---
# Chama a nossa função centralizada do módulo data_loader para carregar os dados.
df = carregar_dados('data/hospital_vida_plena_dataset_500k.csv')

# --- 3. Título da Página ---
st.title("Análise Financeira Detalhada")

# --- 4. Renderização do Conteúdo ---
# Verifica se o DataFrame foi carregado com sucesso.
if df is not None:
    # --- 4.1. Filtros Interativos ---
    st.subheader("Filtros de Análise")

    # Cria um filtro multiselect para que o utilizador possa escolher um ou mais convénios.
    # `unique()` pega todos os valores únicos da coluna 'convenio'.
    # `default` define quais opções vêm pré-selecionadas.
    convenios_selecionados = st.multiselect(
        "Selecione os Convénios para Análise",
        options=df['convenio'].unique(),
        default=df['convenio'].unique()
    )

    # Aplica o filtro ao DataFrame. Apenas as linhas cujo 'convenio' está na
    # lista de `convenios_selecionados` serão mantidas.
    df_filtrado = df[df['convenio'].isin(convenios_selecionados)]

    st.markdown("---")

    # --- 4.2. KPIs Financeiros Dinâmicos ---
    # Os KPIs agora são calculados com base nos dados filtrados, tornando-os dinâmicos.
    st.subheader("KPIs Financeiros (Baseado na Seleção)")

    # Programação defensiva: verifica se o dataframe filtrado não está vazio.
    if not df_filtrado.empty:
        faturacao_filtrada = df_filtrado['valor_total_atendimento'].sum()
        ticket_medio = df_filtrado['valor_total_atendimento'].mean()
        
        col1, col2 = st.columns(2)
        col1.metric("Faturação (Seleção)", f"R$ {faturacao_filtrada:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        col2.metric("Ticket Médio (Seleção)", f"R$ {ticket_medio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

        st.markdown("---")

        # --- 4.3. Gráficos Financeiros ---
        # Prepara os dados para o gráfico: agrupa por convénio e soma a faturação.
        faturacao_por_convenio = df_filtrado.groupby('convenio')['valor_total_atendimento'].sum().sort_values().reset_index()
        
        # Chama a nossa função de plotagem reutilizável.
        fig_convenio = plotar_bar_chart_horizontal(
            faturacao_por_convenio,
            'valor_total_atendimento',
            'convenio',
            "Faturação Total por Convénio"
        )
        # Formata os valores no gráfico para o formato de moeda (R$).
        fig_convenio.update_traces(texttemplate='R$ %{x:,.2f}')
        st.plotly_chart(fig_convenio, use_container_width=True)

    else:
        # Mensagem exibida se a seleção de filtros não retornar nenhum dado.
        st.warning("Nenhum dado encontrado para os filtros selecionados. Por favor, ajuste a sua seleção.")

else:
    # Mensagem exibida caso o carregamento de dados inicial falhe.
    st.error("Não foi possível carregar os dados para exibir esta página.")
