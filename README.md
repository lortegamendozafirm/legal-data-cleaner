# legal-data-cleaner ⚖️

**Estandarización de Identidad para Datos Legales.** Esta librería es el núcleo de normalización de datos para el equipo de **Eficiencia Operativa**. Su objetivo es transformar nombres de clientes provenientes de diversas fuentes (ClickUp, MyCase, 8x8, Dropbox) en un formato canónico apto para **Machine Learning** y resolución de entidades.

## 🚀 Propósito

En procesos legales con miles de registros, la inconsistencia en los nombres (acentos, eñes, metadatos manuales) genera duplicidad y errores de trazabilidad. `legal-data-cleaner` garantiza que:

1. **"Peña, José (Visa T)"** y **"JOSE PENA"** sean reconocidos como la misma entidad.
2. Los datos sean compatibles con sistemas legacy (ASCII).
3. Se elimine el "ruido" legal que no pertenece a la identidad del cliente.

## 🛠️ Instalación

Puedes instalar la librería directamente desde el repositorio de GitHub:

```bash
pip install git+https://github.com/lortegamendozafirm/legal-data-cleaner.git

```

## 📖 Uso Rápido

### Normalización de Nombres

```python
from legal_data_cleaner import standardize_name

raw_name = "  Peña, José (Lead Visa T) "
clean_name = standardize_name(raw_name)

print(clean_name)  
# Output: "JOSE PENA"

```

### Validación de Datos

```python
from legal_data_cleaner import is_clean_name

print(is_clean_name("JOSE PENA"))      # True
print(is_clean_name("Jose Peña"))      # False (No es ASCII/Upper)

```

### Integración con Polars (Procesamiento Masivo)

```python
import polars as pl
from legal_data_cleaner import standardize_name

df = pl.read_csv("leads.csv")
df = df.with_columns(
    pl.col("Nombre").map_elements(standardize_name, return_dtype=pl.String).alias("Nombre_Limpio")
)

```

## 📋 Estándar de Limpieza

La librería aplica las siguientes transformaciones en orden:

1. **Trim:** Elimina espacios en los extremos.
2. **Regex-Clean:** Elimina contenido entre paréntesis `(...)`.
3. **Format-Fix:** Detecta el formato `Apellido, Nombre` y lo invierte a `Nombre Apellido`.
4. **Transliteración:** Convierte caracteres especiales a ASCII (ej: `ñ` -> `n`, `á` -> `a`).
5. **Sanitización:** Elimina caracteres no alfanuméricos.
6. **Noise-Filter:** Remueve palabras irrelevantes definidas en `constants.py` (LEAD, VISA, PENDING, etc.).
7. **Upper:** Todo el resultado se entrega en Mayúsculas.

## 👥 Equipo

Desarrollado por el Departamento de Eficiencia Operativa para la integración de microservicios en **GCP**, **Modal** y flujos **Locales**.

---
