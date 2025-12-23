import os
import joblib
import xgboost as xgb
import numpy as np

try:
    print("Testando a predição completa...")
    from services.executarService import DiagnosticoIA
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'model')
    
    diagnostico = DiagnosticoIA(model_path)
    resultado = diagnostico.predict_simples('gripe')
    print(f"Resultado: {resultado}")
    print(f"Tipo: {type(resultado)}")
    print("\nSucesso!")
    
except Exception as e:
    print(f"\nErro: {type(e).__name__}")
    print(f"Mensagem: {str(e)}")
    import traceback
    traceback.print_exc()
