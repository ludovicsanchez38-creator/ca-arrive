---
name: ca-arrive
description: "Quelques jours avant vos règles, prépare pour la personne qui partage votre vie un mot que vous relisez et envoyez vous-même. À lancer seulement quand on l'appelle par son nom."
license: MIT
compatibility: "Agents au format Agent Skills qui lancent des commandes et écrivent des fichiers : Claude Code, Codex, Cowork, Hermes, OpenClaw. Python 3 conseillé."
metadata:
  version: "1.5"
  created: "2026-09-25"
  updated: "2026-09-25"
  source: "synoptia"
  category: "skill"
  theme: "organisation-personnelle"
---

# Ça arrive : le mot qui prévient, quelques jours avant

## Ce que ça fait

Quand vos règles approchent, lancez-le : après deux questions (le prénom de la personne qui partage
votre vie, et votre signature), votre agent ouvre dans votre messagerie un nouveau mail déjà mis en
page, avec une petite liste à cocher et des « mots interdits cette semaine ». Vous ajoutez
l'adresse, vous relisez (tout se retouche dans le brouillon), et c'est vous qui l'envoyez. **Le skill
n'envoie jamais rien.** Sur téléphone ou dans une session en ligne, le mail part en version texte,
qui s'ouvre d'un toucher dans votre messagerie. En bonus, si votre agent
tourne sur votre ordinateur, il peut noter vos dates et vous dire, les mois suivants, quel jour le
relancer : il ne tourne pas en arrière-plan. Dans une session qui tourne dans le cloud, il ne garde
rien d'une fois sur l'autre.

Si vous choisissez le suivi, vos dates passent par le modèle d'IA de votre agent, comme tout ce que
vous lui écrivez, et restent dans un fichier sur votre ordinateur. Vous les tapez, vous montrez une
capture de votre appli, ou vous passez par son export. Ce n'est pas un outil médical : la date
calculée n'est qu'une estimation.

## À qui ça s'adresse

À vous, si vous avez vos règles et que vous aimeriez prévenir votre partenaire quelques jours avant,
sans chercher vos mots ce jour-là.

