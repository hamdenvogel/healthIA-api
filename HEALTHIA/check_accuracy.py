from services.treinamentoService import acuracia_modelo
import os
import sys

# Ensure we are in the right directory or have it in sys.path
sys.path.append(os.getcwd())

print("Calculando a acurácia do modelo...")
try:
    acuracia = acuracia_modelo()
    print(f"Acurácia prevista do modelo: {acuracia:.2f}%")
except Exception as e:
    print(f"Erro ao calcular acurácia: {e}")
    import traceback
    traceback.print_exc()
