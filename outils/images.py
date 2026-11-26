"""Prépare les images du site AGS (photos fournies et images IA).

Usage, depuis la racine du projet :   python outils/images.py

- Photos du client : assetsAGS/  → assets/img/ags/<nom>.webp   (table PHOTOS ci-dessous)
- Images IA (Gemini) : déposer dans images-ia/ avec le nom attendu
  (accueil-banniere, accueil-banniere-alt, service-<slug>)  → assets/img/ia/<nom>.webp
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

RACINE = Path(__file__).resolve().parent.parent
PHOTOS = {
    'WhatsApp Image 2026-11-26 at 11.11.49.jpeg': 'bureau-responsable-1',
    'WhatsApp Image 2026-11-26 at 11.11.50 (1).jpeg': 'bureau-responsable-2',
    'WhatsApp Image 2026-11-26 at 11.11.50 (2).jpeg': 'bureau-responsable-2b',
    'WhatsApp Image 2026-11-26 at 11.11.50 (3).jpeg': 'siege-facade',
    'WhatsApp Image 2026-11-26 at 11.11.50.jpeg': 'bureau-responsable-3',
    'WhatsApp Image 2026-11-26 at 11.11.51 (1).jpeg': 'equipe-terrain-2',
    'WhatsApp Image 2026-11-26 at 11.11.51.jpeg': 'equipe-terrain',
    'TEAM.jpeg': 'equipe',
}
EXTENSIONS = {'.png', '.jpg', '.jpeg', '.jfif', '.webp'}


def convertir(source, sortie, taille):
    im = ImageOps.exif_transpose(Image.open(source)).convert('RGB')
    im.thumbnail((taille, taille), Image.LANCZOS)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    im.save(sortie, 'WEBP', quality=82, method=6)
    print(f'{source.name:48} → {sortie.relative_to(RACINE)}  ({sortie.stat().st_size // 1024} Ko)')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    for nom, cible in PHOTOS.items():
        f = RACINE / 'assetsAGS' / nom
        if f.exists():
            convertir(f, RACINE / 'assets/img/ags' / f'{cible}.webp', 1600)
    ia = RACINE / 'images-ia'
    if ia.is_dir():
        for f in sorted(ia.iterdir()):
            if f.suffix.lower() in EXTENSIONS:
                nom = f.stem.lower()
                convertir(f, RACINE / 'assets/img/ia' / f'{nom}.webp', 2400 if nom.startswith('accueil-') else 1600)


if __name__ == '__main__':
    main()
