import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from services.datasetService import dados

unique_diagnoses = sorted(list(set(d[1] for d in dados)))

print(f"Total entries: {len(dados)}")
print(f"Unique diagnoses: {len(unique_diagnoses)}")
for diag in unique_diagnoses:
    print(diag)
