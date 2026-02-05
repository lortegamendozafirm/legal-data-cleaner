"""legal-data-cleaner: Estandarización de identidad para datos legales."""

from .cleaner import check_identity_match, standardize_name
from .validator import is_ascii_safe, is_clean_name

__version__ = "1.0.0"
__all__ = [
    "standardize_name",
    "check_identity_match",
    "is_clean_name",
    "is_ascii_safe",
]
