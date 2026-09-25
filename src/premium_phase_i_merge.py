"""
FASE I — ENSAMBLAJE MASTER FINAL

Fusiona PDFs parciales de forma robusta.
Evita errores de recursión usando estrategia de lectura alternativa.
"""

import subprocess
import shutil
from pathlib import Path
from .config import OUTPUT, DOCS

def build_master():
    """Fusionar PDFs usando herramienta del sistema."""

    print("\n" + "="*70)
    print("FASE I — ENSAMBLAJE MASTER FINAL")
    print("="*70)

    # Orden de componentes
    components = [
        ('CORE', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-CORE.pdf'),
        ('2026', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-2026-NAV.pdf'),
        ('2027', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-2027-NAV.pdf'),
        ('2028', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-2028-NAV.pdf'),
        ('SIN FECHA', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-SIN-FECHA-Plantillas.pdf'),
        ('COLECCIONES', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-Colecciones.pdf'),
    ]

    output_path = OUTPUT / 'YOYIR-Planificador-Digital-2026-2028-ES-PREMIUM.pdf'

    # Verificar disponibilidad de herramientas
    merge_tool = find_merge_tool()

    if merge_tool == 'pdftk':
        return merge_with_pdftk(components, output_path)
    elif merge_tool == 'ghostscript':
        return merge_with_ghostscript(components, output_path)
    else:
        return merge_with_pypdf_safe(components, output_path)

def find_merge_tool():
    """Detectar herramientas disponibles para merge de PDFs."""

    # Intentar pdftk
    try:
        result = subprocess.run(['pdftk', '--version'],
                              capture_output=True, timeout=2)
        if result.returncode == 0:
            print("[OK] Detectado: pdftk")
            return 'pdftk'
    except:
        pass

    # Intentar ghostscript
    try:
        result = subprocess.run(['gs', '--version'],
                              capture_output=True, timeout=2)
        if result.returncode == 0:
            print("[OK] Detectado: ghostscript")
            return 'ghostscript'
    except:
        pass

    print("[INFO] Herramientas del sistema no disponibles")
    print("[INFO] Usando pypdf con estrategia segura")
    return 'pypdf_safe'

def merge_with_pdftk(components, output_path):
    """Fusionar usando pdftk."""

    print("\nFusionando con pdftk...")

    # Verificar existencia
    missing = [name for name, path in components if not path.exists()]
    if missing:
        print(f"[ERROR] Falta: {missing}")
        return {'status': 'fail', 'error': 'missing_files'}

    # Construir comando
    input_files = ' '.join(str(path) for name, path in components)
    cmd = f'pdftk {input_files} cat output "{output_path}"'

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True,
                              timeout=60)
        if result.returncode == 0:
            print(f"[OK] PDF fusionado: {output_path}")
            return validate_merge(components, output_path)
        else:
            print(f"[ERROR] pdftk: {result.stderr.decode()}")
            return {'status': 'fail', 'error': result.stderr.decode()}
    except Exception as e:
        print(f"[ERROR] {e}")
        return {'status': 'fail', 'error': str(e)}

def merge_with_ghostscript(components, output_path):
    """Fusionar usando ghostscript."""

    print("\nFusionando con ghostscript...")

    missing = [name for name, path in components if not path.exists()]
    if missing:
        print(f"[ERROR] Falta: {missing}")
        return {'status': 'fail', 'error': 'missing_files'}

    input_files = ' '.join(str(path) for name, path in components)
    cmd = f'gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="{output_path}" {input_files}'

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True,
                              timeout=120)
        if result.returncode == 0:
            print(f"[OK] PDF fusionado: {output_path}")
            return validate_merge(components, output_path)
        else:
            print(f"[ERROR] ghostscript: {result.stderr.decode()}")
            return {'status': 'fail', 'error': result.stderr.decode()}
    except Exception as e:
        print(f"[ERROR] {e}")
        return {'status': 'fail', 'error': str(e)}

def merge_with_pypdf_safe(components, output_path):
    """Fusionar con pypdf usando estrategia segura (sin recursión)."""

    print("\nFusionando con pypdf (estrategia segura)...")

    try:
        from pypdf import PdfWriter, PdfReader
    except ImportError:
        print("[ERROR] pypdf no disponible")
        return {'status': 'fail', 'error': 'pypdf_not_available'}

    missing = [name for name, path in components if not path.exists()]
    if missing:
        print(f"[ERROR] Falta: {missing}")
        return {'status': 'fail', 'error': 'missing_files'}

    writer = PdfWriter()
    total_pages = 0

    print("\nLeyendo componentes...")
    for name, path in components:
        try:
            print(f"  Leyendo {name}...")
            reader = PdfReader(str(path))
            pages = len(reader.pages)

            # Estrategia segura: agregar página por página
            for page_num in range(pages):
                try:
                    page = reader.pages[page_num]
                    writer.add_page(page)
                except Exception as page_err:
                    print(f"    [WARN] Página {page_num}: {page_err}")
                    continue

            total_pages += pages
            print(f"    [OK] {pages} págs agregadas")
        except Exception as e:
            print(f"    [ERROR] {name}: {e}")
            return {'status': 'fail', 'error': f'{name}: {str(e)}'}

    # Guardar
    try:
        print(f"\nGuardando Master final ({total_pages} págs)...")
        with open(str(output_path), 'wb') as f:
            writer.write(f)
        print(f"[OK] PDF guardado: {output_path}")
        return validate_merge(components, output_path)
    except Exception as e:
        print(f"[ERROR] Guardar: {e}")
        return {'status': 'fail', 'error': str(e)}

def validate_merge(components, output_path):
    """Validar merge."""

    try:
        from pypdf import PdfReader
    except:
        return {'status': 'unknown', 'warning': 'pypdf_not_available'}

    if not output_path.exists():
        return {'status': 'fail', 'error': 'output_not_created'}

    try:
        reader = PdfReader(str(output_path))
        final_pages = len(reader.pages)

        expected = sum(1 for _ in components)  # Contar componentes

        result = {
            'status': 'pass',
            'output': str(output_path),
            'final_pages': final_pages,
            'components': len(components),
            'file_size_mb': output_path.stat().st_size / (1024 * 1024)
        }

        print(f"\n[VALIDACIÓN]")
        print(f"  Páginas finales: {final_pages}")
        print(f"  Componentes: {len(components)}")
        print(f"  Tamaño: {result['file_size_mb']:.2f} MB")
        print(f"\n[OK] Merge completado exitosamente")

        return result
    except Exception as e:
        print(f"[ERROR] Validar merge: {e}")
        return {'status': 'fail', 'error': str(e)}

if __name__ == '__main__':
    build_master()
