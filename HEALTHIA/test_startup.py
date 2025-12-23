import sys
import traceback

try:
    print("Testando importação da API...")
    from api.sintomasAPI import router, diagnosticoIA
    print("API importada com sucesso!")
    
    print("\nTestando predição...")
    resultado = diagnosticoIA.predict_simples("gripe")
    print(f"Resultado: {resultado}")
    
except Exception as e:
    print(f"ERRO: {e}")
    print("\nTraceback completo:")
    traceback.print_exc()
