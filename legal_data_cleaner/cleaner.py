"""cleaner.py: Lógica de transformación y estandarización de nombres."""

import re
from unidecode import unidecode
from legal_data_cleaner.constants import NOISE_WORDS

def _strip_non_alpha(text: str) -> str:
    """Replica "^[^A-Za-z]+|[^A-Za-z]+$" de R para limpiar extremos."""
    # Eliminamos lo que no sea letra al inicio y al final
    return re.sub(r"^[^A-Za-z]+|[^A-Za-z]+$", "", text).strip()

def standardize_name(raw_name: str) -> str:
    if not raw_name or not isinstance(raw_name, str):
        return ""

    # 1. Limpieza inicial
    name = raw_name.strip()

    # 2. Eliminar paréntesis y corchetes (reemplazo con "" para evitar espacios extras)
    name = re.sub(r"\([^)]*\)|\[[^\]]*\]", "", name)
    name = _strip_non_alpha(name)

    # 3. Formato "Apellido, Nombre"
    if name.count(",") == 1:
        parts = [p.strip() for p in name.split(",", 1)]
        if len(parts) == 2:
            name = f"{parts[1]} {parts[0]}"
            name = _strip_non_alpha(name)

    # 4. Transliteración (Acentos y Ñ)
    name = unidecode(name)

    # 5. Remover números
    name = re.sub(r"\d", "", name)
    name = _strip_non_alpha(name)

    # 6. Mayúsculas
    name = name.upper()

    # 7. Filtrado de Ruido y Letras Sueltas
    # Aquí sí usamos split() porque ya queremos evaluar palabras individuales
    words = name.split()
    cleaned_words = []
    
    for w in words:
        # Limpiamos cada palabra de caracteres no alfa en sus propios extremos
        clean_w = re.sub(r"^[^A-Z]+|[^A-Z]+$", "", w)
        
        # Mantener si es un símbolo especial (ej. &, +, ;)
        if len(w) == 1 and not w.isalpha():
            cleaned_words.append(w)
        # Mantener si no es ruido y mide más de 1 letra
        elif clean_w not in NOISE_WORDS and len(clean_w) > 1:
            cleaned_words.append(clean_w)

    # Unimos con un solo espacio
    name = " ".join(cleaned_words)
    
    # 8. Limpieza final absoluta de extremos
    return _strip_non_alpha(name)

def check_identity_match(name_a: str, name_b: str) -> bool:
    """Compara dos nombres usando igualdad estricta tras la limpieza.

    Args:
        name_a: Primer nombre a comparar.
        name_b: Segundo nombre a comparar.

    Returns:
        True si ambos nombres son idénticos después de estandarizarlos.
    """
    return standardize_name(name_a) == standardize_name(name_b)
