import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
dataset_service_path = os.path.join(project_root, "services", "datasetService.py")

def cleanup():
    print(f"Lendo {dataset_service_path}...")
    with open(dataset_service_path, 'r', encoding='utf-8') as f:
        content = f.read()

    marker = "# --- DADOS IMPORTADOS DE Symptom2Disease.csv ---"
    
    if marker not in content:
        print("Marcador não encontrado. Arquivo talvez já esteja limpo ou marcador diferente.")
        return

    # Keep content before marker
    index = content.find(marker)
    # Find the last closing bracket before this marker? No, the marker was inserted BEFORE the last bracket.
    # Actually, the insertion logic was: 
    # updated_content = content[:last_bracket_index] + new_content_str + content[last_bracket_index:]
    # So the structure is:
    # ...
    # ("last original tuple"),
    # <MARKER>
    # ("new tuple"),
    # ...
    # ]
    #
    # So if we take content[:index], we are right after the last original tuple (and some whitespace/newlines).
    # We just need to add the closing bracket and the rest of the file (the function def).
    
    # We need to find the function def as well.
    func_marker = "def dataset_completo():"
    func_index = content.find(func_marker)
    
    if func_index == -1:
        print("Erro: Definição de função não encontrada.")
        return

    # We want: content[:index] (cleaned) + "]\n\n\n# criar uma funcao...\n" + content[func_index:]
    # But wait, content[last_bracket_index:] contained "]\n\n\n..."
    # So if we format it manually it's safer.
    
    clean_content = content[:index].rstrip() + "\n]\n\n\n\n# criar uma funcao e colocar os dados acima em um DataFrame Pandas\n" + content[func_index:]
    
    with open(dataset_service_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
        
    print("Arquivo limpo com sucesso!")

if __name__ == "__main__":
    cleanup()
