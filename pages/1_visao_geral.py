# ==============================================================================
# Arquivo: 1_visao_geral.py
# Localização: /hospital_vida_plena_dashboard/pages/
# Descrição: Primeira página do painel de comando, focada em apresentar
#            os KPIs (Indicadores-Chave de Performance) e uma visão geral
#            da operação do Hospital Vida Plena.
# ==============================================================================
import streamlit as st
import pandas as pd
from modules.data_loader import carregar_dados
from modules.plotting import plotar_donut_chart
from modules.style import CSS_STYLE

# --- 1. Configuração Inicial da Página ---
# Define o layout da página e o título que aparecerá na aba do navegador.
st.set_page_config(layout="wide", page_title="Visão Geral | Hospital Vida Plena")

# Aplica o nosso estilo CSS customizado para garantir a consistência visual.
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# --- 2. Carregamento dos Dados ---
# Chama a nossa função centralizada do módulo data_loader para carregar os dados.
# O resultado fica guardado em cache para alta performance.
df = carregar_dados('data/hospital_vida_plena_dataset_500k.csv')

# --- 3. Título da Página ---
st.title("Visão Geral da Operação")

# --- 4. Renderização do Conteúdo ---
# BOA PRÁTICA: Verifica se o DataFrame foi carregado com sucesso antes de
# tentar renderizar qualquer componente que dependa dele. Isto evita erros
# caso o ficheiro de dados não seja encontrado.
if df is not None:
    # --- 4.1. Cálculo e Exibição dos KPIs ---
    st.subheader("Indicadores-Chave de Performance (KPIs)")

    # Realiza os cálculos necessários para os KPIs.
    total_atendimentos = len(df)
    total_pacientes_unicos = df['paciente_id'].nunique()
    faturacao_total = df['valor_total_atendimento'].sum()
    ticket_medio = df['valor_total_atendimento'].mean()

    # Utiliza st.columns para criar uma grelha e organizar os KPIs em cartões.
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Atendimentos", f"{total_atendimentos:,}".replace(',', '.'))
    col2.metric("Pacientes Únicos Atendidos", f"{total_pacientes_unicos:,}".replace(',', '.'))
    col3.metric("Faturação Total", f"R$ {faturacao_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col4.metric("Ticket Médio por Atendimento", f"R$ {ticket_medio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

    st.markdown("---") # Adiciona uma linha divisória

    # --- 4.2. Gráficos de Distribuição ---
    # Cria uma nova grelha para os gráficos.
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        # Prepara os dados para o gráfico: conta o número de atendimentos por setor.
        atendimentos_por_setor = df['setor_atendimento'].value_counts().reset_index()
        # Chama a nossa função de plotagem reutilizável do módulo plotting.
        fig_setor = plotar_donut_chart(atendimentos_por_setor, 'setor_atendimento', 'count', "Atendimentos por Setor")
        # Exibe o gráfico na aplicação.
        st.plotly_chart(fig_setor, use_container_width=True)

    with col_graf2:
        # Prepara os dados para o gráfico: conta o número de atendimentos por tipo.
        atendimentos_por_tipo = df['tipo_atendimento'].value_counts().reset_index()
        # Chama a nossa função de plotagem reutilizável.
        fig_tipo = plotar_donut_chart(atendimentos_por_tipo, 'tipo_atendimento', 'count', "Distribuição por Tipo de Atendimento")
        # Exibe o gráfico na aplicação.
        st.plotly_chart(fig_tipo, use_container_width=True)

else:
    # Mensagem exibida caso o carregamento de dados falhe.
    st.error("Não foi possível carregar os dados para exibir esta página.")

