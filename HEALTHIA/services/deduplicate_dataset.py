import os
import sys

def deduplicate():
    filepath = r'c:\Hamden\Sistemas\Backend\python\HEALTHIA\services\nlp_spacy.py'
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    print(f"Reading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_list = False
    list_lines = []
    
    count_before = 0
    count_after = 0

    for line in lines:
        if 'dados_brutos = [' in line:
            in_list = True
            new_lines.append(line)
            continue
        
        if in_list:
            if line.strip().startswith(']'):
                in_list = False
                
                # Deduplicate
                unique_content = []
                seen = set()
                
                for l in list_lines:
                    # Clean the line for comparison (remove whitespace and trailing comma)
                    clean_item = l.strip().rstrip(',')
                    if not clean_item:
                        continue
                        
                    count_before += 1
                    if clean_item not in seen:
                        unique_content.append(l)
                        seen.add(clean_item)
                        count_after += 1
                
                new_lines.extend(unique_content)
                new_lines.append(line)
                continue
            
            list_lines.append(line)
        else:
            new_lines.append(line)

    print(f"Duplicates found and removed. Items before: {count_before}, after: {count_after}")
    
    if count_before > count_after:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("File updated successfully.")
    else:
        print("No duplicates found or file already clean.")

if __name__ == "__main__":
    deduplicate()
