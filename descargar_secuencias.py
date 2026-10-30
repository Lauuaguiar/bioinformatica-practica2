"""Descarga de UniProt el citocromo c de cinco especies y lo guarda en data/citocromo_c.fasta.

El FASTA ya está incluido en el repositorio; este script solo hace falta para regenerarlo.
"""

from pathlib import Path
from urllib.request import urlopen

# Especie -> accesión de UniProt (Swiss-Prot, revisadas)
ESPECIES = {
    "Humano": "P99999",      # CYC_HUMAN, Homo sapiens
    "Chimpance": "P99998",   # CYC_PANTR, Pan troglodytes
    "Raton": "P62897",       # CYC_MOUSE, Mus musculus
    "Pez_cebra": "Q6IQM2",   # CYC_DANRE, Danio rerio
    "Mosca": "P84029",       # CYC2_DROME, Drosophila melanogaster (Cyt-c-p, la forma somática)
}

SALIDA = Path(__file__).resolve().parent / "data" / "citocromo_c.fasta"


def descargar(accesion):
    url = f"https://rest.uniprot.org/uniprotkb/{accesion}.fasta"
    with urlopen(url) as respuesta:
        return respuesta.read().decode()


def main():
    SALIDA.parent.mkdir(exist_ok=True)
    registros = []
    for especie, accesion in ESPECIES.items():
        cabecera, *lineas = descargar(accesion).strip().splitlines()
        # Ponemos la especie como ID para que SeqIO la use directamente como etiqueta
        registros.append(f">{especie} {cabecera[1:]}\n" + "\n".join(lineas))
        print(f"{especie:<10} {accesion}  {len(''.join(lineas))} aa")
    SALIDA.write_text("\n".join(registros) + "\n")
    print(f"\nGuardado en {SALIDA}")


if __name__ == "__main__":
    main()
