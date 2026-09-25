"""
Merge alternativo: Concatenación de streams PDF.
Estrategia: Leer cada PDF como stream y escribir bytes directos.
"""

from pathlib import Path

def concatenate_pdfs_binary(components, output_path):
    """Concatenar PDFs como streams binarios (más robusto)."""

    print("[MERGE ALTERNATIVO: Concatenación de Streams]")

    with open(output_path, 'wb') as outfile:
        # Escribir header PDF
        outfile.write(b'%PDF-1.4\n')

        offset = len(b'%PDF-1.4\n')
        xref_offsets = []

        for name, path in components:
            print(f"  Leyendo {name}...")

            with open(path, 'rb') as infile:
                content = infile.read()

                # Saltar header PDF de archivos subsecuentes
                if components.index((name, path)) > 0:
                    # Encontrar '%' que marca inicio de objeto
                    start = content.find(b'%')
                    if start > 0:
                        content = content[start:]

                outfile.write(content)
                offset += len(content)
                xref_offsets.append(offset)

    print(f"[OK] PDF concatenado: {output_path}")
    print(f"[INFO] Tamaño: {output_path.stat().st_size / (1024*1024):.2f} MB")

    # Validar
    from pypdf import PdfReader
    try:
        reader = PdfReader(output_path)
        print(f"[OK] Archivo válido: {len(reader.pages)} páginas")
    except Exception as e:
        print(f"[WARN] Validación: {e}")

if __name__ == '__main__':
    from ..config import OUTPUT

    components = [
        ('CORE', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-CORE.pdf'),
        ('2026', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-2026-NAV.pdf'),
        ('2027', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-2027-NAV.pdf'),
        ('2028', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-2028-NAV.pdf'),
        ('SIN FECHA', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-SIN-FECHA-Plantillas.pdf'),
        ('COLECCIONES', OUTPUT / 'premium-build-tests' / 'YOYIR-Premium-Colecciones.pdf'),
    ]

    output = OUTPUT / 'YOYIR-Planificador-Digital-2026-2028-ES-PREMIUM-ALT.pdf'

    concatenate_pdfs_binary(components, output)