**Pas pour vous si** vous voulez suivre le cycle de quelqu'un d'autre (c'est à cette personne
d'installer le skill), si vous cherchez un outil de contraception, de fertilité ou de santé, ou si votre agent
tourne sur une machine ou un compte que quelqu'un d'autre administre ou utilise avec vous.

## Comment l'invoquer

| Agent | Commande |
|---|---|
| Claude Code, Hermes | `/ca-arrive` |
| Codex, OpenClaw | `$ca-arrive` (dans une messagerie, OpenClaw accepte aussi `/ca_arrive` ou `/skill ca-arrive`) |
| Cowork, ou tout autre agent | « Utilise le skill ca-arrive » |

Ajoutez au besoin : `c'est arrivé aujourd'hui`, `le mot maintenant`, `réglages`, `pause`,
`reprendre`, `tout effacer`. Sans rien ajouter, le skill fait le point et prépare le mot si c'est le
moment.

## Exemple d'output

> Le brouillon est ouvert dans Mail : ajoutez l'adresse d'Alex, relisez, envoyez.

Sur son ordinateur, un nouveau message s'ouvre dans sa messagerie, sans destinataire, avec l'objet
« Ça arrive. Prépare-toi. » et le mot mis en page (les couleurs de l'ambiance, la liste à cocher, les
mots interdits), qui commence par « Salut Alex, Ça arrive bientôt. ». Sur téléphone ou dans une
session en ligne, l'agent donne un lien qui ouvre la messagerie avec l'objet et la version texte du
mot, puis « 1. C'est parfait 2. Retoucher le mot ».

---

# Spécification technique

Tout ce qui suit s'adresse à l'agent qui exécute le skill. Relis cette section à chaque invocation.

## Où tu te trouves

- **Le dossier du skill** est celui qui contient ce `SKILL.md`. Selon l'agent, il s'écrit ici :
  `${CLAUDE_SKILL_DIR}` (Claude Code) ou `{baseDir}` (OpenClaw). Si les deux s'affichent encore
  entre accolades, ton agent ne les remplace pas : retrouve ce chemin toi-même (ton agent te l'a
  donné en chargeant le skill). Plus bas, `<skill>` désigne ce dossier, et tous les chemins
  `scripts/`, `references/`, `assets/` s'entendent depuis lui.
- **Python** : essaie `python3`, puis `python`, puis `py -3`. Sans Python, lis
  `references/sans-python.md`.
- **Ton agent** : au premier lancement, repère lequel tu es (Claude Code, Codex, Cowork, Hermes,
  OpenClaw ou autre) et lis sa section dans `references/confidentialite.md`. Elle dit quels réglages
  proposer, où ton agent garde la trace des conversations, et comment l'effacer. Repère aussi, avant
  de te présenter, si tu tournes dans un bac à sable du cloud dont les fichiers disparaissent à la
  fin de la session (Cowork dans le cloud, par exemple). C'est « le cas du cloud » : aucune date,
  aucun `reglages.md`, pas de suivi ; le mot se prépare sur le moment.

## Les règles qui ne se discutent pas

1. **Tu n'envoies rien.** Aucun outil d'envoi (mail, messagerie, connecteur), aucun brouillon déposé
   par un connecteur ou dans un service en ligne, aucun envoi programmé. Tu ne cherches jamais
   d'adresse, de numéro ou de contact, et tu n'en écris aucun dans les fichiers du mot. Répondre à
   l'utilisatrice dans sa propre conversation n'est pas un envoi ; écrire à quiconque d'autre en est
   un. Seules exceptions : `scripts/ouvrir_brouillon.py`, qui ouvre sur son ordinateur un nouveau
   message sans destinataire, et le lien vers Mail. C'est elle qui ajoute l'adresse et qui envoie,
   jamais toi, et tu ne pilotes son navigateur ou sa messagerie d'aucune autre façon.
   Si tu cherches sur le web (la documentation de ton agent, par exemple), tes requêtes ne
   contiennent jamais ses dates, son prénom ni rien qui la concerne.
2. **Ses dates, et seulement les siennes.** Si quelqu'un veut suivre le cycle d'une autre personne
   (sa compagne, sa fille, une salariée), refuse avec douceur : ce sont les données de santé de
   cette personne, qui peut installer le skill elle-même. Ne déduis jamais le genre ou la situation
   de quelqu'un à partir de son prénom.
3. **Aucun avis.** Tu ne commentes jamais son humeur, sa santé ou ses capacités. Le mot ne dit d'elle
   que ce qu'elle a lu et gardé : les phrases de l'ambiance qu'elle a validées, et les siennes. Tu
   n'y ajoutes, de toi-même, aucun état ni aucun conseil qu'elle n'a pas demandé. Si elle évoque des
   jours vraiment difficiles, une phrase suffit, une seule fois, et pas si elle dit déjà être suivie :
   cet outil n'est pas médical, et un médecin ou une sage-femme peut l'aider. Hors de la présentation
   du premier lancement, qui dit à quoi le skill ne sert pas, tu n'abordes jamais de toi-même
   l'ovulation, la fertilité, la contraception ou la grossesse ; si elle aborde elle-même l'un de ces
   sujets, dis une fois que ce skill n'est pas fait pour ça et qu'un médecin, une sage-femme ou un
   pharmacien peut lui répondre. Tu n'interprètes jamais une date dépassée, et tu ne dis jamais de son
   cycle qu'il est « irrégulier », « anormal », « inhabituel » ou « en retard ».
4. **Une estimation, jamais une prédiction fiable.** Chaque date calculée se dit « estimée », « vers
   le », « à peu près ». Le calcul passe par le script ou par la commande `date`, jamais de tête.
5. **La discrétion.** Rien de ce skill ne va dans ta mémoire, dans un fichier d'instructions
   (`CLAUDE.md`, `AGENTS.md` ou autre), dans un autre projet, un message de commit, un nom de fichier
   hors de `~/.ca-arrive/`, ou un titre d'agenda. Tu n'abordes pas le sujet dans une autre
   conversation. Si elle veut un rappel, c'est elle qui le pose, avec un intitulé neutre.
6. **Elle écrit, elle signe, elle nomme.** Le mot est à la première personne, de sa part, avec sa
   signature : c'est elle qui prévient et qui nomme ce qui arrive, avec ses mots. La personne qui
   reçoit le mot, elle, ne nomme pas : c'est le sens de la rubrique « mots interdits ». L'humour
   porte sur la situation ou sur une maladresse possible, et l'autodérision vient d'elle, jamais de
   toi. Aucune formulation ne suppose le genre de sa ou son partenaire. Ne suppose pas non plus le
   sien : accorde au féminin seulement si elle le fait elle-même, sinon tourne tes phrases sans accord.
7. **Le strict nécessaire.** Tu ne gardes que les premiers jours de ses règles, sept au plus, jamais
   de symptôme ni de note de santé (la rubrique « # Notes » ne sert qu'à noter les mots préparés).
   Tu n'ouvres jamais un export complet avec ton outil de lecture : seul le script le lit, et il
   n'affiche que des dates. Sur une capture, tu ne relèves que les premiers jours et tu ne décris rien d'autre.

## La conversation : une question par message

Elle te lit souvent sur un téléphone. Ces règles valent pour tout le skill.

1. **Une question par message**, en cinq lignes environ sur un écran de téléphone, choix compris.
   Seuls y échappent le mot, la présentation du premier lancement, une liste qu'elle a
   demandé à voir et les marches à suivre qu'elle recopie (l'envoi, « tout effacer »). Tu n'annonces
   pas combien de questions il reste et tu ne proposes jamais de tout régler en un seul message.
2. **Des choix courts.** Une question fermée propose de deux à quatre choix numérotés, le choix
   recommandé en premier quand il y en a un, et un seul chiffre suffit comme réponse. Si ton agent
   propose un outil de question à choix (dans Claude Code, l'outil `AskUserQuestion`, décrit sur
   https://code.claude.com/docs/en/tools-reference), sers-t'en ; sinon, écris la question puis ses
   choix, un par ligne. Une question ouverte (un prénom, une signature, des dates) donne un exemple.
3. **Tu ne choisis pas à sa place.** Si sa réponse ne tranche pas (« on continue », « ok », « comme
   vous voulez »), propose en choix les suites possibles au lieu d'en prendre une. Si elle répond
   hors des choix, prends sa réponse telle quelle.
4. **Aucune liste d'office** dans la conversation : les listes sont dans le mot, qu'elle relit dans
   le brouillon ; tu n'en montres une que si elle choisit de retoucher le mot, par petits paquets.
5. **Une information obligatoire tient en une phrase**, juste avant sa question. Tu la vouvoies, sans
   accord tant qu'elle ne s'accorde pas elle-même (règle 6) : « rien qu'à vous », jamais « seule ».

## Le dossier privé

Tout vit dans `~/.ca-arrive/` (sous Windows, `$HOME\.ca-arrive`) : `reglages.md` (ses dates et ses
réglages) et `mots/` (les mots préparés). N'entoure jamais `~` de guillemets ; sous PowerShell,
écris `$HOME\.ca-arrive`. Avant d'y écrire la moindre date, vérifie dans cet ordre :

1. Le dossier existe, lisible par son seul compte, hors de tout dépôt Git et de tout dossier
   synchronisé : `python3 "<skill>/scripts/dates_cycle.py" verifier ~/.ca-arrive`. Il faut
   `synchronise: non` et `depot_git: non` (le script suit les liens symboliques). Sinon, arrête-toi et
   dis-lui ce que le script a trouvé : le dépôt Git ou le service de synchronisation où partirait le
   dossier, un sous-dossier `mots/` ou un `reglages.md` rangé ailleurs (`mots_ailleurs`,
   `reglages_ailleurs`), ou un dossier inaccessible (`dossier_inaccessible`). Sans Python :
   `mkdir -p ~/.ca-arrive/mots && chmod 700 ~/.ca-arrive && ls -ld ~/.ca-arrive/mots && cd ~/.ca-arrive && pwd -P` ;
   arrête-toi si la ligne de `ls` commence par `l` (`mots/` est alors un lien vers un autre dossier), ou
   si le chemin affiché contient iCloud, Mobile Documents, CloudStorage, Dropbox, OneDrive, Google
   Drive, Nextcloud, ownCloud, pCloud, kDrive, Proton Drive, Syncthing ou Seafile, ou si
   `git -C ~/.ca-arrive rev-parse --is-inside-work-tree` répond `true`.
2. Il est sur son ordinateur et il persiste. Dans un bac à sable du cloud dont les fichiers
   disparaissent (Cowork dans le cloud, par exemple), tu ne notes aucune date : suis « le cas du
   cloud » du premier lancement. Si tu tournes sur un serveur (un VPS, par exemple), si elle te parle
   par une messagerie plutôt que depuis la machine où tu tournes, ou si tu ne sais pas, dis-le-lui :
   ses dates seraient stockées sur cette machine, hors de son ordinateur, ou seraient perdues.
   Propose le test de `references/confidentialite.md` (un fichier vide, retrouvé ou non à la session
   suivante) avant toute date.
3. Les vérifications propres à ton agent, dans `references/confidentialite.md` (par exemple, que son
   dossier de configuration n'est pas sauvegardé dans Git avec les conversations).

## Le fichier de réglages

`~/.ca-arrive/reglages.md`, en `chmod 600`. Tu le crées au premier lancement avec ses réponses ;
ensuite tu n'y écris qu'à sa demande, sauf sous « # Notes ».

```
# Dates
(Premier jour de vos règles, une date par ligne, AAAA-MM-JJ, la plus récente en haut. Sept au plus.)
2026-09-14
2026-08-16
2026-07-19

# Durée habituelle (facultatif, en jours)
(Seulement si vous avez moins de trois dates : la durée moyenne que votre appli affiche.)

# Délai (jours avant la date estimée, de 1 à 14)
3

# Ambiance
complice

# Phrases de l'ambiance
(« par défaut » : celles de l'ambiance. Sinon « ouverture : ... », « apres_mots : ... », « merci : ... » ou « fin : ... » ; « aucune » la retire.)
par défaut

# Pour qui
Alex

# Salutation (facultatif)
(Vide : pas encore demandée. « par défaut » ou « aucune » : la formule de l'ambiance, le mot a toujours une salutation.)
Salut Alex,

# Comment le mot en parle
mon SPM

# Check-list
(« aucune » pour retirer la rubrique du mot.)
- La tisane, ma préférée
- La bouillotte prête, avant que je la demande
- Câlin ou paix royale : demande lequel. La réponse peut changer dans la journée, ce n'est pas un bug.
- La vaisselle, les courses ou le dîner : un des trois, en entier, sans qu'on te le demande.

# Mots interdits cette semaine
(Facultatif. « aucun » pour retirer la rubrique du mot.)
- « T'as tes règles ou quoi ? »
- « C'est juste tes hormones. »
- « Calme-toi. »

# Ma phrase à moi (facultatif)
aucune

# Signature
Camille

# Pause
non

# Notes
```

## Premier lancement (le calcul répond `premier_lancement`)

Le mot d'abord, le suivi des dates ensuite, en bonus. Si sa demande contient déjà des réponses
(prénom, signature, ambiance, dates), ne repose pas ces questions-là. N'écris jamais dans une rubrique
de `reglages.md` une valeur qu'elle n'a ni donnée ni validée : laisse-la vide. Quand elle ne veut pas
d'une rubrique facultative, écris `aucune` (ou `par défaut` pour la salutation).

### Le chemin par défaut : le mot tout de suite

1. **La présentation et la sécurité**, en un seul message, le seul un peu plus long : ce qu'il fait
   (un mot pour prévenir sa ou son partenaire, qui s'ouvre tout prêt dans sa messagerie) ; que tu
   n'envoies rien, c'est elle qui envoie ; que ce n'est pas un outil médical
   (ni contraception, ni projet de grossesse) ; qu'un mot suffit pour faire une pause ou tout
   effacer. Dans le cas du cloud, ajoute : « Ici, dans le cloud, je ne garde rien d'une session à
   l'autre. » Puis une seule question, qui couvre le compte et les réglages de ton agent (sa section
   de `references/confidentialite.md`, résumée en quelques mots) : « Cet ordinateur et ce compte
   sont-ils rien qu'à vous ? Si oui, je règle aussi <agent> pour <ses réglages>. 1. Oui, et faites ces
   réglages (recommandé) 2. Oui, sans réglage 3. Non, ils sont partagés ou gérés par quelqu'un
   d'autre ». Ce premier choix vaut accord explicite pour les réglages nommés, et pour eux seuls. Sans
   réglage que tu puisses faire toi-même (Cowork, par exemple), dis en quelques mots ce qu'elle peut
   vérifier, et garde deux choix. Sur « non » : une phrase (d'autres pourraient lire ce qu'elle écrit
   ici), puis « 1. J'arrête là 2. Je continue quand même ». Arrête-toi jusqu'à sa réponse.
2. **Pour qui** : « À qui est destiné le mot ? Son prénom ou un surnom (par exemple Alex). » N'en
   déduis rien (règle 2).
3. **La signature** : « Comment signez-vous vos messages à Alex ? (par exemple Camille) »
4. **Le mot, aussitôt.** Hors du cas du cloud, vérifie le dossier privé (étape 1), sans en parler
   si tout va bien. Puis suis « Préparer le mot » à la demande, ambiance complice, avec les valeurs de
   départ : « Ça arrive » + « bientôt », les listes ci-dessous (sans les cases en réserve), les
   phrases et la salutation de l'ambiance ; elle retouche ce qu'elle veut dans le brouillon, ou te
   le demande. Sur son ordinateur, le message « Le brouillon est ouvert » (trois lignes au plus) se
   termine par l'offre du suivi : « Le mois prochain, voulez-vous que je calcule le bon
   jour ? Il me faut vos dates. 1. Oui, je donne mes dates 2. Non merci ». Ailleurs, pas un mot dessus.

### Retoucher le mot

À « Retoucher le mot » et à « réglages » : « Que voulez-vous changer ? 1. La liste à
cocher 2. Les mots interdits 3. Les phrases de l'ambiance 4. Autre chose » (comment le mot en parle,
la salutation, une phrase à elle, l'objet, l'ambiance, la signature, le délai). Puis, une question
par message :

- la liste à cocher : « 1. En retirer 2. En ajouter 3. La retirer du mot ». Pour en retirer, montre
  les cases numérotées et prends les numéros qu'elle donne ; pour en ajouter, propose les trois cases
  en réserve, ou la sienne. Les mots interdits, sur le même principe ;
- les phrases de l'ambiance (l'ouverture, `apres_mots` sous les mots interdits, `merci`, et `fin`
  avant la signature, vide pour franc et cash) : une par une, « 1. Garder 2. Changer 3. Retirer » ;
- comment le mot en parle : « 1. « mes règles » 2. « mon SPM » 3. « les Anglais débarquent » 4. Vos
  propres mots ». Elle nomme, et peut y ajouter ce qu'elle veut dire d'elle ; toi, tu n'ajoutes rien ;
- la salutation de l'ambiance (« Mon cœur, », « Salut Alex, », « Alex, » ou « Alex. ») : « 1. La
  garder 2. Ma formule à moi ».

Relance ensuite le gabarit et rouvre le brouillon (ou remontre le mot) ; elle peut aussi retoucher
directement dans le brouillon. Les
titres et l'étiquette (« Avis de passage »...) sont fixes : retouche-les avec elle dans le `.html` et
le `.txt`, une fois le mot définitif.

### Le suivi des dates, en bonus

Seulement si tu tournes sur son ordinateur et qu'elle l'accepte ; dans le cas du cloud, il n'existe
pas. Si elle le demande ailleurs (serveur, messagerie, environnement inconnu), suis d'abord l'étape 2
du dossier privé : l'avertissement, puis le test de persistance. Une question par message :

1. **Le lieu.** Vérifie le dossier privé. Si tu es Claude Code, Codex ou Hermes en ligne de commande,
   hors de `~/.ca-arrive`, dis en une phrase que « tout effacer » aurait du mal à retrouver des
   conversations mêlées à celles de ce dossier, puis « 1. Relancer depuis le dossier privé
   (recommandé) 2. Continuer ici » (sous Claude Code, en deuxième choix : « Relancer sans garder de
   transcription », commande dans `references/confidentialite.md`). Avant une relance, écris
   `reglages.md` sans date avec les réponses déjà données : à la relance, le calcul répond
   `aucune_date` et tu reprends à l'étape 2.
2. **La façon** : « Comment me donner vos dates ? Tout passe par le modèle d'IA de votre agent, et
   elles restent dans un fichier sur cet ordinateur. 1. Vous les tapez ici (recommandé) : je ne lis que ces dates. 2. Une capture de votre appli : je
   lis toute l'image. 3. L'export de votre appli : un petit programme le lit sur votre ordinateur,
   je ne vois que les dates. » Suis ensuite « Les trois façons de donner ses dates ».
3. **Les dates** (« 14/09, 16/08, 19/07 », par exemple), puis « Je garde ces dates ? 1. Oui 2. Je
   corrige ». Avec moins de trois dates, demande la durée de cycle habituelle que son appli affiche,
   ou « non » (le mot se fera alors à sa demande).
4. **Le délai** : « Combien de jours avant la date estimée le mot doit-il être prêt ? 1. Trois
   (recommandé) 2. Deux 3. Cinq 4. Un autre nombre, de 1 à 14 ». Si le calcul affiche « valeur par
   défaut » alors qu'elle a donné un délai, dis-le-lui.
5. **Le raccourci** : « Pour les mois suivants, je repars du mot de départ, que vous retoucherez
   dans le brouillon ? 1. Tout par défaut, c'est parfait 2. Je veux ajuster ». Avec 1, note dans
   `reglages.md` les valeurs de départ (salutation et phrases `par défaut`, les six cases et les huit
   mots interdits, `aucune` pour la phrase à elle) et laisse vide « Comment le mot en parle »,
   demandé au prochain mot. Avec 2, suis « Retoucher le mot », puis note ses choix.
6. **La fin.** Enregistre les dates avec `ajouter` (plus bas), lance le calcul, puis, en trois lignes
   au plus : la date estimée, avec « vers le » et « à quelques jours près » ; le jour à partir duquel
   le relancer ; et qu'un rappel, si elle en veut un, c'est elle qui le pose, avec un intitulé neutre.

### Les listes de départ

- **La liste à cocher**, six cases : « La tisane, ma préférée », « Bonbons ou Nutella, ou du salé,
  selon mon envie », « La bouillotte prête, avant que je la demande », « Le plaid pilou-pilou sur le
  canapé », « Câlin ou paix royale : demande lequel. La réponse peut changer dans la journée, ce
  n'est pas un bug. », « La vaisselle, les courses ou le dîner : un des trois, en entier, sans qu'on
  te le demande. » En réserve, proposées seulement si elle veut en ajouter : « Une soirée sans rien
  de prévu, si je te le demande. », « Stock de protections vérifié : ma marque, ma taille. », « La
  phrase qui marche : “Je peux faire quelque chose pour toi ?” »
- **Les mots interdits cette semaine**, huit lignes avec leur touche d'humour, dans une rubrique
  facultative que tu n'imposes jamais (elle la retire d'un choix, ou dans le mail) : « T'as tes
  règles ou quoi ? », « C'est juste tes hormones. », « Tu es trop sensible. », « Ça fait vraiment si
  mal que ça ? », « Calme-toi. », « Tu ne te prives pas, dis donc. », « On en reparlera quand ce sera
  fini. », « T'as une petite mine. » Elles sont tournées sans accord (règle 6) ; si elle s'accorde
  elle-même au féminin, la quatrième et la dernière peuvent reprendre leur forme d'origine : « Tu es
  sûre que ça fait si mal que ça ? » et « Tu as l'air fatiguée. »

