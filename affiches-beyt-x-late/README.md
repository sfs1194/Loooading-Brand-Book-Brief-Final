# BEŶT ✕ LATE — affiches de collaboration

Trois affiches A1 pour les panneaux devant le magasin, refaites à partir des
deux originaux. Tout est vectoriel : les fichiers montent en A0 (ou plus) sans
perdre un poil de netteté.

## Ce qui a changé par rapport aux originaux

Les affiches de départ posaient les logos et les icônes un peu partout, tous au
même poids visuel : de loin, on ne lisait ni la hiérarchie, ni le fait qu'il
s'agit d'une collaboration.

| Problème | Correction |
|---|---|
| Logos flottants, sans lien entre eux | Un vrai lockup **BEŶT ✕ LATE** — la croix dit « collaboration » d'un coup d'œil |
| Aucun message | Une phrase claire par affiche : LATE est le coffee shop, il est chez BEŶT |
| Icônes éparpillées au hasard | Icônes rangées : socle de l'arche, angles, bandeau — elles cadrent au lieu de brouiller |
| Rayures sur toute la surface, rien ne respire | Une zone calme (arche ou bandeau crème) réservée au lockup, rayures autour |
| Tout à plat, sans hiérarchie | Trois niveaux : surtitre → lockup → message → mention pratique |

L'arche est le fil rouge de la série : **BEŶT (بيت) veut dire « maison »**, donc
le seuil d'une porte. Affiche 1, l'arche est claire sur fond rayé ; affiche 3,
elle est rayée sur fond crème — même motif, inversé.

## Les trois affiches

| # | Fond | Rôle | Message |
|---|---|---|---|
| 01 — collaboration | orange rayé | l'annonce | « LE CAFÉ, À LA MAISON » |
| 02 — invitation | bleu rayé | l'accroche de rue | « ON PREND UN CAFÉ ? » |
| 03 — deux maisons | crème | la signature | « DEUX MAISONS, UNE SEULE ADRESSE » |

Elles fonctionnent seules comme en série. Pour deux panneaux seulement, prendre
01 et 02 : l'annonce puis l'invitation.

## Fichiers

```
affiches/pdf/…-A1.pdf                 format final, 594 × 841 mm
affiches/pdf/…-A1-fonds-perdus.pdf    604 × 851 mm — la version à envoyer à l'imprimeur
affiches/png/…png                     aperçus 1600 px (réseaux, validation)
affiches/svg/…-A1.svg                 sources vectorielles, éditables dans Illustrator
```

Les PDF ne contiennent **aucune image matricielle** : logos, icônes et textes
sont tous en courbes, donc aucune police à fournir à l'imprimeur.

## Palette

Reprise au pixel près des originaux.

| | |
|---|---|
| Orange | `#F55000` |
| Orange rayure | `#F97A37` |
| Bleu | `#C3E9FB` |
| Bleu rayure | `#E2F2F9` |
| Crème | `#F7EFDC` |

## Typographie

Les logos BEŶT et LATE ne sont jamais retapés : ce sont les lettrages d'origine,
vectorisés. Pour le reste :

- **Italiana** — les phrases en capitales, dans l'esprit fin et déco de BEŶT
- **Anton** — l'accroche de l'affiche 02, dans l'esprit massif du « MATCHA + COFFEE »
- **Archivo** — les mentions pratiques

## Refabriquer les fichiers

```bash
cd source
pip install pymupdf pillow numpy potracer cairosvg fonttools
python3 vectorize.py   # logos PNG → courbes (shapes.json) — à refaire seulement si un logo change
python3 build.py       # → ../affiches/{pdf,png,svg}
```

`source/kit.py` contient la boîte à outils (palette, rayures peintes, arche,
croix, placement des icônes, texte converti en courbes). Une affiche = un
fichier `p1.py` / `p2.py` / `p3.py`, en millimètres, faciles à retoucher.

Les polices sont sous licence SIL Open Font (Google Fonts), redistribuables.

## À compléter si besoin

Les affiches ne portent volontairement **ni horaires, ni adresse, ni comptes
Instagram** — je n'avais pas ces informations. Pour en ajouter, la ligne du bas
de chaque affiche est prévue pour ça (`Archivo-Medium`, bas de `p1.py`,
`p2.py`, `p3.py`).
