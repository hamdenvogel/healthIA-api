
import sys
import os

print("Script iniciado.")
print(f"CWD: {os.getcwd()}")

if __name__ == "__main__":
    # Adicionar o diretório raiz ao sys.path para permitir importações
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    print("Iniciando imports...")
    try:
        from services.salvarmodelService import salvar_vetorizador, salvar_encoderY, salvar_modelo
        print("Imports concluídos.")
        
        print("Iniciando retreinamento e salvamento dos artefatos...")
        salvar_vetorizador()
        print("Vetorizador salvo.")
        salvar_encoderY()
        print("Encoder salvo.")
        salvar_modelo()
        print("Modelo salvo.")
        print("Processo concluído com sucesso.")
    except Exception as e:
        print(f"Erro durante o processo: {e}")
        import traceback
        traceback.print_exc()
