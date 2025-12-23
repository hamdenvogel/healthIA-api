import os
import sys
import re

# Add root directory to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.nlp_spacy import limpar_sintomas
from services.datasetService import dados

def mass_clean():
    dataset_path = r'c:\Hamden\Sistemas\Backend\python\HEALTHIA\services\datasetService.py'
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        return

    print(f"Beginning mass clean of {len(dados)} records...")
    
    unique_cleaned_dados = []
    seen = set()
    
    for i, (sintoma, diagnostico) in enumerate(dados):
        if i % 100 == 0:
            print(f"Processing record {i}...")
            
        sintoma_limpo = limpar_sintomas(sintoma)
        
        # Deduplication check
        item_key = (sintoma_limpo, diagnostico)
        if item_key not in seen:
            unique_cleaned_dados.append(item_key)
            seen.add(item_key)

    print(f"Cleaning complete. Unique records: {len(unique_cleaned_dados)} (from {len(dados)})")

    print(f"Reading original file structure from {dataset_path}...")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Reconstruct the 'dados' list in the file
    # We find the start and end of the list to replace its content
    start_tag = 'dados = ['
    end_tag = ']'
    
    start_index = content.find(start_tag)
    if start_index == -1:
        print("Could not find 'dados = [' in datasetService.py")
        return
    
    # We need to find the matching closing bracket for the dados list
    # Since the list is huge, we'll look for the last ']' before 'def dataset_completo'
    ref_index = content.find('def dataset_completo')
    if ref_index == -1:
        # Fallback to finding the last bracket if function name changes
        end_index = content.rfind(end_tag)
    else:
        end_index = content.rfind(end_tag, start_index, ref_index)

    if end_index == -1 or end_index <= start_index:
        print("Could not find appropriate closing bracket for 'dados' list.")
        return

    # Build the new content
    new_list_str = 'dados = [\n'
    for s, d in unique_cleaned_dados:
        new_list_str += f'    ("{s}", "{d}"),\n'
    new_list_str += ']'

    final_content = content[:start_index] + new_list_str + content[end_index + 1:]

    print(f"Overwriting {dataset_path} with NLP-optimized data...")
    with open(dataset_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print("Mass cleaning successfully completed.")

if __name__ == "__main__":
    mass_clean()