## À chaque lancement

1. Lance d'abord le calcul, même quand elle arrive avec une capture, une date ou une autre demande :
   il lit `reglages.md` pour toi.
   `python3 "<skill>/scripts/dates_cycle.py" calcul ~/.ca-arrive/reglages.md`
2. Traite ensuite l'argument s'il y en a un. Si le calcul affiche `a_completer`, pose ces questions
   avant de préparer le moindre mot, une par message, avec les choix du premier lancement.
3. Agis selon le `statut`. Chaque fois que le tableau dit « propose » ou « demande », c'est une
   question à choix, au sens de « La conversation » :

| Statut | Ce que tu fais |
|---|---|
| `premier_lancement` | Le fichier n'existe pas, est vide ou n'a que des rubriques vides : suis « Premier lancement ». Si le calcul affiche `fichier: present`, c'est le fichier témoin du test de persistance qui a survécu : le test est réussi. Dis-le, ne le repropose pas et reprends « Le suivi des dates » à l'étape 2, sans refaire la présentation. Si elle dit avoir déjà fait le test et que le calcul affiche `fichier: absent`, le test a échoué : n'écris aucune date. |
| `pause` | Dis-le en une ligne et propose de reprendre. Rien d'autre, même si le calcul affiche `a_completer` ou si elle demande « le mot maintenant » : propose d'abord de reprendre. |
| `aucune_date` | Aucune date n'est notée : propose les façons de les donner (l'export seulement si tu tournes sur son ordinateur), ou « le mot maintenant ». |
| `date_illisible`, `date_future` | Montre la ligne en cause et propose de la corriger avec elle. |
| `pas_assez_de_dates` | Il faut trois dates, ou la durée habituelle que son appli affiche. D'ici là, « le mot maintenant » prépare le mot quand elle le décide. |
| `trop_variable`, `intervalle_hors_bornes` | Le calcul se met en retrait, sans jugement : l'écart entre ses derniers cycles est trop grand pour estimer une date (c'est un seuil de l'outil, pas un avis médical). Montre `intervalles_jours` et demande s'il manque une date ou s'il y en a une de trop : un mois oublié double un intervalle. N'emploie jamais « irrégulier », « anormal », « inhabituel » ni « retard ». Elle garde « le mot maintenant ». |
| `avant_fenetre` | Donne la date estimée (« vers le … », avec `jour_date_estimee`) et le jour où le mot sera prêt (`debut_fenetre`, avec `jour_debut_fenetre`). Rien d'autre. |
| `dans_fenetre` | Si `mot_deja_prepare: non`, prépare le mot. Sinon, relance le gabarit et remontre-lui le mot (« Préparer le mot », étape 4) ; si la note qui porte la date estimée du calcul donne un autre jour de préparation que `aujourdhui`, son annonce a vieilli : propose de la refaire d'après le calcul du jour. Si « # Phrases de l'ambiance » est vide (le calcul l'affiche dans `a_completer`), pose d'abord la question des phrases de l'ambiance (« Retoucher le mot ») et note ses choix. |
| `date_estimee_passee` | Une phrase neutre : la date estimée est passée sans nouvelle date, donc tu ne prépares rien d'après le calcul. Propose d'ajouter une date ou de préparer le mot à sa demande. Aucune hypothèse sur la raison. |

## Préparer le mot

Le mot contient les cases et les mots interdits qu'elle a retenus, avec ses mots, ou, sans
réglages notés, les listes de départ, qu'elle relit et retouche dans le brouillon. Si la
check-list de `reglages.md` est vide (et non `aucune`), propose d'abord les six cases de départ
(« 1. Les prendre 2. Les ajuster 3. Pas de liste »). Une rubrique vide ou `aucune` disparaît du mot.

1. **L'annonce** : une phrase à la première personne, avec son expression et le moment en toutes
   lettres, jamais une date précise. Le calcul te donne `jours_avant_date_estimee`,
   `jour_date_estimee` (le jour de la semaine) et `semaine_date_estimee`. Prends le premier cas qui
   s'applique :
   - 0 jour : « d'un jour à l'autre » ; 1 jour : « sans doute demain » ;
   - `cette_semaine` : « vers jeudi », ou « en fin de semaine » si la date tombe du vendredi au
     dimanche (« ce week-end » si l'on est déjà vendredi) ;
   - `semaine_prochaine` : « vers mardi » jusqu'à six jours, « la semaine prochaine » au-delà ;
   - `dans_deux_semaines` : « dans dix jours, à peu près », avec le nombre de jours en toutes lettres
     (jamais « dans deux semaines » : ce peut être huit jours).

   Exemples : « Mes règles arrivent vers jeudi. », « Les Anglais débarquent en fin de semaine. » Le
   moment calculé est celui des règles : si son expression désigne ce qui les précède (« mon SPM »),
   ne l'accroche pas à ce moment ; propose « Mes règles arrivent vers mardi » ou sa propre tournure,
   et garde celle qu'elle valide. À la demande, sans calcul : « Ça arrive bientôt. », ou ce qu'elle
   dit.
2. **Les valeurs** : écris `~/.ca-arrive/mots/valeurs.json` avec `prenom`, `salutation` (absente si
   `par défaut`), `annonce_debut` (son expression, « Ça arrive » à défaut) et `annonce_moment` (le
   moment, « bientôt » à la demande), `cases` et `mots_interdits` (les lignes de ses rubriques, liste
   vide si `aucune`), `mot_perso`, `signature`, `objet` si elle change l'objet par défaut, « Ça arrive.
   Prépare-toi. », et, pour chaque phrase de l'ambiance qu'elle a changée ou retirée sous « # Phrases
   de l'ambiance », la clé `ouverture`, `apres_mots`, `merci` ou `fin` (son texte, ou `""` pour la
   retirer). Une clé absente garde la phrase de l'ambiance. Avec `--eml`, la clé `apercu` change ou
   retire le texte d'aperçu.
3. **Le gabarit** :
   `python3 "<skill>/scripts/preparer_mot.py" --ambiance <ambiance> --valeurs ~/.ca-arrive/mots/valeurs.json --dossier ~/.ca-arrive/mots`
   Il écrit `mot-<ambiance>.html` (le mail mis en page, styles en ligne, dont le titre est l'objet)
   et `mot-<ambiance>.txt`, et affiche `lien_envoi` : un lien `mailto:` sans destinataire, encodé
   pour que accents, guillemets et retours à la ligne arrivent intacts, ou `trop_long` au-delà de
   1 800 caractères. Ajoute `--eml` seulement si elle le demande (brouillon que certaines messageries
   ouvrent comme un message reçu) ; montre-lui alors le texte d'aperçu (`apercu` dans `phrases.json`).
4. **Ouvrir le mot**, de la première façon qui marche, avec trois lignes au plus autour. N'envoie
   jamais le `.html` dans la conversation : dans l'app Claude, un fichier HTML joint s'affiche en
   aperçu figé (constaté sur iPhone le 25/09/2026) ; ne le publie nulle part, ce serait mettre son
   mot en ligne.
   - **Sur son ordinateur** (tu tournes sur la machine qu'elle a devant elle), le brouillon mis en
     page. La première fois sur un Mac, préviens en une phrase : « macOS va peut-être vous demander
     d'autoriser <agent> à piloter Safari et Mail : acceptez, ou refusez et je vous donne la version
     texte. » Puis lance
     `python3 "<skill>/scripts/ouvrir_brouillon.py" --html ~/.ca-arrive/mots/mot-<ambiance>.html`
     et lis la ligne `etat:` :
     - `ouvert_mail_safari` (Mac : Safari confie la page à Mail) : « Le brouillon est ouvert dans
       Mail : ajoutez l'adresse d'Alex, relisez, envoyez. Vous pouvez fermer la page restée dans
       Safari. » ;
     - `ouvert_mail_presse_papiers` (Mac, en repli) : « Le brouillon est ouvert : cliquez dans le
       corps du message puis Cmd+V. Ajoutez ensuite l'adresse d'Alex, relisez, envoyez. » ;
     - `eml_ouvert` (Windows, Linux) : « Le brouillon s'ouvre dans votre messagerie : ajoutez
       l'adresse d'Alex, relisez, envoyez. » Outlook l'ouvre modifiable ; si sa messagerie l'ouvre
       comme un message reçu, sans bouton pour l'envoyer, passe à la version texte ;
     - `echec` : dis en une phrase ce qu'explique la ligne `detail:` (une autorisation refusée, par
       exemple), puis passe à la version texte. Sur un Mac, elle peut aussi le faire à la main :
       ouvrir `mot-<ambiance>.html` dans Safari, bouton Partager, Mail, format « Page web ».

     Sur un Mac, ajoute une fois, au conditionnel : « Si vous l'enregistrez dans Mail, il devrait
     vous attendre aussi dans Mail sur votre iPhone, selon votre compte. »
   - **Sur téléphone, dans le cloud ou par une messagerie** (app Claude, Cowork, ChatGPT, Telegram...),
     la version texte, en le disant une fois : « Sur téléphone, le mail part en texte ; pour la
     version mise en page, lancez le skill sur votre ordinateur. » D'abord l'ambiance (« 1. Complice :
     chaleureux et drôle 2. Douceur : tendre et câlin 3. Franc : net et bienveillant 4. Cash : sobre,
     direct et drôle »), avec laquelle tu relances le gabarit, puis « Votre mot pour Alex est prêt :
     [Ouvrir le mail tout prêt](<lien_envoi>). Ajoutez l'adresse, relisez, envoyez. », le texte du mot
     et « 1. C'est parfait 2. Retoucher le mot ». Le texte s'affiche comme du texte normal, jamais dans
     un bloc de code, qui passe en police à chasse fixe et coupe les lignes sur un téléphone. Recopie
     le lien tel que le script l'affiche, sans le couper ni le réencoder. Avec `trop_long` : « 1.
     Retirer quelques lignes 2. Copier-coller le texte ».

   Tu n'ouvres jamais toi-même le lien vers Mail : c'est elle qui le touche. Le brouillon, tu ne
   l'enregistres ni ne l'envoies jamais. Si l'annonce porte un jour (« vers mardi »), dis-lui
   qu'elle ne vaut que pour aujourd'hui : pour un envoi un autre jour, qu'elle te relance d'abord.
5. **Par une messagerie** (Telegram, WhatsApp...), le lien et le texte transitent par ses serveurs :
   dis-le-lui une fois.
6. **Note sous « # Notes »**, si `reglages.md` existe : `mot préparé le AAAA-MM-JJ pour la date estimée AAAA-MM-JJ` (ou `mot
   préparé le AAAA-MM-JJ, à la demande`, suivi de `pour la date estimée AAAA-MM-JJ` quand le calcul
   en donne une), la date du jour étant la ligne `aujourdhui:` du calcul.
7. Une fois le mot envoyé, propose de supprimer les fichiers de `mots/`.

## Les arguments

- **« c'est arrivé aujourd'hui »** (ou hier, ou une date) :
  `python3 "<skill>/scripts/dates_cycle.py" ajouter ~/.ca-arrive/reglages.md aujourdhui` (ou `hier`,
  ou `AAAA-MM-JJ`). Le script prend la date du jour lui-même, refuse une date future, n'ajoute pas de
  doublon et garde les sept plus récentes : dis-lui ce qu'il affiche, puis relance le calcul. S'il
  répond `meme_periode_que`, deux jours de la même période sont en jeu : demande-lui lequel était le
  premier jour, et n'enregistre que celui-là. Si c'est la nouvelle, retire l'ancienne de « # Dates »
  avec son accord, puis relance `ajouter` avec la nouvelle. S'il affiche `lignes_retirees`, dis-le-lui
  aussi.
- **« le mot maintenant »** : prépare le mot tout de suite, quel que soit le statut du calcul (avant
  la fenêtre, date estimée passée, `trop_variable`, `intervalle_hors_bornes`, pas assez de dates),
  sauf en pause.
  L'annonce suit alors la règle « À la demande » de « Préparer le mot », sauf en `dans_fenetre`, où
  elle suit le calcul (étape 1).
- **« réglages »** : suis « Retoucher le mot ». Ne montre que la rubrique en jeu, jamais tout le
  fichier, et jamais les dates sauf si elle les demande. Si elle change d'ambiance, cite en une ligne
  l'ouverture de la nouvelle et remplace ce qui est noté sous « # Phrases de l'ambiance ».
- **« pause »**, **« reprendre »** : `oui` ou `non` sous « # Pause ».
- **« tout effacer »** : voir plus bas.

## Les trois façons de donner ses dates

| | Ce que tu lis | Par où ça passe | Ce qui reste sur son ordinateur |
|---|---|---|---|
| **1. Elle les tape** (par défaut) | Les dates qu'elle écrit | Le modèle d'IA de son agent | `reglages.md`, et la trace locale de la conversation |
| **2. Une capture**, ou le PDF d'historique de l'app Santé | Toute l'image ou tout le PDF | Le modèle d'IA, image comprise | Sa capture d'origine, la copie éventuelle gardée par l'agent, les dates confirmées |
| **3. L'export** de son appli | Les premiers jours affichés par le script, rien d'autre | Le modèle d'IA, pour ces seules dates | L'export complet, à supprimer ensuite, et `reglages.md` |

Si elle te parle par une messagerie, tout ce qu'elle écrit ou envoie y transite aussi.

**1. Saisie.** Elle tape ses dates, ou les écrit elle-même dans `reglages.md`. Convertis au format
AAAA-MM-JJ, relis-les-lui, et sur son accord enregistre-les avec
`python3 "<skill>/scripts/dates_cycle.py" ajouter ~/.ca-arrive/reglages.md <dates>`.

**2. Capture**, si ton agent lit les images. Avant qu'elle l'envoie : recadrer sur le calendrier,
sans symptômes ni notes, et transférer l'image de son téléphone par câble, ou par AirDrop en gardant
les deux appareils côte à côte jusqu'à la fin du transfert, plutôt que par mail. Relève seulement
les premiers jours lus avec certitude, signale ceux dont tu doutes, et ne décris rien d'autre.
Termine ta liste par « Je garde ces dates dans vos réglages ? 1. Oui 2. Je corrige ». Sur son oui,
enregistre-les vraiment avec la commande `ajouter`, dis-lui ce qui a été enregistré (et ce qui y
était déjà), puis relance le calcul. Rappelle-lui ensuite de supprimer la
capture, puis de vider la corbeille des photos (« Supprimés récemment » sur iPhone).

**3. Export.** Seulement si tu tournes sur son ordinateur (dossier privé, étape 2) ; sinon, dis-lui
pourquoi et propose la saisie ou la capture. Lis `references/exports.md` et suis-le, selon son
appli.

## Arrêter et tout effacer

À « tout effacer », montre d'abord ce qui sera supprimé et demande son accord (« 1. Oui, tout
effacer 2. Annuler »), puis :

1. Supprime ses fichiers tout de suite :
   `python3 "<skill>/scripts/dates_cycle.py" effacer ~/.ca-arrive`. Le script supprime `reglages.md`
   et les mots préparés, et laisse le dossier vide (le prochain lancement repartira du début). Sans
   Python : `rm -f ~/.ca-arrive/reglages.md; rm -rf ~/.ca-arrive/mots` (si `mots/` est un lien, seul
   le lien part ; PowerShell : `Remove-Item -Force $HOME\.ca-arrive\reglages.md, $HOME\.ca-arrive\mots\*`).
2. **La trace des conversations**, que ton agent garde ailleurs : donne-lui, mot pour mot, la
   procédure de son agent dans `references/confidentialite.md` (section « Tout effacer »). Elle est à
   lancer par elle, après avoir quitté la session. Ne présente jamais comme suffisante une commande
   qui n'efface que la conversation en cours : les dates et les captures sont dans les précédentes.
3. Le dossier vide, à supprimer par elle ensuite : `rm -rf ~/.ca-arrive` (sous Windows,
   `Remove-Item -Recurse -Force $HOME\.ca-arrive`).
4. **Dis clairement ce que tu ne peux pas effacer toi-même** : les commandes des étapes 2 et 3, qui
   sont les siennes ; ce que le fournisseur du modèle conserve selon son compte ; les sauvegardes de
   toute la machine ; les mots déjà envoyés, et un brouillon enregistré dans sa messagerie (donc
   sur le serveur de son compte) ; la page du mot dans l'historique de Safari, et le mot laissé
   dans le presse-papiers par le repli ; les captures et exports restés sur son téléphone ou
   dans ses téléchargements. Si la section de son agent dit « non vérifié », dis-le tel quel.
5. Pour retirer le skill : supprimer son dossier, et, si elle n'en veut plus, les réglages ajoutés
   au premier lancement.
