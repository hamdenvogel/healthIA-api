import os
import sys

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

try:
    from services.salvarmodelService import salvar_modelo, salvar_vetorizador, salvar_encoderY
    from services.treinamentoService import acuracia_modelo
    
    print("Iniciando processo de treinamento...")
    
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
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
