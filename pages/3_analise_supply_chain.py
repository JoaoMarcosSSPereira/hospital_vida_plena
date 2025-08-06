# ==============================================================================
# Arquivo: 3_analise_supply_chain.py
# Localização: /hospital_vida_plena_dashboard/pages/
# Descrição: Terceira página do painel, dedicada à análise da cadeia de
#            suprimentos (Supply Chain) do Hospital Vida Plena.
# ==============================================================================
import streamlit as st
import pandas as pd
from modules.data_loader import carregar_dados_supply_chain
from modules.plotting import plotar_bar_chart_horizontal, plotar_timeseries_chart
from modules.style import CSS_STYLE

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Supply Chain | Hospital Vida Plena")
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# --- Carregamento dos Dados ---
df_supply = carregar_dados_supply_chain('data/hospital_supply_chain_dataset.csv')

st.title("Análise da Cadeia de Suprimentos (Supply Chain)")

if df_supply is not None:
    # --- KPIs ---
    st.subheader("KPIs de Compras e Logística")
    custo_total = df_supply['custo_total_pedido'].sum()
    pedidos_atrasados = df_supply[df_supply['status_entrega'] == 'Atrasado'].shape[0]
    total_pedidos = len(df_supply)
    taxa_atraso = (pedidos_atrasados / total_pedidos) * 100 if total_pedidos > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Custo Total de Aquisições", f"R$ {custo_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col2.metric("Pedidos com Atraso na Entrega", f"{pedidos_atrasados}")
    col3.metric("Taxa de Atraso de Fornecedores", f"{taxa_atraso:.2f}%")

    st.markdown("---")

    # --- Gráficos ---
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        # Custo por Fornecedor
        custo_por_fornecedor = df_supply.groupby('nome_fornecedor')['custo_total_pedido'].sum().sort_values().reset_index()
        fig_fornecedor = plotar_bar_chart_horizontal(
            custo_por_fornecedor,
            'custo_total_pedido',
            'nome_fornecedor',
            "Custo Total por Fornecedor"
        )
        fig_fornecedor.update_traces(texttemplate='R$ %{x:,.2f}')
        st.plotly_chart(fig_fornecedor, use_container_width=True)

    with col_graf2:
        # Custo por Categoria de Item
        custo_por_categoria = df_supply.groupby('categoria_item')['custo_total_pedido'].sum().sort_values().reset_index()
        fig_categoria = plotar_bar_chart_horizontal(
            custo_por_categoria,
            'custo_total_pedido',
            'categoria_item',
            "Custo Total por Categoria de Item"
        )
        fig_categoria.update_traces(texttemplate='R$ %{x:,.2f}')
        st.plotly_chart(fig_categoria, use_container_width=True)
    
    st.markdown("---")
    
    # Análise Temporal de Custos
    st.subheader("Análise Temporal de Custos de Aquisição")
    custos_mensais = df_supply.set_index('data_pedido').resample('M')['custo_total_pedido'].sum().reset_index()
    fig_temporal = plotar_timeseries_chart(
        custos_mensais,
        'data_pedido',
        'custo_total_pedido',
        "Evolução Mensal dos Custos de Aquisição"
    )
    st.plotly_chart(fig_temporal, use_container_width=True)
