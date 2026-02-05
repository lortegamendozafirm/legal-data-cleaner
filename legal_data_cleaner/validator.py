"""Funciones de validación para verificar si un dato ya está limpio."""

import re

from .constants import NOISE_WORDS


def is_clean_name(name: str) -> bool:
    """Verifica si un nombre ya cumple con el estándar canónico.

    Criterios:
        - Solo contiene caracteres ASCII (A-Z y espacios).
        - Está en mayúsculas.
        - No tiene espacios redundantes (extremos ni internos).
        - No contiene palabras de ruido.

    Args:
        name: El nombre a validar.

    Returns:
        True si el nombre ya está en formato canónico.
    """
    if not name or not isinstance(name, str):
        return False

    # Verificar que no tiene espacios en los extremos
    if name != name.strip():
        return False

    # Verificar que está en mayúsculas
    if name != name.upper():
        return False

    # Verificar que solo contiene letras ASCII y espacios
    if not re.match(r"^[A-Z\s]+$", name):
        return False

    # Verificar que no tiene espacios redundantes
    if "  " in name:
        return False

    # Verificar que no contiene palabras de ruido
    words = set(name.split())
    if words & NOISE_WORDS:
        return False

    return True


def is_ascii_safe(text: str) -> bool:
    """Verifica si el texto contiene solo caracteres ASCII.

    Args:
        text: Texto a verificar.

    Returns:
        True si todos los caracteres son ASCII.
    """
    try:
        text.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False
