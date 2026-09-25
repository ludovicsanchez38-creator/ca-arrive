# Donner ses dates par l'export de son appli

Ce fichier complète `SKILL.md` pour la troisième façon de donner ses dates. L'agent le suit pas à
pas, selon l'appli de l'utilisatrice. Les chemins `<skill>/...` partent du dossier du skill. Tout ce
qui est décrit ici vient des pages d'aide des éditeurs, lues le 25/09/2026, avec leur adresse ; ce
qui n'a pas pu être vérifié est dit comme tel.

## Le principe, quelle que soit l'appli

Cette façon n'est proposée que si l'agent tourne sur l'ordinateur de l'utilisatrice. Dans le cloud
(Cowork, par défaut), sur un serveur ou par une messagerie, il faudrait lui envoyer l'export entier :
l'agent l'explique et propose la saisie ou la capture.

Un export contient bien plus que des dates : toutes les données de santé dans le cas d'Apple, ou
tout ce qui a été noté dans l'appli. L'agent ne l'ouvre donc **jamais** avec son outil de lecture. Le
script `scripts/dates_cycle.py` le lit sur l'ordinateur et n'affiche que les premiers jours des règles, sept
au plus : ce sont les seules données qui passent par le modèle d'IA, en général dans le cloud.

Ensuite, toujours dans cet ordre :

1. L'agent montre la liste affichée et demande à l'utilisatrice de la comparer avec son appli. Un
   export peut contenir une date oubliée ou en trop, et la lecture des formats non documentés (Clue,
   Flo) reste une lecture de bonne foi.
2. Seules les dates qu'elle confirme vont dans `reglages.md`.
3. L'agent lui rappelle de mettre l'export à la corbeille, puis de la vider : ce fichier contient
   bien plus que ce dont le skill a besoin. Même chose sur son téléphone, s'il y est resté.

Pour transférer un fichier du téléphone vers l'ordinateur, un câble, ou AirDrop en gardant les deux
appareils côte à côte jusqu'à la fin du transfert, valent mieux que l'e-mail ou un service de
stockage en ligne : le fichier ne passe alors par aucun serveur (si l'on s'éloigne pendant un
transfert AirDrop, Apple indique qu'il continue par Internet :
https://support.apple.com/fr-fr/guide/iphone/iphcd8b9f0af/ios ; le réglage Réglages > Général >
AirDrop > « Utiliser les données cellulaires », une fois désactivé, lui interdit au moins le réseau
mobile).

Si Python manque sur l'ordinateur, cette option n'est pas disponible : l'agent propose la saisie ou
la capture.

## Apple Santé (iPhone)

### L'export complet, lu par le script

Apple documente l'export de toutes les données de Santé au format XML : dans l'app Santé, toucher
**Résumé**, puis sa photo ou ses initiales, puis **« Exporter toutes les données Santé »**, et choisir
une méthode de partage.
Source : https://support.apple.com/fr-fr/guide/iphone/iph5ede58c3d/ios (section « Partager des
données de santé et de forme au format XML »).

L'iPhone produit en principe une archive `.zip` (Apple ne le précise pas sur la page lue). Une fois
sur l'ordinateur :

```bash
python3 "<skill>/scripts/dates_cycle.py" apple <chemin de l'archive .zip ou du fichier .xml>
```

