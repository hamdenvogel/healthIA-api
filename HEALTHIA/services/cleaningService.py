
import re

def limpar_texto(texto):
    """
    Remove verbos, expressões desnecessárias e stop words do texto.
    """
    if not isinstance(texto, str):
        return str(texto)
        
    texto = texto.lower()
    
    # Lista de expressões/palavras para remover (baseado no pedido do usuário)
    # "acabei de desenvolver", "está", "tenho tido", "experimentei", "tive", "estão", "bastante", "sólido como uma rocha"
    # Adicionando variações comuns e outras stopwords se necessário, mas focando no pedido.
    
    # Expressões exatas primeiro (para garantir que sejam removidas antes de palavras soltas se houver sobreposição)
    expressoes = [
        r"sólido como uma rocha",
        r"acabei de desenvolver",
        r"tenho tido",
        r"acabei de",
    ]
    
    for exp in expressoes:
        texto = re.sub(exp, "", texto)

    # Palavras soltas (verbos e adverbios citados)
    palavras_remover = [
        "desenvolver", "está", "experimentei", "tive", "estão", "bastante",
        "tenho", "tido", "acabei", "sólido", "rocha", "como", "uma", "de", 
        "estou", "sou", "foi", "era", "ser", "sido", "fui", 
        "me", "mim", "com", "em", "para", "por", "sem", "sob",
        "o", "a", "os", "as", "um", "uma", "uns", "umas",
        "e", "ou", "mas", "que", "se", "no", "na", "nos", "nas", "do", "da", "dos", "das"
    ]
    
    # Cria uma regex para remover essas palavras isoladas
    # \b garante que é a palavra inteira
    padrao = r"\b(" + "|".join(palavras_remover) + r")\b"
    texto = re.sub(padrao, "", texto)
    
    # Remove pontuação básica e espaços extras
    texto = re.sub(r'[^\w\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto
