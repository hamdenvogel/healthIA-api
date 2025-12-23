
from services.cleaningService import limpar_texto
import time

sintomas = "acabei de desenvolver uma dor de cabeça forte"
start = time.time()
print(f"Original: {sintomas}")
limpo = limpar_texto(sintomas)
print(f"Limpo: {limpo}")
print(f"Tempo: {time.time() - start:.4f}s")

sintomas_longo = "tenho tido bastante dor solido como uma rocha"
print(f"Original: {sintomas_longo}")
print(f"Limpo: {limpar_texto(sintomas_longo)}")
