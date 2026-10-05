# Atelier Zellije — The Zellijist × Morocco Design (Flexform)

Livrables pour les deux sessions supplémentaires de l'atelier :
**mardi 6 octobre · 12:00** et **mercredi 7 octobre · 15:00**, showroom Flexform, Casablanca.
DA reprise de Morocco Design (vert `#2D5E37`, or `#D6B53F`, blanc, grotesque étendue en capitales).

| Fichier | Rôle |
|---|---|
| `visuels/zellijist-atelier-post-1080x1350.png` | Post Instagram 4:5 |
| `visuels/zellijist-atelier-story-1080x1920.png` | Story Instagram 9:16 (zones de sécurité respectées) |
| `visuels/caption.txt` | Légende du post + consignes story |
| `visuels/post.html`, `visuels/story.html` | Sources éditables → `node visuels/render.cjs` pour regénérer les PNG |
| `index.html`, `inscrits.html`, `assets/` | Page de réservation + récap (copie de travail ; la version en ligne est dans le repo `the-zellijist-site`, dossier `flexform/`) |
| `apps-script/Code.gs` | Service Apps Script : le Google Sheet est la base des inscriptions |

## Mise en ligne sur thezellijist.com (Vercel)

La page est dans le repo `sfs1194/the-zellijist-site` : `flexform/index.html` (→ thezellijist.com/flexform),
`flexform/inscrits.html` (récap) et `api/atelier.js` (fonction Vercel). Même architecture que le visualiser :
le navigateur ne parle qu'à `api/atelier.js`, qui relaie vers Apps Script avec un secret.

1. Ouvrir le classeur **Flexform zellijist waitlist** (celui de la liste du lundi).
2. **Extensions → Apps Script**, coller `apps-script/Code.gs`. Ajuster `capacity` des sessions si besoin.
3. **Paramètres du projet → Propriétés du script** : `SECRET` (longue chaîne aléatoire) et `ADMIN_KEY` (mot de passe du récap).
4. Exécuter `setup` une fois (autoriser l'accès) → crée les feuilles **Mardi 6 oct · 12h** et **Mercredi 7 oct · 15h**. La feuille du lundi n'est pas touchée.
5. **Déployer → Nouveau déploiement → Application Web** — Exécuter en tant que : *Moi* ; Accès : *Tout le monde*. Copier l'URL `…/exec`.
6. Sur Vercel (projet the-zellijist-site → Settings → Environment Variables) :
   `ATELIER_SCRIPT_URL` = l'URL `…/exec`, `ATELIER_SECRET` = la valeur de `SECRET`. Redéployer.
7. Tester : ouvrir thezellijist.com/flexform, faire une réservation, la voir dans la feuille du jour et sur /flexform/inscrits.html, puis la passer en « Annulé ».

En local (fichier, localhost) ou avec `?demo` dans l'URL, la page tourne en **mode démo** (inscriptions dans le navigateur seulement).

### Fonctionnement
- Compteur de places en direct par session ; une session pleine passe en « Complet » automatiquement.
- Verrou côté Apps Script : impossible de dépasser la capacité, même avec des inscriptions simultanées.
- Doublon email/session refusé ; 1 ou 2 places par inscription ; champ piège anti-robots ; limite de cadence par IP.
- Email de confirmation au participant.
- Annuler / pointer un participant : colonne **Statut** de la feuille du jour (Confirmé / Présent / Annulé) → une place annulée est libérée.
- Code Apps Script modifié : **Déployer → Gérer les déploiements → Modifier → Nouvelle version** (l'URL ne change pas).

## Logos
Tous sur fond transparent, dans `assets/logos/` :
- Morocco Design : `morocco-design.svg`, converti du PDF vectoriel officiel (or `#E6AC03`, repris comme or de la DA).
- The Zellijist : `the-zellijist-blanc.png`, logo du site recadré et passé en blanc.
- Flexform : `flexform.png`, logo original fourni (cadre rouge compris), simplement recadré ; profil couleur Display P3 d'origine conservé.
- Saad Filali Studio : logo retiré des visuels et de la page (demande du 5 octobre).

Après un changement de logo dans les visuels : `node visuels/render.cjs`.
