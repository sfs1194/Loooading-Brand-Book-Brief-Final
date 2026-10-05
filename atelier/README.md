# Atelier Zellige — The Zellijist × Morocco Design (Flexform)

Livrables pour les deux sessions supplémentaires de l'atelier :
**mardi 6 octobre · 12:00** et **mercredi 7 octobre · 15:00**, showroom Flexform, Casablanca.
DA reprise de Morocco Design (vert `#2D5E37`, or `#D6B53F`, blanc, grotesque étendue en capitales).

| Fichier | Rôle |
|---|---|
| `visuels/zellijist-atelier-post-1080x1350.png` | Post Instagram 4:5 |
| `visuels/zellijist-atelier-story-1080x1920.png` | Story Instagram 9:16 (zones de sécurité respectées) |
| `visuels/caption.txt` | Légende du post + consignes story |
| `visuels/post.html`, `visuels/story.html` | Sources éditables → `node visuels/render.cjs` pour regénérer les PNG |
| `index.html` | Page de réservation (à publier sur `thezellijist.com/atelier`) |
| `inscrits.html` | Récap des inscrits (protégé par clé, export CSV, impression) |
| `apps-script/Code.gs` | Backend : Google Sheet = base des inscriptions |

## Mise en ligne des réservations (≈ 5 min)

1. Créer un Google Sheet « Inscriptions atelier zellige ».
2. Menu **Extensions → Apps Script**, coller le contenu de `apps-script/Code.gs`.
3. Ajuster en haut du fichier : `capacity` de chaque session, `ADMIN_KEY` (mot de passe du récap), `NOTIFY_EMAIL` (optionnel).
4. Exécuter la fonction `setup` une fois (autoriser l'accès) → crée les onglets **Inscriptions** et **Récap**.
5. **Déployer → Nouveau déploiement → Application Web** — Exécuter en tant que : *Moi* ; Accès : *Tout le monde*. Copier l'URL `…/exec`.
6. Coller cette URL dans `const API_URL = ''` de `index.html` **et** de `inscrits.html`.
7. Publier le dossier `atelier/` (avec `assets/` et `visuels/`) sur thezellijist.com/atelier.

Tant que `API_URL` est vide, la page fonctionne en **mode démo** (bandeau jaune, inscriptions stockées dans le navigateur seulement).

### Fonctionnement
- Compteur de places en direct par session ; une session pleine passe en « Complet » automatiquement.
- Verrou côté serveur : impossible de dépasser la capacité, même avec des inscriptions simultanées.
- Doublon email/session refusé ; 1 ou 2 places par inscription ; champ anti-spam caché.
- Email de confirmation au participant (via le compte Google du Sheet).
- Annuler / pointer un participant : colonne **Statut** du Sheet (Confirmé / Présent / Annulé) → la place annulée est libérée.
- Si le code Apps Script est modifié : **Déployer → Gérer les déploiements → Modifier → Nouvelle version** (l'URL reste la même).

## Logos
Les logos sont des wordmarks typographiques provisoires (`.logo-*` dans `assets/brand.css`).
Pour les remplacer par les fichiers officiels (Morocco Design, The Zellijist, Saad Filali Studio, Flexform) :
déposer les SVG dans `assets/logos/` et remplacer le contenu des `<span class="logo …">` par `<img>`, puis relancer `node visuels/render.cjs`.
