import sys
import os

# Adiciona o diretório atual ao path para importar services
sys.path.append(os.getcwd())

from services.nlp_spacy import limpar_sintomas

test_sentences = [
    "estou com muita fraqueza",
    "sinto tontura constante",
    "dor na garganta",
    "mancha na pele",
    "insônia severa",
    "dor na bunda",
    "muita ansiedade",
    "diarreia líquida",
    "temperatura alta",
    "boca seca",
    "fezes líquidas",
    "mãos secas"
]

print(f"{'Input Sentence':<30} | {'Cleaned (NLP)':<30}")
print("-" * 65)

for text in test_sentences:
    cleaned = limpar_sintomas(text)
    print(f"{text:<30} | {cleaned:<30}")
