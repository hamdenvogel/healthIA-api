import os
from fastapi import APIRouter, HTTPException
from services.executarService import DiagnosticoIA


router = APIRouter()

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
model_path = os.path.join(project_root, 'model')

diagnosticoIA = DiagnosticoIA(caminhoModelo=model_path)


@router.get("/")
async def raiz():
    return {"Message": "Welcome to HealthIA API"}


#usuario envia os sintomas via query params
@router.get("/predict/")
async def predict(sintomas: str):
    """
    Endpoint para predição de diagnóstico com base em sintomas fornecidos via query params.
    Exige no mínimo 4 sintomas.
    """
    sintomas_list = [s.strip() for s in sintomas.split(',') if s.strip()]
    
    if len(sintomas_list) < 4:
        raise HTTPException(
            status_code=400, 
            detail=f"É necessário fornecer no mínimo 4 sintomas para uma predição confiável. Você forneceu {len(sintomas_list)}."
        )

    # Retorna os top 3 diagnósticos mais prováveis
    diagnosticos_provaveis = diagnosticoIA.predict_top_k(sintomas_list, k=3)

    return {
        "sintomas": sintomas_list,
        "diagnosticos_provaveis": diagnosticos_provaveis
    }


@router.get("/predict-lista/")
async def predict_lista(sintomas: str, k: int = 10):
    """
    Endpoint para predição de múltiplos diagnósticos com base em sintomas.
    Exige no mínimo 4 sintomas.
    """
    # Limpa e filtra a lista de sintomas
    sintomas_list = [s.strip() for s in sintomas.split(',') if s.strip()]
    
    if len(sintomas_list) < 4:
        raise HTTPException(
            status_code=400, 
            detail=f"É necessário fornecer no mínimo 4 sintomas para uma predição confiável. Você forneceu {len(sintomas_list)}."
        )

    diagnosticos_previstos = diagnosticoIA.predict_top_k(sintomas_list, k)

    return {
        "sintomas": sintomas_list,
        "diagnosticos_previstos": diagnosticos_previstos
    }

# Reload trigger comment (Translation updated)
