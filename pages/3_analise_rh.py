# ==============================================================================
# Arquivo: 3_analise_rh.py
# Localização: /hospital_vida_plena_dashboard/pages/
# Descrição: Terceira página do painel, dedicada à análise de Recursos Humanos
#            (People Analytics) do Hospital Vida Plena.
# ==============================================================================
import streamlit as st
import pandas as pd
from modules.data_loader import carregar_dados_rh
from modules.plotting import plotar_bar_chart_horizontal, plotar_donut_chart, plotar_histograma
from modules.style import CSS_STYLE

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="People Analytics | Hospital Vida Plena")
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# --- Carregamento dos Dados ---
df_rh = carregar_dados_rh('data/people_analytics_dataset.csv')

st.title("Análise de Capital Humano (People Analytics)")

if df_rh is not None:
    # --- Filtros na Barra Lateral ---
    st.sidebar.header("Filtros de RH")
    departamento_selecionado = st.sidebar.selectbox(
        "Filtrar por Departamento",
        options=['Todos'] + list(df_rh['departamento'].unique()),
        index=0
    )

    df_filtrado = df_rh.copy()
    if departamento_selecionado != 'Todos':
        df_filtrado = df_rh[df_rh['departamento'] == departamento_selecionado]

    # --- KPIs de RH ---
    st.subheader("KPIs de Recursos Humanos")
    
    total_funcionarios = len(df_filtrado)
    funcionarios_ativos = df_filtrado[df_filtrado['data_termino'].isnull()]
    total_saidas = df_filtrado[df_filtrado['data_termino'].notnull()]
    
    # Cálculo de Turnover Anualizado (simplificado)
    turnover_rate = (len(total_saidas) / total_funcionarios) * 100 if total_funcionarios > 0 else 0
    idade_media = df_filtrado['idade'].mean()
    satisfacao_media = df_filtrado['satisfacao_trabalho'].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Funcionários (Seleção)", f"{total_funcionarios}")
    col2.metric("Taxa de Turnover (Turnover Rate)", f"{turnover_rate:.1f}%")
    col3.metric("Idade Média", f"{idade_media:.1f} anos")
    col4.metric("Satisfação Média (1-5)", f"{satisfacao_media:.2f}")

    st.markdown("---")

    # --- Análise de Turnover e Demografia ---
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        # Gráfico de Turnover por Motivo
        if not total_saidas.empty:
            turnover_por_motivo = total_saidas['motivo_saida'].value_counts().reset_index()
            fig_motivo = plotar_donut_chart(turnover_por_motivo, 'motivo_saida', 'count', "Principais Motivos de Saída")
            st.plotly_chart(fig_motivo, use_container_width=True)
        else:
            st.info("Não há dados de saída para a seleção atual.")

    with col_graf2:
        # Gráfico de Distribuição de Idade
        fig_idade = plotar_histograma(df_filtrado, 'idade', "Distribuição de Idade dos Funcionários")
        st.plotly_chart(fig_idade, use_container_width=True)
        
    st.markdown("---")

    # --- Análise de Performance e Salário ---
    st.subheader("Análise de Performance e Remuneração")
    
    col_graf3, col_graf4 = st.columns(2)
    with col_graf3:
        # Gráfico de Salário por Departamento
        salario_por_depto = df_rh.groupby('departamento')['salario_mensal'].mean().sort_values().reset_index()
        fig_salario = plotar_bar_chart_horizontal(salario_por_depto, 'salario_mensal', 'departamento', "Salário Médio por Departamento")
        fig_salario.update_traces(texttemplate='R$ %{x:,.2f}')
        st.plotly_chart(fig_salario, use_container_width=True)
        
    with col_graf4:
        # Gráfico de Distribuição da Avaliação de Desempenho
        fig_performance = plotar_histograma(df_filtrado, 'avaliacao_desempenho_anual', "Distribuição da Avaliação de Desempenho")
        st.plotly_chart(fig_performance, use_container_width=True)

else:
    st.error("Não foi possível carregar os dados de People Analytics para exibir esta página.")
