# Sans Python

Si ni `python3`, ni `python`, ni `py -3` ne répondent, la saisie et la capture fonctionnent quand
même : tu fais le calcul avec la commande `date` et tu remplis le gabarit toi-même. L'option
« export » n'est alors pas disponible.

## Le calcul, avec les mêmes règles que le script

Dans cet ordre, sans rien calculer de tête :

1. Ranger les dates de la plus récente à la plus ancienne et garder les sept plus récentes.
2. Pas d'estimation sous trois dates, sauf si une durée habituelle entre 15 et 60 jours est donnée.
3. Calculer chaque intervalle entre deux dates voisines. Si l'un sort de 15 à 60 jours, pas
   d'estimation (il manque peut-être une date, ou il y en a une de trop). Si l'écart entre le plus
   court et le plus long dépasse sept jours, pas d'estimation non plus : c'est un seuil de l'outil,
   pas un avis médical, et tu ne dis jamais de son cycle qu'il est « irrégulier », « anormal »,
   « inhabituel » ou « en retard ».
4. Moyenne des intervalles, arrondie au jour le plus proche (un demi-jour vers le haut).
5. Date estimée = date la plus récente + moyenne. Début de la fenêtre = date estimée moins le délai
   (de 1 à 14 jours ; absent ou hors de ces bornes, 3).
6. Avant le début : `avant_fenetre`. Du début à la date estimée comprise : `dans_fenetre`. Après :
   `date_estimee_passee`.

Les commandes :

- La date du jour : `date +%F` (sous PowerShell, `Get-Date -Format yyyy-MM-dd`).
- Un intervalle sous Linux ou Git Bash :
  `echo $(( ($(date -u -d 2026-09-14 +%s) - $(date -u -d 2026-08-16 +%s)) / 86400 ))`
- Sur Mac, chaque date en secondes : `date -u -j -f '%Y-%m-%d %H:%M:%S' '2026-09-14 00:00:00' +%s`
- Sous PowerShell : `(New-TimeSpan -Start '2026-08-16' -End '2026-09-14').Days`
- Le jour de la semaine de la date estimée, en chiffre (1 = lundi, 7 = dimanche) :
  `date -d 2026-10-13 +%u` (Linux, Git Bash), `date -j -f %Y-%m-%d 2026-10-13 +%u` (Mac),
  `[int](Get-Date '2026-10-13').DayOfWeek` (PowerShell, où 0 = dimanche). Même commande pour aujourd'hui
  et pour le début de la fenêtre ; une semaine va du lundi au dimanche. Préfère le chiffre au nom du jour, qui dépend
  de la langue du système.
- Pour l'annonce (« Préparer le mot », étape 1) : `jours_avant_date_estimee` est l'intervalle entre
  aujourd'hui et la date estimée (commande ci-dessus) ; `jour_date_estimee` est le chiffre de la date
  estimée ; pour `semaine_date_estimee`, prends u, le chiffre d'aujourd'hui (sous PowerShell, 0
  devient 7) : `cette_semaine` si jours_avant ≤ 7 − u, `semaine_prochaine` si jours_avant ≤ 14 − u,
  sinon `dans_deux_semaines`. Sous Linux, Mac ou Git Bash, `echo $(( 7 - $(date +%u) ))` donne la
  première borne.
- La moyenne arrondie, sans calcul de tête : `echo $(( (2 * 57 + 2) / (2 * 2) ))` sous Linux, Mac
  ou Git Bash (deux fois la somme des intervalles, plus leur nombre, divisé par deux fois leur
  nombre) ; sous PowerShell, `[math]::Floor((2 * 57 + 2) / (2 * 2))`.
- Retirer des jours (le délai) : même commande qu'ajouter, avec `-3 days`, `-v-3d` ou `AddDays(-3)`.
- Ajouter des jours : `date -d '2026-09-14 +29 days' +%F` (Linux),
  `date -j -v+29d -f %Y-%m-%d 2026-09-14 +%Y-%m-%d` (Mac),
  `(Get-Date '2026-09-14').AddDays(29).ToString('yyyy-MM-dd')` (PowerShell).

## Remplir le gabarit à la main

1. Copier `assets/templates/<ambiance>.html` et `.txt` dans `~/.ca-arrive/mots/`, sous les noms
   `mot-<ambiance>.html` et `mot-<ambiance>.txt`.
2. Remplacer `{{OBJET}}` et `{{TITRE}}` par l'objet (« Ça arrive. Prépare-toi. » par défaut),
   `{{SALUTATION}}`, `{{ANNONCE}}` et `{{SIGNATURE}}` par ses textes, et `{{OUVERTURE}}`,
   `{{APRES_MOTS}}`, `{{MERCI}}`, `{{FIN}}` et `{{APERCU}}` par les phrases de l'ambiance, lues dans
   `assets/templates/phrases.json` (ou celles qu'elle a choisies à leur place), et `{{MOT_PERSO}}` par
   sa phrase à elle.
3. Répéter le bloc compris entre `<!--CASES-->` et `<!--/CASES-->` pour chaque ligne de la liste à
   cocher (`{{CASE}}`), et de même le bloc `<!--MOT-->` pour chaque mot interdit (`{{MOT}}`).
4. Retirer entièrement le bloc `<!--CHECKLIST-->`, `<!--MOTS_INTERDITS-->`, `<!--MOT_PERSO-->`,
   `<!--OUVERTURE-->`, `<!--APRES_MOTS-->`, `<!--MERCI-->` ou `<!--FIN-->` s'il est vide, titre
   compris.
5. Dans le `.html`, écrire `&amp;`, `&lt;` et `&gt;` à la place de `&`, `<` et `>` dans ses textes.
6. Retirer le commentaire « Gabarit » en tête du fichier et tous les marqueurs `<!--...-->` restants,
   qui s'afficheraient tels quels dans la version texte, puis vérifier qu'il ne reste ni `{{` ni
   `<!--` (hors du `<head>` du `.html`).

## Le brouillon mis en page sans Python

Une fois le `.html` rempli (ci-dessus), sur un Mac : l'ouvrir dans Safari, puis bouton Partager (ou
Fichier > Partager), Mail : Mail ouvre un nouveau message avec la page, au format « Page web », qui
garde la mise en page (aide d'Apple, lue le 25/09/2026 :
https://support.apple.com/fr-fr/guide/safari/sfri40722/mac). C'est elle qui le fait, pas toi. Hors
Mac, ou si ça ne marche pas, donne la version texte, à copier.

## Ajouter une date sans Python

Écris-la en tête de « # Dates », au format AAAA-MM-JJ, jamais postérieure à celle que donne
`date +%F`, sans doublon, sept au plus (retire la plus
ancienne au-delà). Si cette date est à sept jours ou moins d'une date déjà notée, c'est la même période :
demande-lui lequel était le premier jour, et ne garde que celui-là.
