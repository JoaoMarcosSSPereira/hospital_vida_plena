# ==============================================================================
# JM ANALYTICS - PROJETO HOSPITAL VIDA PLENA (MÓDULO SUPPLY CHAIN)
# Arquivo: supply_chain_generator.py
# Localização: /hospital_vida_plena_dashboard/scripts/
# Descrição: Script para geração de dados sintéticos focados na cadeia de
#            suprimentos (Supply Chain) do hospital.
# ==============================================================================
import pandas as pd
from faker import Faker
from tqdm import tqdm
import random
from datetime import datetime, timedelta
import os

print("Iniciando a simulação da Cadeia de Suprimentos do Hospital Vida Plena...")

# --- 1. CONFIGURAÇÃO DA SIMULAÇÃO ---
fake = Faker('pt_BR')
TOTAL_PEDIDOS = 50_000
OUTPUT_DIR = 'data'
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, 'hospital_supply_chain_dataset.csv')
DATA_INICIAL = datetime(2015, 1, 1)
DATA_FINAL = datetime(2024, 12, 31)

# --- 2. DEFINIÇÃO DAS LISTAS DE DIMENSÕES ---
FORNECEDORES = [
    {'fornecedor_id': 101, 'nome_fornecedor': 'MedSupply Brasil'},
    {'fornecedor_id': 102, 'nome_fornecedor': 'FarmaLog Distribuidora'},
    {'fornecedor_id': 103, 'nome_fornecedor': 'Cirúrgica Atlas'},
    {'fornecedor_id': 104, 'nome_fornecedor': 'CleanHealth Insumos'}
]
STATUS_ENTREGA = ['Entregue', 'Pendente', 'Atrasado']

# Catálogo de Produtos
PRODUTOS = [
    {'item_id': 2001, 'nome_item': 'Paracetamol 500mg (cx c/ 20)', 'categoria': 'Medicamento', 'custo_base': 15.50},
    {'item_id': 2002, 'nome_item': 'Luvas Cirúrgicas Estéreis (par)', 'categoria': 'Material Cirúrgico', 'custo_base': 2.50},
    {'item_id': 2003, 'nome_item': 'Seringa Descartável 10ml', 'categoria': 'Material Cirúrgico', 'custo_base': 0.80},
    {'item_id': 2004, 'nome_item': 'Máscara N95', 'categoria': 'EPI', 'custo_base': 3.20},
    {'item_id': 2005, 'nome_item': 'Álcool em Gel 70% (1L)', 'categoria': 'Material de Limpeza', 'custo_base': 12.00},
    {'item_id': 2006, 'nome_item': 'Amoxicilina 250mg', 'categoria': 'Medicamento', 'custo_base': 45.00},
    {'item_id': 2007, 'nome_item': 'Gaze Estéril (pacote c/ 100)', 'categoria': 'Material Cirúrgico', 'custo_base': 25.00}
]

# --- 3. GERAÇÃO DOS DADOS ---
print(f"Gerando {TOTAL_PEDIDOS} registos de pedidos...")
pedidos = []
for i in tqdm(range(TOTAL_PEDIDOS)):
    pedido_id = 500000 + i
    produto = random.choice(PRODUTOS)
    fornecedor = random.choice(FORNECEDORES)
    data_pedido = fake.date_time_between(start_date=DATA_INICIAL, end_date=DATA_FINAL)
    quantidade = random.randint(10, 500)
    
    # Simula uma pequena variação no custo
    custo_unitario = round(produto['custo_base'] * random.uniform(0.95, 1.05), 2)
    custo_total = quantidade * custo_unitario
    
    status = random.choices(STATUS_ENTREGA, weights=[0.85, 0.05, 0.10], k=1)[0]
    data_entrega_prevista = data_pedido + timedelta(days=random.randint(7, 20))
    data_entrega_real = None
    if status == 'Entregue':
        data_entrega_real = data_entrega_prevista - timedelta(days=random.randint(0, 3))
    elif status == 'Atrasado':
        data_entrega_real = data_entrega_prevista + timedelta(days=random.randint(1, 10))

    pedidos.append({
        'pedido_id': pedido_id,
        'item_id': produto['item_id'],
        'nome_item': produto['nome_item'],
        'categoria_item': produto['categoria'],
        'fornecedor_id': fornecedor['fornecedor_id'],
        'nome_fornecedor': fornecedor['nome_fornecedor'],
        'data_pedido': data_pedido,
        'quantidade_pedida': quantidade,
        'custo_unitario': custo_unitario,
        'custo_total_pedido': round(custo_total, 2),
        'status_entrega': status,
        'data_entrega_prevista': data_entrega_prevista,
        'data_entrega_real': data_entrega_real
    })

df_pedidos = pd.DataFrame(pedidos)

# --- 4. EXPORTAÇÃO PARA CSV ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
df_pedidos.to_csv(OUTPUT_FILENAME, index=False, sep=';', decimal=',')

print("\n==========================================================")
print("PROJETO HOSPITAL VIDA PLENA - GERAÇÃO DE DADOS DE SUPPLY CHAIN CONCLUÍDA!")
print(f"Dataset com {len(df_pedidos)} linhas foi gerado.")
print(f"Arquivo salvo como: {OUTPUT_FILENAME}")
print("==========================================================")
