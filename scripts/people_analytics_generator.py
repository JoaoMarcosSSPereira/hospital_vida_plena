# ==============================================================================
# JM ANALYTICS - PROJETO PEOPLE ANALYTICS
# Arquivo: people_analytics_generator.py
# Descrição: Script para geração de dados sintéticos focados em Recursos Humanos
#            e análise de pessoal (People Analytics).
# ==============================================================================
import pandas as pd
from faker import Faker
from tqdm import tqdm
import random
from datetime import datetime, timedelta
import os

print("Iniciando a simulação de dados para People Analytics...")

# --- 1. CONFIGURAÇÃO DA SIMULAÇÃO ---
fake = Faker('pt_BR')
TOTAL_FUNCIONARIOS = 50_000
OUTPUT_DIR = 'data'
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, 'people_analytics_dataset.csv')
DATA_INICIAL_CONTRATACAO = datetime(2020, 1, 1)
DATA_ATUAL = datetime(2025, 8, 5)

# --- 2. DEFINIÇÃO DAS LISTAS DE DIMENSÕES ---
DEPARTAMENTOS = ['Vendas', 'Tecnologia', 'Marketing', 'Recursos Humanos', 'Financeiro', 'Operações']
CARGOS = {
    'Vendas': ['Representante de Vendas', 'Gerente de Contas', 'Diretor de Vendas'],
    'Tecnologia': ['Desenvolvedor Júnior', 'Desenvolvedor Pleno', 'Desenvolvedor Sénior', 'Arquiteto de Software'],
    'Marketing': ['Analista de Marketing', 'Especialista em SEO', 'Gerente de Marketing'],
    'Recursos Humanos': ['Analista de RH', 'Business Partner', 'Gerente de RH'],
    'Financeiro': ['Analista Financeiro', 'Contabilista', 'Controller'],
    'Operações': ['Analista de Logística', 'Coordenador de Operações', 'Gerente de Operações']
}
NIVEL_SENIORIDADE = ['Júnior', 'Pleno', 'Sénior', 'Liderança']
MOTIVO_SAIDA = ['Voluntário - Outra Oportunidade', 'Voluntário - Insatisfação', 'Involuntário - Performance', 'Involuntário - Reestruturação']

# --- 3. GERAÇÃO DOS DADOS ---
print(f"Gerando {TOTAL_FUNCIONARIOS} registos de funcionários...")
funcionarios = []
for i in tqdm(range(TOTAL_FUNCIONARIOS)):
    employee_id = 1000 + i
    nome = fake.name()
    genero = random.choice(['Masculino', 'Feminino'])
    idade = random.randint(18, 65)
    departamento = random.choice(DEPARTAMENTOS)
    cargo = random.choice(CARGOS[departamento])
    
    # Lógica para definir senioridade e salário base
    if any(s in cargo for s in ['Júnior', 'Representante', 'Analista']):
        nivel_senioridade = 'Júnior'
        salario_base = random.uniform(2500, 4500)
    elif any(s in cargo for s in ['Pleno', 'Especialista', 'Contabilista']):
        nivel_senioridade = 'Pleno'
        salario_base = random.uniform(4500, 7500)
    elif any(s in cargo for s in ['Sénior', 'Coordenador']):
        nivel_senioridade = 'Sénior'
        salario_base = random.uniform(7500, 12000)
    else: # Gerente, Diretor, Arquiteto
        nivel_senioridade = 'Liderança'
        salario_base = random.uniform(12000, 25000)
        
    salario_mensal = round(salario_base, 2)
    
    data_contratacao = fake.date_time_between(start_date=DATA_INICIAL_CONTRATACAO, end_date=DATA_ATUAL)
    
    # Simulação de Turnover (Rotatividade)
    tempo_empresa = (DATA_ATUAL - data_contratacao).days / 365.25
    chance_saida = 0.05 + (0.3 / (1 + tempo_empresa)) # Maior chance de sair no início
    
    data_termino = None
    motivo_saida = None
    if random.random() < chance_saida:
        data_termino = fake.date_time_between(start_date=data_contratacao + timedelta(days=180), end_date=DATA_ATUAL)
        motivo_saida = random.choice(MOTIVO_SAIDA)

    # Simulação de Performance e Satisfação (com alguma correlação)
    satisfacao_trabalho = random.randint(1, 5)
    avaliacao_desempenho = satisfacao_trabalho - random.choice([-1, 0, 0, 1])
    avaliacao_desempenho = max(1, min(5, avaliacao_desempenho)) # Garante que a nota fica entre 1 e 5

    if motivo_saida and 'Insatisfação' in motivo_saida:
        satisfacao_trabalho = random.randint(1, 2)
    
    horas_extras_mes = random.randint(0, 40)
    promovido_ultimo_ano = 'Não'
    if avaliacao_desempenho >= 4 and tempo_empresa > 1.5 and random.random() < 0.3: # 30% de chance de promoção para bons funcionários
        promovido_ultimo_ano = 'Sim'

    funcionarios.append({
        'employee_id': employee_id,
        'nome_completo': nome,
        'idade': idade,
        'genero': genero,
        'departamento': departamento,
        'cargo': cargo,
        'nivel_senioridade': nivel_senioridade,
        'data_contratacao': data_contratacao.date(),
        'data_termino': data_termino.date() if data_termino else None,
        'motivo_saida': motivo_saida,
        'salario_mensal': salario_mensal,
        'avaliacao_desempenho_anual': avaliacao_desempenho,
        'satisfacao_trabalho': satisfacao_trabalho,
        'horas_extras_mes': horas_extras_mes,
        'promovido_ultimo_ano': promovido_ultimo_ano,
        'tempo_empresa_anos': round(tempo_empresa, 2)
    })

df_funcionarios = pd.DataFrame(funcionarios)

# --- 4. EXPORTAÇÃO PARA CSV ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
df_funcionarios.to_csv(OUTPUT_FILENAME, index=False, sep=';', decimal=',')

print("\n==========================================================")
print("PROJETO PEOPLE ANALYTICS - GERAÇÃO DE DADOS CONCLUÍDA!")
print(f"Dataset com {len(df_funcionarios)} linhas foi gerado.")
print(f"Arquivo salvo como: {OUTPUT_FILENAME}")
print("==========================================================")

