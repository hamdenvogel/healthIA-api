
import sys
import os

print(f"CWD: {os.getcwd()}")
print(f"Path: {sys.path}")

try:
    from services.datasetService import dataset_completo
    print("dataset_completo imported")
    df = dataset_completo()
    print(f"DataFrame shape: {df.shape}")
    print("Head:")
    print(df.head())
except Exception as e:
    print(f"Error importing or running dataset_completo: {e}")
    import traceback
    traceback.print_exc()

try:
    from services.vetorizacaoService import vetorizacao
    print("vetorizacao imported")
    X = vetorizacao()
    print(f"X shape: {X.shape}")
except Exception as e:
    print(f"Error running vetorizacao: {e}")
    import traceback
    traceback.print_exc()
