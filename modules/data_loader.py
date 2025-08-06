# ==============================================================================
# Arquivo: data_loader.py
# Localização: /hospital_vida_plena_dashboard/modules/
# Descrição: Este módulo é responsável por todas as operações de carregamento,
#            limpeza e pré-processamento dos dados do Hospital Vida Plena.
#            A sua função é fornecer um DataFrame limpo e pronto para análise
#            para as outras partes da aplicação.
# ==============================================================================
import streamlit as st
import pandas as pd

# --- 1. Função de Carregamento de Dados ---
# O decorador `@st.cache_data` é uma ferramenta poderosa do Streamlit.
# Ele "memoriza" o resultado da função. Se a função for chamada novamente
# com os mesmos argumentos, o Streamlit retorna o resultado guardado em cache
# em vez de executar a função novamente, o que torna a aplicação muito mais rápida.
# `ttl=3600` significa que o cache expira após 3600 segundos (1 hora).
@st.cache_data(ttl=3600)
def carregar_dados(caminho_arquivo):
    """
    Carrega os dados do hospital a partir de um ficheiro CSV especificado.

    Esta função realiza a leitura do ficheiro e aplica otimizações e
    conversões de tipo de dados essenciais para a análise.

    Args:
        caminho_arquivo (str): O caminho para o ficheiro CSV.

    Returns:
        pandas.DataFrame: Um DataFrame contendo os dados do hospital,
                          ou None se o ficheiro não for encontrado.
    """
    try:
        # Tenta ler o ficheiro CSV. Os parâmetros são importantes:
        # - sep=';': Indica que as colunas são separadas por ponto e vírgula.
        # - decimal=',': Indica que o separador decimal é a vírgula.
        # - parse_dates=[...]: Converte automaticamente as colunas de data
        #                      para o formato datetime do pandas, que é
        #                      essencial para filtros e análises temporais.
        df = pd.read_csv(
            caminho_arquivo,
            sep=';',
            decimal=',',
            parse_dates=['data_nascimento_paciente', 'data_atendimento']
        )

        # --- 2. Otimização de Memória ---
        # Para datasets grandes, é uma boa prática converter colunas de texto
        # com poucos valores únicos (como 'status' ou 'tipo') para o tipo
        # 'category'. Isto pode reduzir drasticamente o uso de memória.
        for col in ['tipo_atendimento', 'setor_atendimento', 'convenio', 'status_pagamento']:
            df[col] = df[col].astype('category')
            
        return df

    except FileNotFoundError:
        # --- 3. Tratamento de Erros ---
        # Se o ficheiro CSV não for encontrado no caminho especificado,
        # a aplicação não irá quebrar. Em vez disso, exibirá uma mensagem
        # de erro amigável para o utilizador, o que é uma boa prática de UX.
        st.error(f"Erro Crítico: O ficheiro de dados não foi encontrado em '{caminho_arquivo}'.")
        st.warning("Por favor, certifique-se de que o dataset 'hospital_vida_plena_dataset_500k.csv' foi gerado e está localizado na pasta '/data/'.")
        return None

@st.cache_data(ttl=3600)
def carregar_dados_supply_chain(caminho_arquivo):
    """
    Carrega os dados de supply chain a partir de um ficheiro CSV.
    """
    try:
        df = pd.read_csv(
            caminho_arquivo,
            sep=';',
            decimal=',',
            parse_dates=['data_pedido', 'data_entrega_prevista', 'data_entrega_real']
        )
        for col in ['categoria_item', 'nome_fornecedor', 'status_entrega']:
            df[col] = df[col].astype('category')
        return df
    except FileNotFoundError:
        st.error(f"Erro: O ficheiro de supply chain não foi encontrado em '{caminho_arquivo}'.")
        return None
    
    # Adicione esta função ao final do ficheiro modules/data_loader.py

@st.cache_data(ttl=3600)
def carregar_dados_rh(caminho_arquivo):
    """
    Carrega os dados de People Analytics a partir de um ficheiro CSV.
    """
    try:
        df = pd.read_csv(
            caminho_arquivo,
            sep=';',
            decimal=',',
            parse_dates=['data_contratacao', 'data_termino']
        )
        # Otimização de memória
        for col in ['genero', 'departamento', 'cargo', 'nivel_senioridade', 'motivo_saida', 'promovido_ultimo_ano']:
            df[col] = df[col].astype('category')
        return df
    except FileNotFoundError:
        st.error(f"Erro: O ficheiro de People Analytics não foi encontrado em '{caminho_arquivo}'.")
        return None