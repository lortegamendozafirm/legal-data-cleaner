"""Diccionarios de palabras de ruido a eliminar durante la estandarización."""

# Palabras clave que se consideran ruido y deben ser removidas del nombre.
# Incluye términos legales, de estado de caso y metadatos manuales.
NOISE_WORDS = {
    "LEAD",
    "VISA",
    "PROCESADO",
    "CLIENTE",
    "CASO",
    "CASE",
    "NEW",
    "NUEVO",
    "PENDING",
    "PENDIENTE",
    "CLOSED",
    "CERRADO",
    "ACTIVE",
    "ACTIVO",
}
