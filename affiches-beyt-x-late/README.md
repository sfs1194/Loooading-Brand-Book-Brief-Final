# BEŶT & CO ✕ LATE — affiches recto / verso

Deux affiches A1 pour les panneaux devant le magasin. Recto et verso d'un même
message, construites sur les **assets officiels BEŶT** récupérés dans le Drive.
Tout est vectoriel : les fichiers montent en A0 sans perdre un poil de netteté.

## Le parti pris

Les affiches de départ posaient logos et icônes au même poids visuel, sur des
rayures pleine page : de loin, ni hiérarchie, ni lecture de la collaboration.
Et elles ne montraient que **BEŶT**, pas **BEŶT & CO**.

Contrainte forte : **ne jamais écrire ce qui est servi.** Ce sont donc les
**noms** qui portent l'affiche, et les **tasses** qui disent le reste. Chaque
côté fait un seul travail :

| | Fond | Encre | Rôle | Lecture |
|---|---|---|---|---|
| **Recto** | Tomate | Crème | les noms | BEŶT & CO ✕ LATE |
| **Verso** | Bleu | Tomate | les objets | LATE — chez — BEŶT & CO |

Le recto est mené par la maison hôte, le verso par l'invité : même système,
hiérarchie inversée, couleurs permutées. Les deux côtés portent les deux noms,
parce qu'un passant n'en voit qu'un seul à la fois.

## Assets utilisés (tous officiels)

| Élément | Fichier d'origine |
|---|---|
| Logo BEŶT | `2026-08-26-BEYT-Logo-Officiel-Vectorise-Tomate-v01.svg` |
| Tampon « & CO » | `2026-09-04-BEYT-Tampon-Ovale-Beyt-And-Co-Vectorise-v01.svg` |
| Icône tasse | `2026-08-20-BEYT-Icone-Tasse-Vectorisee-Noir-v01.svg` |
| Icône tasse thé-sfenj | `2026-08-25-BEYT-Icone-Tasse-The-Sfenj-Vectorisee-Noir-v01.svg` |
| Logo LATE | revectorisé depuis les affiches d'origine (`source/late/`) |

Le sous-titre du logo LATE a été retiré : il nomme ce qui est servi.

## Palette

| | | |
|---|---|---|
| Tomate | `#E82613` | rouge officiel BEŶT |
| Crème | `#F7EFDC` | le papier |
| Bleu | `#C3E9FB` | le bleu LATE, repris des affiches d'origine |

## Typographie

Deux familles, pas trois. Les logos ne sont jamais retapés.

- **Italiana** — l'esprit fin et déco du logo BEŶT
- **Archivo** — surtitres et mentions, en capitales espacées

## Fichiers

```
affiches/pdf/…-A1.pdf                 format final, 594 × 841 mm
affiches/pdf/…-A1-fonds-perdus.pdf    604 × 851 mm — la version pour l'imprimeur
affiches/png/…png                     aperçus 1600 px
affiches/svg/…-A1.svg                 sources vectorielles, éditables dans Illustrator
```

Les PDF ne contiennent **aucune image matricielle** : logos, icônes et textes
sont tous en courbes, donc aucune police à fournir à l'imprimeur.

## Refabriquer les fichiers

```bash
cd source
pip install cairosvg fonttools
python3 build.py        # → ../affiches/{pdf,png,svg}
```

`source/kit2.py` contient la boîte à outils (palette, chargement des assets
BEŶT, placement, croix de collaboration, texte converti en courbes). Une
affiche = un fichier (`recto.py`, `verso.py`), en millimètres.

`source/late/vectorize.py` ne sert qu'à régénérer le logo LATE si sa source
change (il demande en plus `pillow`, `numpy`, `potracer`).

Les polices sont sous licence SIL Open Font (Google Fonts), redistribuables.

## À compléter si besoin

Les affiches ne portent volontairement **ni horaires, ni adresse, ni comptes
Instagram** — je n'avais pas ces informations. La ligne du bas de chaque
affiche est prévue pour ça (`Archivo-Medium`, bas de `recto.py` / `verso.py`).
