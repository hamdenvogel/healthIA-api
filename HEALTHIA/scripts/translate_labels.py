import re
import os
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor

# Path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
dataset_service_path = os.path.join(project_root, "services", "datasetService.py")

def translate_labels():
    print(f"Lendo {dataset_service_path}...")
    with open(dataset_service_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find tuples: ("text", "label")
    # Captures label in group 1
    # We assume standard formatting from previous steps
    pattern = re.compile(r'\(".*?",\s*"(.*?)"\)')
    
    matches = pattern.findall(content)
    unique_labels = sorted(list(set(matches)))
    
    print(f"Encontrados {len(unique_labels)} diagnósticos únicos.")
    
    translator = GoogleTranslator(source='en', target='pt')
    
    # Dictionary to store translations
    translations = {}
    
    def translate_single(label):
        # Skip if already looks Portuguese or is one of the known keys?
        # Actually, let's just translate everything that looks English-ish or just everything.
        # But we want to avoid translating "anemia_falciforme" effectively if it's already ok.
        # Ideally we only translate the new English ones.
        # English ones often have underscores or spaces.
        # Let's try to translate. If it's the same, no harm.
        try:
            # Replace underscores with spaces for better translation
            text_to_translate = label.replace("_", " ")
            translated = translator.translate(text_to_translate)
            # Slugify back: lowercase, spaces to underscores, remove accents if desired?
            # User asked for "Portuguese do Brasil". Usually we keep accents in display but maybe not in code keys?
            # The existing keys have underscores "anemia_falciforme", "diabetes_tipo1".
            # The response JSON shows "sintomas" and "diagnostico_previsto".
            # If I return "Depressão" it's fine.
            # But the model classes need to be consistent.
            # Let's clean the translated string: lowercase, replace spaces with underscores.
            # actually keep accents if the user wants "Portuguese".
            # But for simple IDs, usually we remove accents.
            # However, the user request says "Todos sejam traduzidos...".
            # If I change "peptic_ulcer_disease" to "doença_úlcera_péptica" -> "doenca_ulcera_peptica" (normalized)
            # let's try to keep it simple: lowercase, space -> underscore.
            # But `deep_translator` returns utf-8.
            
            # Helper to normalize
            normalized = translated.lower().replace(" ", "_").replace("-", "_")
            # Remove accents?
            import unicodedata
            normalized = ''.join(c for c in unicodedata.normalize('NFD', normalized) if unicodedata.category(c) != 'Mn')
            
            return label, normalized
        except Exception as e:
            print(f"Error translating {label}: {e}")
            return label, label

    print("Traduzindo labels...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(translate_single, unique_labels)
        for original, translated in results:
            translations[original] = translated
            print(f"{original} -> {translated}")

    # Now replace in content
    # We must be careful not to replace partial matches if iterate blindly.
    # But since we extracted exact matches from the quotes, we can replace strictly.
    # To be safe, we iterate through unique labels and replace instances.
    # Since we want to replace ` "original"),` with ` "translated"),`
    
    new_content = content
    # Sort by length descending to avoid prefix issues (though unlikely with exact quotes)
    for original in sorted(unique_labels, key=len, reverse=True):
        if original in translations and translations[original] != original:
            # Replace only the label part of the tuple
            # Pattern: ", "{original}")"
            # We use distinct replacement to ensure we don't change symptoms (first element)
            # The regex for matching the tuple end is `",\s*"{original}"\)`
            
            # Simple string replace for `"{original}")` might be risky if symptom text ends with that.
            # But symptom text is the first element.
            # Format is `("sintoma", "label")`.
            # So `", "{original}")` is unique enough (comma, space, quote, label, quote, parenthesis).
            
            target = f', "{original}")'
            replacement = f', "{translations[original]}")'
            new_content = new_content.replace(target, replacement)
            
    with open(dataset_service_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("datasetService.py atualizado com sucesso!")

if __name__ == "__main__":
    translate_labels()
