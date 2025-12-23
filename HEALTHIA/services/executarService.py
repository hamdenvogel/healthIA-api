import os
import joblib
import xgboost as xgb
import numpy as np
from services.datasetService import dataset_completo


class DiagnosticoIA:
    
    def __init__(self, caminhoModelo: str):
        self.caminho_raiz = caminhoModelo
        # Carregar o modelo diretamente sem instanciar primeiro
        modelo_path = os.path.join(self.caminho_raiz, 'modelo_HealthIA.json')
        self.HealthIA = xgb.Booster()
        self.HealthIA.load_model(modelo_path)
        self.vetorizadortfidf = joblib.load(os.path.join(self.caminho_raiz, 'vetorizador_HealthIA.pkl'))
        self.encoderYPronto = joblib.load(os.path.join(self.caminho_raiz, 'encoderY_HealthIA.pkl'))
        
        # Lista simples com os nomes dos diagnósticos


    def predict_simples(self, sintomas):
        """
        Função simples para fazer predição
        """
        # Converter lista para string se necessário
        if isinstance(sintomas, list):
            sintomas_string = " ".join(sintomas)
        else:
            sintomas_string = sintomas
        
        # Vetorizar os sintomas
        from services.cleaningService import limpar_texto
        # Limpar o texto antes de vetorizar
        sintomas_string = limpar_texto(sintomas_string)
        
        sintomas_vetorizados = self.vetorizadortfidf.transform([sintomas_string])
        
        # Fazer predição usando Booster (DMatrix necessário)
        dmatrix = xgb.DMatrix(sintomas_vetorizados)
        predicao = self.HealthIA.predict(dmatrix)
        
        # Decodificar usando o array de labels
        # diagnostico = self.encoderYPronto.inverse_transform([pred_index])[0]
        print(f"DEBUG: predicao shape: {predicao.shape}")
        print(f"DEBUG: predicao[0]: {predicao[0]}")
        
        # Pegar o índice da classe com maior probabilidade
        pred_index = int(np.argmax(predicao[0]))
        
        # Decodificar usando o array de labels
        diagnostico = self.encoderYPronto.inverse_transform([pred_index])[0]
        
        return diagnostico

    def predict_top_k(self, sintomas, k=10):
        """
        Função para fazer predição retornando os k diagnósticos mais prováveis
        """
        # Converter lista para string se necessário
        if isinstance(sintomas, list):
            sintomas_string = " ".join(sintomas)
        else:
            sintomas_string = sintomas
        
        # Vetorizar os sintomas
        sintomas_vetorizados = self.vetorizadortfidf.transform([sintomas_string])
        
        # Fazer predição usando Booster (DMatrix necessário)
        dmatrix = xgb.DMatrix(sintomas_vetorizados)
        predicao = self.HealthIA.predict(dmatrix)
        
        # Obter os índices dos top k scores (argsort retorna ordem crescente, então pegamos o final e invertemos)
        # Garantir que k não seja maior que o número total de classes
        num_classes = len(predicao[0])
        k = min(k, num_classes)
        
        top_k_indices = np.argsort(predicao[0])[-k:][::-1]
        
        # Obter os diagnósticos e probabilidades correspondentes
        resultados = []
        labels = self.encoderYPronto.inverse_transform(top_k_indices)
        
        for i, idx in enumerate(top_k_indices):
            resultados.append({
                "diagnostico": labels[i],
                "probabilidade": float(predicao[0][idx])
            })
            
        return resultados


