"""
FASE E — 2028 (BISIESTO)

Reutiliza el builder parametrizado.
Valida específicamente el 29 de febrero de 2028.
"""

from datetime import date as dateclass
from .premium_phase_c import build_year

if __name__ == '__main__':
    result = build_year(2028)

    # Validación adicional para año bisiesto
    print("\n[BISIESTO CHECK]")
    try:
        d28 = dateclass(2028, 2, 28)
        d29 = dateclass(2028, 2, 29)
        d1m = dateclass(2028, 3, 1)
        print(f"  28/02/2028: {d28} [OK]")
        print(f"  29/02/2028: {d29} [OK]")
        print(f"  01/03/2028: {d1m} [OK]")

        # Verificar que el PDF incluya el 29
        feb_pages = [p for p in result.get('_pages', []) if p.get('month') == 2]
        if any(p.get('day_num') == 29 for p in feb_pages):
            print("  29/02/2028 presente en PDF: [OK]")
        else:
            print("  ALERTA: 29/02/2028 no encontrado en PDF")
    except ValueError as e:
        print(f"  ERROR: {e}")