Le script cherche les enregistrements de flux menstruel que la documentation développeur d'Apple
décrit (`HKCategoryTypeIdentifierMenstrualFlow`, avec la clé `HKMetadataKeyMenstrualCycleStart` qui
marque le début d'un cycle), ignore les jours notés « sans flux », regroupe les jours en périodes et
n'affiche que le premier jour de chacune. Sur un gros export (plusieurs gigaoctets), l'agent
lance la commande avec un délai long, dix minutes par exemple : la lecture peut dépasser une minute.
Sources : https://developer.apple.com/documentation/healthkit/hkcategorytypeidentifier/menstrualflow
et https://developer.apple.com/documentation/healthkit/hkmetadatakeymenstrualcyclestart

**Ce qui n'a pas été vérifié** : Apple ne décrit pas, sur les pages lues, la structure exacte du
fichier exporté ni le nom de l'archive. Le script a été testé sur des fichiers fabriqués selon la
structure connue de cet export, pas sur un export réel. D'où l'étape 1 : comparer avec l'appli.

**Par où passent les données** : l'export complet reste sur l'ordinateur ; seules les dates
affichées par le script passent par le modèle d'IA. Côté Apple, les données de Santé synchronisées
avec iCloud sont chiffrées de bout en bout, avec l'identification à deux facteurs et un code sur
l'appareil (sources : https://support.apple.com/fr-fr/120356, le tableau de
https://support.apple.com/fr-fr/102651, et pour la condition du code
https://support.apple.com/guide/security/advanced-data-protection-for-icloud-sec973254c5f/web).

### Le PDF de l'historique des cycles, lu comme une capture

Apple documente aussi un export plus léger : dans l'app Santé, toucher **Rechercher**, puis **Suivi
de cycle**, faire défiler jusqu'à **Vos cycles**, toucher **Historique des cycles**, puis **« Exporter
au format PDF »** pour les douze derniers mois.
Source : https://support.apple.com/fr-fr/120356 (section « Consulter et exporter l'historique de
votre cycle »).

Ce PDF n'est pas lu par le script : l'agent le lit comme une capture d'écran, et tout son contenu
passe donc par le modèle d'IA. À réserver à qui préfère cette simplicité, en sachant
que le PDF peut contenir d'autres informations notées dans l'app.

## Clue

### L'export de Clue, lu par le script

Clue documente la demande de copie des données : dans l'appli, menu **« = »** en haut à droite de
la vue du cycle, **Settings**, **Download my data**, **Request data**. Un mot de passe s'affiche (à
copier), et un e-mail arrive à l'adresse du compte Clue avec un lien de téléchargement valable
72 heures. Le fichier est une archive `.zip` protégée par ce mot de passe, qui contient un fichier
JSON avec les données suivies et les réglages de l'appli.
Source : https://support.helloclue.com/hc/en-us/articles/17320910724125-How-do-I-get-a-copy-of-my-Clue-data
(page consultée le 25/09/2026).

L'utilisatrice décompresse elle-même l'archive avec ce mot de passe, puis :

```bash
python3 "<skill>/scripts/dates_cycle.py" json <chemin du fichier .json>
```

**Ce qui n'a pas été vérifié** : Clue ne décrit pas le contenu de ce fichier JSON. Le script y
cherche des dates associées aux règles et écarte ce qui ressemble à une prévision ou à la fenêtre
fertile ; il a été testé sur des fichiers fabriqués, pas sur un export réel de Clue. Si le script
ne trouve rien, ou si la liste ne correspond pas à l'appli, revenir à la saisie ou à la capture.

**Par où passent les données** : le lien arrive par e-mail, et le fichier passe par les serveurs de
Clue puis par la messagerie de l'utilisatrice avant d'arriver sur son ordinateur. Seules les dates
affichées par le script passent ensuite par le modèle d'IA.

### Par Apple Santé, sur iPhone

Clue documente aussi une synchronisation de ses données de règles et de flux vers Apple Santé :
dans Clue, **Settings**, **Apple Health**, **Go to Settings**, puis dans les réglages de l'iPhone,
**Santé**, **Accès aux données et appareils**, **Clue**, et donner l'autorisation. Seules les règles
notées après cette autorisation sont transmises : l'historique n'est pas importé, et Clue suggère de
supprimer puis de ressaisir les anciennes dates pour qu'elles passent.
Source : https://support.helloclue.com/hc/en-us/articles/20199556038813-Can-I-export-my-data-from-Clue-to-Apple-Health-or-Apple-Health-to-Clue
(page consultée le 25/09/2026). Les libellés des réglages de l'iPhone sont traduits de cette page en
anglais et peuvent différer légèrement à l'écran.

Une fois la synchronisation faite, suivre la partie Apple Santé ci-dessus.

## Flo

### La copie des données, lue par le script

