import os
import sys

# Adicionar o diretório raiz ao sys.path para permitir importações dos serviços
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.nlp_spacy import limpar_sintomas, dados_brutos
import re

def integrar():
    dataset_path = r'c:\Hamden\Sistemas\Backend\python\HEALTHIA\services\datasetService.py'
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        return

    print(f"Processing {len(dados_brutos)} records from nlp_spacy.py...")
    
    novos_dados = []
    for sintoma, diagnostico in dados_brutos:
        sintoma_limpo = limpar_sintomas(sintoma)
        novos_dados.append((sintoma_limpo, diagnostico))

    print(f"Reading {dataset_path}...")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Procurar o final da lista 'dados'
    # Procuramos por 'dados = [' e depois o ']' de fechamento
    match = re.search(r'dados = \[(.*?)\]', content, re.DOTALL)
    if not match:
        print("Could not find 'dados' list in datasetService.py")
        return

    # Gerar a string com os novos dados
    novas_linhas = "\n    # --- Dados integrados via NLP pipeline ---\n"
    for s, d in novos_dados:
        novas_linhas += f'    ("{s}", "{d}"),\n'
    
    # Inserir antes do fechamento da lista
    novo_conteudo = content[:match.end() - 1] + novas_linhas + content[match.end() - 1:]

    print(f"Updating datasetService.py with {len(novos_dados)} new entries...")
    with open(dataset_path, 'w', encoding='utf-8') as f:
        f.write(novo_conteudo)
    
    print("Integration complete.")

if __name__ == "__main__":
    integrar()
