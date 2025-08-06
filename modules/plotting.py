# ==============================================================================
# Arquivo: plotting.py
# Localização: /hospital_vida_plena_dashboard/modules/
# Descrição: Este módulo contém todas as funções reutilizáveis para a criação
#            dos gráficos interativos do painel, utilizando a biblioteca Plotly.
#            Centralizar as funções de plotagem aqui garante consistência
#            visual e facilita a manutenção do código.
# ==============================================================================
import plotly.express as px
import plotly.graph_objects as go
from modules.style import CORES_DARK_MODE

# --- 1. Funções de Gráficos Genéricos ---

def plotar_donut_chart(df, coluna_nomes, coluna_valores, titulo):
    """
    Cria um gráfico de rosca (donut) interativo e estilizado.

    Args:
        df (pd.DataFrame): O DataFrame com os dados.
        coluna_nomes (str): O nome da coluna para as categorias (nomes das fatias).
        coluna_valores (str): O nome da coluna para os valores numéricos.
        titulo (str): O título do gráfico.

    Returns:
        plotly.graph_objects.Figure: A figura do gráfico pronta para ser exibida.
    """
    fig = px.pie(
        df,
        names=coluna_nomes,
        values=coluna_valores,
        title=titulo,
        hole=0.6,  # O "buraco" no meio que transforma a pizza em rosca
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Aplica o estilo "Dark Mode" e customizações de layout
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Fundo transparente para se adaptar ao da página
        plot_bgcolor='rgba(0,0,0,0)',
        font_color=CORES_DARK_MODE['texto_principal'],
        title_font_size=20,
        legend_title_text='Categorias'
    )
    return fig

def plotar_bar_chart_horizontal(df, x, y, titulo):
    """
    Cria um gráfico de barras horizontais interativo e estilizado.

    Args:
        df (pd.DataFrame): O DataFrame com os dados.
        x (str): O nome da coluna para o eixo X (valores).
        y (str): O nome da coluna para o eixo Y (categorias).
        titulo (str): O título do gráfico.

    Returns:
        plotly.graph_objects.Figure: A figura do gráfico pronta para ser exibida.
    """
    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation='h',
        title=titulo,
        text=x,  # Mostra os valores nas barras
        color=y, # Colore cada barra com base na sua categoria
        color_discrete_sequence=px.colors.sequential.Plasma_r
    )
    
    # Aplica o estilo "Dark Mode" e customizações de layout
    fig.update_layout(
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}, # Ordena as barras da menor para a maior
        xaxis_title="Volume",
        yaxis_title=None,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color=CORES_DARK_MODE['texto_principal']
    )
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    return fig

def plotar_gauge_chart(valor, titulo, referencia, max_range=50):
    """
    Cria um gráfico de medidor (gauge) para exibir um KPI.

    Args:
        valor (float): O valor a ser exibido no medidor.
        titulo (str): O título do gráfico.
        referencia (int): O valor de referência para o delta (mudança).
        max_range (int): O valor máximo do eixo do medidor.

    Returns:
        plotly.graph_objects.Figure: A figura do gráfico pronta para ser exibida.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=valor,
        title={'text': titulo, 'font': {'size': 20, 'color': CORES_DARK_MODE['texto_secundario']}},
        delta={'reference': referencia, 'increasing': {'color': CORES_DARK_MODE['vermelho_critico']}},
        gauge={
            'axis': {'range': [None, max_range], 'tickwidth': 1, 'tickcolor': CORES_DARK_MODE['texto_principal']},
            'bar': {'color': CORES_DARK_MODE['azul_destaque']},
            'bgcolor': CORES_DARK_MODE['fundo_secundario'],
            'borderwidth': 2,
            'bordercolor': CORES_DARK_MODE['borda'],
            'steps': [
                {'range': [0, referencia], 'color': CORES_DARK_MODE['verde_sucesso']},
                {'range': [referencia, referencia * 2], 'color': CORES_DARK_MODE['amarelo_alerta']}
            ],
            'threshold': {
                'line': {'color': CORES_DARK_MODE['vermelho_critico'], 'width': 4},
                'thickness': 0.75,
                'value': valor
            }
        }
    ))
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        font_color=CORES_DARK_MODE['texto_principal']
    )
    return fig




def plotar_timeseries_chart(df, x, y, titulo):
    """Cria um gráfico de linha (série temporal) interativo."""
    fig = px.line(
        df,
        x=x,
        y=y,
        title=titulo,
        markers=True
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Valor (R$)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color=CORES_DARK_MODE['texto_principal']
    )
    return fig



# Adicione esta função ao final do ficheiro modules/plotting.py

def plotar_histograma(df, coluna, titulo):
    """Cria um histograma interativo para analisar a distribuição de uma variável."""
    fig = px.histogram(
        df,
        x=coluna,
        title=titulo,
        color_discrete_sequence=[CORES_DARK_MODE['azul_destaque']]
    )
    fig.update_layout(
        yaxis_title="Número de Funcionários",
        xaxis_title=coluna.replace('_', ' ').title(),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color=CORES_DARK_MODE['texto_principal']
    )
    return fig