Flo documente une copie des données sur demande : dans l'appli, toucher son avatar (Menu), **Help**,
faire défiler jusqu'à **Contact us**, et envoyer un message qui demande l'export. Flo propose deux
formats : un fichier texte (TXT), lisible par un humain, et un fichier JSON, fait pour être lu par
un programme. En mode anonyme, il faut d'abord enregistrer son compte.
Source : https://help.flo.health/hc/en-us/articles/360054973811-How-do-I-get-a-copy-of-my-data
(page consultée le 25/09/2026).

Demander le **JSON**, puis :

```bash
python3 "<skill>/scripts/dates_cycle.py" json <chemin du fichier .json>
```

**Ce qui n'a pas été vérifié** : la page de Flo ne précise ni le moyen d'envoi du fichier ni le
délai, et Flo ne décrit pas le contenu du JSON. Le script a été testé sur des fichiers fabriqués,
pas sur un export réel de Flo. Même règle : comparer avec l'appli, et revenir à la saisie ou à la
capture si la liste ne correspond pas.

**Par où passent les données** : la demande passe par le support de Flo, et le fichier par le moyen
que Flo choisit. Seules les dates affichées par le script passent ensuite par le modèle d'IA.

### Pas de passage par Apple Santé

Flo indique que les règles notées dans Flo ne sont pas envoyées à l'app Santé : la voie Apple ne
marche donc pas pour Flo.
Source : https://help.flo.health/hc/en-us/articles/34890229122068-How-to-import-data-from-the-Health-app-to-Flo-iOS
(page consultée le 25/09/2026).

Sur Android, Flo documente un appairage avec Health Connect
(https://help.flo.health/hc/en-us/articles/34890469974292-How-to-pair-Flo-with-Health-Connect-Android),
mais aucun chemin pour en sortir les dates vers un ordinateur n'a été vérifié pour ce skill.

## Un raccourci automatique sur iPhone (pour les plus à l'aise)

**Cette recette n'a pas été testée sur un iPhone.** Elle assemble des briques qu'Apple documente :

- l'action **« Rechercher des échantillons de Santé »** de l'app Raccourcis
  (https://support.apple.com/fr-fr/guide/shortcuts/apd3c845e881/ios) ;
- les filtres, le tri et la limite de ces actions
  (https://support.apple.com/guide/shortcuts/add-filter-parameters-apdbdab3433f/ios) ;
- les automatisations déclenchées à une heure donnée, dont certaines peuvent s'exécuter sans
  demander de confirmation (https://support.apple.com/guide/shortcuts/create-a-new-personal-automation-apdfbdbd7123/ios).

Le principe : un raccourci qui recherche les échantillons de Santé du type menstruations, triés du
plus récent au plus ancien et limités à une soixantaine, en extrait la date de début au format
AAAA-MM-JJ, et enregistre la liste dans un fichier texte. Le choix du type « menstruations » dans le
filtre n'est pas détaillé sur les pages lues : suivre ce que propose l'écran. Sur l'ordinateur :

```bash
python3 "<skill>/scripts/dates_cycle.py" liste <chemin du fichier texte>
```

Le script regroupe les jours en périodes et n'affiche que les premiers jours.

**Par où passent les données, et c'est le point à peser** : pour que le fichier arrive tout seul sur
l'ordinateur, il faut l'enregistrer dans iCloud Drive. Or, d'après Apple, iCloud Drive n'est chiffré
de bout en bout qu'avec la **protection avancée des données** ; en protection standard, qui est le
réglage par défaut, Apple garde les clés de chiffrement. Les données de Santé, elles, sont chiffrées
de bout en bout dans les deux modes, dès lors que l'identification à deux facteurs et un code sont
activés : le raccourci les en fait donc sortir.
Sources : https://support.apple.com/fr-fr/102651 (version française publiée le 08/01/2026) et
https://support.apple.com/guide/security/advanced-data-protection-for-icloud-sec973254c5f/web.

D'où le conseil : n'automatiser vers iCloud Drive que si la protection avancée des données est
activée ; sinon, lancer le raccourci à la main, garder le fichier sur l'iPhone et le transférer par
AirDrop ou par câble.
