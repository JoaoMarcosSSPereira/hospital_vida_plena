import pandas as pd
import numpy as np
from faker import Faker
from tqdm import tqdm
import random
from datetime import datetime, timedelta
import os

# ==============================================================================
# JM ANALYTICS - PROJETO HOSPITAL VIDA PLENA (MEGA PROJETO)
# Arquivo: data_generator.py
# Localização: /hospital_vida_plena_dashboard/scripts/ (Recomendado)
# Descrição: Script para geração de dados sintéticos em larga escala.
# OBJETIVO: Criar um dataset robusto com 500 mil linhas, utilizando
#           uma abordagem de chunking para garantir a eficiência de memória.
# ==============================================================================

print("Iniciando a simulação do Hospital Vida Plena...")
print("A geração de 500 mil linhas é um processo rápido.")

# --- 1. CONFIGURAÇÃO DA SIMULAÇÃO ---
fake = Faker('pt_BR')
TOTAL_REGISTOS = 500_000
TAMANHO_LOTE = 100_000  # Gerar 100 mil linhas por vez
NUM_LOTES = TOTAL_REGISTOS // TAMANHO_LOTE
# Garante que o ficheiro é guardado na pasta correta
OUTPUT_DIR = 'data'
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, 'hospital_vida_plena_dataset_500k.csv')

DATA_INICIAL = datetime(2015, 1, 1)
DATA_FINAL = datetime(2024, 12, 31)

# --- 2. DEFINIÇÃO DAS LISTAS DE DIMENSÕES (Simulando tabelas de apoio) ---
SETORES_HOSPITALARES = ['Cardiologia', 'Ortopedia', 'Neurologia', 'Pediatria', 'Oncologia', 'Clínica Geral', 'Pronto-Socorro', 'UTI']
TIPOS_ATENDIMENTO = ['Ambulatorial', 'Internação', 'Emergência', 'Exame']
CONVENIOS = ['SulAmérica', 'Bradesco Saúde', 'Amil', 'Unimed', 'CASSI', 'SUS', 'Particular']
STATUS_PAGAMENTO = ['Pago', 'Pendente', 'Atrasado', 'Cancelado']

# --- 3. GERAÇÃO DE DADOS BASE (Pacientes) ---
# Geramos um pool de pacientes para a simulação.
print("\nPasso 1: Gerando um pool de pacientes para a simulação...")
num_pacientes = 100_000 # Pool de 100 mil pacientes únicos
pacientes = [{'paciente_id': 1000000 + i, 'nome_paciente': fake.name(), 'data_nascimento': fake.date_of_birth(minimum_age=0, maximum_age=95)} for i in tqdm(range(num_pacientes))]

# --- 4. FUNÇÃO PARA GERAR UM LOTE DE DADOS ---
# Esta função encapsula a lógica de criação de um único lote (chunk).
def gerar_lote(numero_lote, total_lotes, tamanho_do_lote):
    """Gera um DataFrame do pandas com um lote de dados sintéticos."""
    print(f"\nGerando Lote {numero_lote + 1}/{total_lotes}...")
    registos_lote = []
    for i in tqdm(range(tamanho_do_lote)):
        # --- Seleciona um paciente aleatório do pool ---
        paciente = random.choice(pacientes)
        
        # --- Simula dados do atendimento ---
        tipo_atendimento = random.choices(TIPOS_ATENDIMENTO, weights=[0.4, 0.2, 0.3, 0.1], k=1)[0]
        setor = random.choice(SETORES_HOSPITALARES)
        data_atendimento = fake.date_time_between(start_date=DATA_INICIAL, end_date=DATA_FINAL)
        
        dias_internacao = 0
        if tipo_atendimento == 'Internação':
            dias_internacao = random.randint(1, 30)
        
        # --- Simula dados financeiros ---
        convenio = random.choice(CONVENIOS)
        valor_base = random.uniform(150, 5000)
        fator_convenio = 1.0 if convenio == 'Particular' else (0.5 if convenio == 'SUS' else random.uniform(0.7, 0.9))
        valor_final_cobrado = valor_base * fator_convenio

        # --- Consolida o registo ---
        atendimento_id = (numero_lote * tamanho_do_lote) + i
        registos_lote.append({
            'atendimento_id': atendimento_id,
            'paciente_id': paciente['paciente_id'],
            'nome_paciente': paciente['nome_paciente'],
            'data_nascimento_paciente': paciente['data_nascimento'],
            'data_atendimento': data_atendimento,
            'tipo_atendimento': tipo_atendimento,
            'setor_atendimento': setor,
            'dias_internacao': dias_internacao,
            'convenio': convenio,
            'valor_total_atendimento': round(valor_final_cobrado, 2),
            'status_pagamento': random.choice(STATUS_PAGAMENTO)
        })
    return pd.DataFrame(registos_lote)

# --- 5. EXECUÇÃO PRINCIPAL DO PROCESSO DE CHUNKING ---
# Este é o coração da operação: um ciclo que gera e grava os dados em lotes.

# Garante que a pasta /data exista
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Remove o ficheiro antigo, se existir, para começar do zero.
if os.path.exists(OUTPUT_FILENAME):
    os.remove(OUTPUT_FILENAME)
    print(f"Ficheiro antigo '{OUTPUT_FILENAME}' removido.")

for i in range(NUM_LOTES):
    # Gera um novo lote de dados
    df_lote = gerar_lote(i, NUM_LOTES, TAMANHO_LOTE)
    
    # Na primeira iteração (i=0), escreve o cabeçalho no ficheiro CSV.
    # Nas iterações seguintes, adiciona os dados sem o cabeçalho (append).
    df_lote.to_csv(
        OUTPUT_FILENAME,
        mode='a',  # 'a' para append (adicionar ao fim do ficheiro)
        header=(i == 0), # Escreve o cabeçalho apenas na primeira vez
        index=False,
        sep=';',
        decimal=','
    )
    print(f"Lote {i + 1} gravado com sucesso. Total de linhas geradas: {(i + 1) * TAMANHO_LOTE:,}")

print("\n==========================================================")
print("PROJETO HOSPITAL VIDA PLENA - GERAÇÃO DE DADOS CONCLUÍDA!")
print(f"Dataset com {TOTAL_REGISTOS:,} linhas foi gerado.")
print(f"Arquivo salvo como: {OUTPUT_FILENAME}")
print("==========================================================")
