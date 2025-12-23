import pandas as pd
from deep_translator import GoogleTranslator
from tqdm import tqdm
import os
import sys

# Add project root to path so we can import services later
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# Paths
csv_path = os.path.join(project_root, "..", "dataset_diagnostico_medico", "Symptom2Disease.csv")
dataset_service_path = os.path.join(project_root, "services", "datasetService.py")

from concurrent.futures import ThreadPoolExecutor, as_completed

def translate_row(row, translator, label_map):
    try:
        sintoma_en = row['text']
        sintoma_pt = translator.translate(sintoma_en)
        
        # Get original label and map it
        raw_label = row['label']
        # Normalized key for map lookup (if we stored it normalized) or just raw
        # We'll assume the map is keyed by the raw label from CSV
        
        diagnostico = label_map.get(raw_label, raw_label)
        
        # Final cleanup on the translated diagnosis (snake case, lowercase)
        # Using simple replacements to keep it robust
        diagnostico = diagnostico.lower().replace(" ", "_").replace("-", "_")
        
        # Remove accents from diagnosis key if desired, but user said "Português do Brasil"
        # usually implies keeping accents in text but maybe keys should be simple?
        # The existing keys are "anemia_falciforme" (no accent on anemia, but falciforme ok).
        # "sindrome_fadiga_cronica" -> no accents.
        # So I should remove accents from the key.
        import unicodedata
        diagnostico = ''.join(c for c in unicodedata.normalize('NFD', diagnostico) if unicodedata.category(c) != 'Mn')
        
        return (sintoma_pt, diagnostico)
    except Exception as e:
        return None

def translate_and_load_data():
    print(f"Lendo CSV de: {csv_path}")
    if not os.path.exists(csv_path):
        print(f"ERRO: Arquivo não encontrado: {csv_path}")
        return []

    df = pd.read_csv(csv_path)
    # df = df.head(50) # Uncomment to test with fewer items
    translator = GoogleTranslator(source='en', target='pt')
    
    # 1. Translate Labels First (Sequential)
    print("Traduzindo diagnósticos (labels)...")
    unique_labels = df['label'].unique()
    label_map = {}
    
    for label in tqdm(unique_labels):
        try:
            # Replace underscores/hyphens for translation
            text = label.replace("_", " ").replace("-", " ")
            translated = translator.translate(text)
            label_map[label] = translated
            # print(f"  {label} -> {translated}")
        except Exception as e:
            print(f"Erro traduzindo label {label}: {e}")
            label_map[label] = label

    dados_traduzidos = []
    
    print("Traduzindo sintomas (multi-threading)...")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        # We pass label_map to the function
        futures = {executor.submit(translate_row, row, translator, label_map): row for _, row in df.iterrows()}
        
        for future in tqdm(as_completed(futures), total=len(futures)):
            result = future.result()
            if result:
                dados_traduzidos.append(result)
            
    return dados_traduzidos

def update_dataset_file(new_data):
    print(f"Atualizando {dataset_service_path}...")
    
    with open(dataset_service_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the dataset_completo function
    func_start = content.find("def dataset_completo():")
    if func_start == -1:
        print("ERRO: Função dataset_completo não encontrada.")
        return False
        
    # Find the last closing bracket BEFORE the function definition
    last_bracket_index = content.rfind("]", 0, func_start)
    
    if last_bracket_index == -1:
        print("ERRO: Não foi possível encontrar o final da lista 'dados' antes da função.")
        return False

    # Preparing the string to inject
    # format:     ("sintoma", "diagnostico"),
    new_content_str = "\n    # --- DADOS IMPORTADOS DE Symptom2Disease.csv ---\n"
    for sintoma, diagnostico in new_data:
        # Escape quotes in sintoma just in case
        sintoma_esc = sintoma.replace('"', '\\"')
        new_content_str += f'    ("{sintoma_esc}", "{diagnostico}"),\n'

    # Insert before the last bracket
    updated_content = content[:last_bracket_index] + new_content_str + content[last_bracket_index:]

    with open(dataset_service_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("Arquivo datasetService.py atualizado com sucesso.")
    return True

def run_retraining():
    print("\nIniciando retreinamento...")
    # Now we import the services to run the training. 
    # Since we modified the file on disk, we hope the import picks it up.
    # However, Python imports are cached. If this script imported datasetService before, it would use the old version.
    # But we haven't imported it yet in this script.
    
    try:
        from services.salvarmodelService import salvar_modelo, salvar_vetorizador, salvar_encoderY
        from services.treinamentoService import acuracia_modelo
        
        print("Salvando vetorizador...")
        salvar_vetorizador()
        print("Salvando encoder...")
        salvar_encoderY()
        print("Treinando e salvando modelo...")
        salvar_modelo()
        
        print("Calculando acurácia...")
        acc = acuracia_modelo()
        print(f"\n>>> NOVA ACURÁCIA DO MODELO: {acc:.2f}% <<<")
        
    except Exception as e:
        print(f"Erro durante o retreinamento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    novos_dados = translate_and_load_data()
    if novos_dados:
        if update_dataset_file(novos_dados):
            run_retraining()
    else:
        print("Nenhum dado novo foi traduzido ou erro na leitura.")
