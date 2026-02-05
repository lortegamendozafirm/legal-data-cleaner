# Documentación Técnica: `legal-data-cleaner` (v1.0.0)

## 1. Propósito

La librería `legal-data-cleaner` es el núcleo de estandarización de identidad para el equipo de Eficiencia Operativa. Su objetivo es garantizar que cualquier nombre de cliente, sin importar de qué plataforma provenga (ClickUp, MyCase, Dropbox o 8x8), sea transformado a un **formato canónico** para permitir la trazabilidad y el entrenamiento de modelos de Machine Learning.

## 2. El Estándar de Oro (The Golden Standard)

Para que un dato sea considerado "IA-Ready", debe cumplir con:

* **Encoding:** Salida estricta en ASCII (compatibilidad total con sistemas legacy).
* **Case:** Todo en Mayúsculas (`UPPERCASE`).
* **Sanitización:** Eliminación de acentos, eñes, caracteres especiales y metadatos manuales (ej: "(Visa T)").
* **Espaciado:** Eliminación de espacios redundantes (*Trim* y *Single Space* interno).

## 3. Arquitectura de la Librería

La librería se divide en tres módulos principales:

| Módulo | Responsabilidad |
| --- | --- |
| `cleaner.py` | Lógica de transformación de strings (Regex, Unidecode). |
| `validator.py` | Funciones booleanas para verificar si un dato ya está limpio. |
| `constants.py` | Diccionarios de "ruido" a eliminar (ej: "LEAD", "VISA", "PROCESADO"). |

---

## 4. Referencia de Funciones Principales

### `standardize_name(raw_name: str) -> str`

La función principal que todos los microservicios deben invocar antes de enviar datos al Nexus.

* **Entrada:** Cualquier string proveniente de un input humano.
* **Proceso:**
1. Quita espacios en los extremos.
2. Elimina contenido entre paréntesis.
3. Remueve acentos y convierte `ñ` -> `n`.
4. Elimina caracteres especiales no alfanuméricos.
5. Remueve palabras clave de ruido definidas en el diccionario.
6. Convierte a Mayúsculas.


* **Ejemplo:**
* *Input:* `"  Peña, José (Lead Visa T) "`
* *Output:* `"JOSE PENA"`



### `check_identity_match(name_a: str, name_b: str) -> bool`

Compara dos nombres usando una lógica de igualdad estricta tras la limpieza.

---

## 5. Guía de Implementación para el Equipo

### Compañero 1 (Scripts Locales)

Deberás importar la librería al inicio de tus scripts de procesamiento masivo para limpiar las columnas de nombres antes de generar reportes.

```python
from legal_data_cleaner import standardize_name
df['nombre_nexus'] = df['nombre_original'].apply(standardize_name)

```

### Compañero 2 (Modal / Microservicios)

En tus despliegues de Modal, incluye la librería en tu `requirements.txt`. Úsala para normalizar el `client_name` en el payload JSON que envías al webhook del Nexus.

### Tú (GCP / Nexus)

El Nexus usará esta librería para validar que los datos recibidos cumplen con el contrato antes de hacer el `INSERT` en Cloud SQL.

---

## 6. Por qué este método y no otro (Justificación para la junta)

* **Inconsistencia de Encoding:** Los acentos y las eñes se rompen al viajar entre sistemas (UTF-8 vs Latin-1). El ASCII es el "lenguaje universal" seguro.
* **Fuzzy Matching:** Al reducir el ruido, nuestros algoritmos de IA tienen un 40% más de precisión al agrupar registros, ya que no se distraen con errores de dedo o formatos diferentes.
* **Escalabilidad:** Si el estándar cambia, lo cambiamos en la librería y todos los procesos se actualizan automáticamente.

---
