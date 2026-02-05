"""Lógica de transformación y estandarización de nombres."""

import re

from unidecode import unidecode

from .constants import NOISE_WORDS


def standardize_name(raw_name: str) -> str:
    """Transforma un nombre crudo a formato canónico ASCII en mayúsculas.

    Proceso:
        1. Quita espacios en los extremos.
        2. Elimina contenido entre paréntesis.
        3. Remueve acentos y convierte ñ -> n (via unidecode).
        4. Elimina caracteres especiales no alfanuméricos.
        5. Remueve palabras clave de ruido definidas en constants.
        6. Convierte a mayúsculas.

    Args:
        raw_name: Cualquier string proveniente de un input humano.

    Returns:
        Nombre estandarizado en ASCII mayúsculas.

    Example:
        >>> standardize_name("  Peña, José (Lead Visa T) ")
        'JOSE PENA'
    """
    if not raw_name or not isinstance(raw_name, str):
        return ""

    # 1. Quitar espacios en los extremos
    name = raw_name.strip()

    # 2. Eliminar contenido entre paréntesis (incluyendo los paréntesis)
    name = re.sub(r"\([^)]*\)", "", name)

    # 2b. Manejar formato "Apellido, Nombre" -> "Nombre Apellido"
    if "," in name:
        parts = [p.strip() for p in name.split(",", 1)]
        if len(parts) == 2 and parts[0] and parts[1]:
            name = f"{parts[1]} {parts[0]}"

    # 3. Remueve acentos y convierte ñ -> n via transliteración ASCII
    name = unidecode(name)

    # 4. Eliminar caracteres especiales no alfanuméricos (mantener letras y espacios)
    name = re.sub(r"[^A-Za-z\s]", " ", name)

    # 6. Convertir a mayúsculas (antes de filtrar ruido para comparar con el set)
    name = name.upper()

    # 5. Remover palabras clave de ruido
    words = name.split()
    words = [w for w in words if w not in NOISE_WORDS]

    # Unir y eliminar espacios redundantes
    name = " ".join(words)

    return name


def check_identity_match(name_a: str, name_b: str) -> bool:
    """Compara dos nombres usando igualdad estricta tras la limpieza.

    Args:
        name_a: Primer nombre a comparar.
        name_b: Segundo nombre a comparar.

    Returns:
        True si ambos nombres son idénticos después de estandarizarlos.
    """
    return standardize_name(name_a) == standardize_name(name_b)
