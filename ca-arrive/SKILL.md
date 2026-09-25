---
name: ca-arrive
description: "Quelques jours avant vos règles, prépare pour la personne qui partage votre vie un mot que vous relisez et envoyez vous-même. À lancer seulement quand on l'appelle par son nom."
license: MIT
compatibility: "Agents au format Agent Skills qui lancent des commandes et écrivent des fichiers : Claude Code, Codex, Cowork, Hermes, OpenClaw. Python 3 conseillé."
metadata:
  version: "1.2"
  created: "2026-09-25"
  updated: "2026-09-25"
  source: "synoptia"
  category: "skill"
  theme: "organisation-personnelle"
---

# Ça arrive : le mot qui prévient, quelques jours avant

## Ce que ça fait

Quelques jours avant vos règles, quand vous le lancez, votre agent vous prépare un mot pour la
personne qui partage votre vie, votre conjoint ou votre conjointe : un mail mis en page, dans
l'ambiance que vous avez choisie, avec une petite liste à cocher et, si vous le voulez, vos « mots
interdits cette semaine ». Vous le relisez, vous le retouchez, et c'est vous qui l'envoyez. **Le
skill n'envoie jamais rien.** Il ne tourne pas non plus en arrière-plan : il vous dit à partir de
quel jour le mot sera prêt, et vous le relancez ce jour-là.

Vos dates passent par le modèle d'IA de votre agent, comme tout ce que vous lui écrivez, et restent
dans un fichier sur votre ordinateur quand votre agent y tourne (sinon, le skill vous prévient avant
de noter la moindre date). Vous choisissez comment les donner : vous les tapez, vous
montrez une capture de votre appli, ou vous passez par son export. Ce n'est pas un outil médical :
la date calculée n'est qu'une estimation.

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

```
Vos prochaines règles sont estimées vers le mardi 13 octobre, à quelques jours près. Voici le
mot pour Alex, ambiance « complice » :

  Objet : Ça arrive. Prépare-toi.
  Salut Alex,
  Mes règles arrivent vers mardi. Si je suis à cran, ça ne te vise pas, promis.
  TA MISSION, SI TU L'ACCEPTES
  [ ] Câlin ou paix royale : demande lequel. La réponse peut changer dans la journée...

La version mise en page est dans ~/.ca-arrive/mots/mot-complice.html. Je retouche quelque chose ?
```

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
  proposer, où ton agent garde la trace des conversations, et comment l'effacer.

## Les règles qui ne se discutent pas

1. **Tu n'envoies rien.** Aucun outil d'envoi (mail, messagerie, connecteur, navigateur piloté),
   aucun brouillon déposé dans une messagerie ou un service en ligne, aucun envoi programmé. Tu ne
   cherches jamais d'adresse, de numéro ou de contact, et tu n'en écris aucun dans les fichiers du
   mot. Répondre à l'utilisatrice dans sa propre conversation n'est pas un envoi ; écrire à
   quiconque d'autre en est un. Si tu cherches sur le web (la documentation de ton agent, par
   exemple), tes requêtes ne contiennent jamais ses dates, son prénom ni rien qui la concerne.
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
   n'affiche que des dates. Sur une capture, tu ne relèves que les premiers
   jours et tu ne décris rien d'autre.

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
2. Il est sur son ordinateur et il persiste. Si tu tournes dans le cloud ou sur un serveur (un VPS,
   par exemple), dans un bac à sable dont les fichiers disparaissent, si elle te parle par une
   messagerie plutôt que depuis la machine où tu tournes, ou si tu ne sais pas, dis-le-lui : ses
   dates seraient stockées sur cette machine, hors de son ordinateur, ou seraient perdues. Propose
   le test de `references/confidentialite.md` (un fichier vide, retrouvé ou non à la session
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

Même si sa demande contient déjà des réponses (dates, prénom, ambiance, délai), pose toutes les
questions restantes avant d'écrire `reglages.md`. N'écris jamais dans une rubrique une valeur qu'elle
n'a ni donnée ni validée : laisse-la vide. Quand elle ne veut pas d'une rubrique facultative, écris
`aucune` (ou `par défaut` pour la salutation), pour qu'on ne la lui redemande pas.

1. **Présente le skill en six lignes** : ce qu'il fait ; qu'il n'envoie rien ; que les dates restent
   dans un fichier sur son ordinateur quand tu y tournes (tu le vérifies juste après) ; que la date
   calculée n'est qu'une estimation ; que ce n'est pas un outil médical (ni contraception, ni projet
   de grossesse) ; qu'un mot suffit pour faire une pause ou effacer ses fichiers, le reste de la
   procédure venant de toi le moment venu. Termine sur « Voulez-vous continuer ? » et arrête-toi là
   jusqu'à sa réponse.
2. **Fais les vérifications** du dossier privé. Si tu es Claude Code, Codex ou Hermes en ligne de
   commande et que ton dossier de travail n'est pas `~/.ca-arrive`, propose-lui, avant la moindre
   date, de quitter puis de te relancer depuis ce dossier (`cd ~/.ca-arrive && claude`, ou `codex`,
   ou `hermes`) : sinon, les conversations du skill se mêlent à celles de ce dossier, et « tout
   effacer » aura du mal à les retrouver. Demande-lui ensuite si cet ordinateur et le compte de
   son agent sont à son seul usage, et non administrés par quelqu'un d'autre (un employeur, par
   exemple) ; sinon, dis-lui que d'autres pourraient lire ses dates et laisse-la décider. Propose
   ensuite les réglages de ton agent (`references/confidentialite.md`), chacun avec son accord
   explicite.
3. **Ses dates.** Présente les façons possibles, une ligne chacune, la première par défaut (la
   troisième seulement si tu tournes sur son ordinateur ; sinon, dis-lui en une ligne pourquoi elle
   n'est pas proposée) :
   - « Vous tapez vos dates » : je lis ce que vous tapez, qui passe par le modèle d'IA de votre
     agent, comme tout ce que vous lui écrivez ; le fichier de dates reste dans le dossier privé
     vérifié juste avant.
   - « Vous montrez une capture » de votre appli : je lis toute l'image, qui passe par le modèle ;
     recadrez sur le calendrier. Seules les dates que vous confirmez sont gardées.
   - « Vous passez par l'export » de votre appli : un petit programme le lit sur place et ne me
     transmet que les premiers jours ; l'export complet ne quitte pas votre ordinateur. Ne propose cette façon que si tu tournes sur son ordinateur : dans le cloud, sur un
     serveur ou par une messagerie, il faudrait t'envoyer l'export entier, qui contient bien plus que
     ses dates.

   Demande aussi le délai : deux, trois ou cinq jours avant, ou un autre nombre de 1 à 14 (trois par
   défaut). Si le calcul affiche « valeur par défaut » alors qu'elle a donné un délai, dis-le-lui.
4. **Le mot**, en deux temps. D'abord l'ambiance seule, parmi quatre (aperçus dans
   `assets/apercus/`), avec la phrase qui ouvre le mot, lue dans `assets/templates/phrases.json` (si ce
   fichier diffère des citations ci-dessous, c'est lui qui fait foi) : **douceur** (couleurs tendres, formes
   arrondies, ton câlin) : « Je vais sûrement manquer d'énergie et avoir la larme facile. Si je
   pleure, pas besoin de chercher pourquoi : prends-moi dans tes bras. » ; **complice** (chaleureux
   et drôle) : « Si je suis à cran, ça ne te vise pas, promis. » ; **franc** (net et bienveillant) :
   « Je te préviens maintenant pour qu'on s'organise tranquillement. Si je m'agace, ce que je dis
   reste valable, même quand le ton monte plus vite que d'habitude. » ; **cash** (sobre, contrasté,
   direct et drôle) : « Si je m'énerve contre toi, garde en tête que j'ai peut-être raison : on en
   reparle à froid quelques jours plus tard. » Précise que ces phrases parlent d'humeur et qu'elle peut
   n'en garder aucune : propose alors une ouverture sans humeur, « Je te préviens maintenant pour
   qu'on s'organise tranquillement. », ou la sienne.

   Puis, l'ambiance choisie, tout le reste dans un seul message :
   - ses quatre phrases modifiables, lues dans `assets/templates/phrases.json` : l'ouverture, la
     phrase sous les mots interdits (`apres_mots`), le remerciement (`merci`) et la formule avant la
     signature (`fin`, vide pour franc et cash). Elle garde, change ou retire chacune ; note ses choix
     sous « # Phrases de l'ambiance » (« par défaut » si elle garde tout). Dis-lui aussi ce qui reste
     fixe : l'étiquette (« Avis de passage »..., dans la seule version mise en page), le titre de la
     liste et la ligne qui le suit, s'il y en a une, et le titre « Mots interdits cette semaine »
     (dans les deux versions) ; si elle veut les changer, retouche avec elle
     le `.html` et le `.txt`, une fois le mot définitif, car le script réécrit les deux fichiers à
     chaque passage ;
   - comment elle commence ses messages à cette personne (« Mon cœur, », « Salut Alex, »), et sa
     signature ;
   - comment le mot en parle : elle nomme, avec ses mots (« mes règles », « mon SPM », « les Anglais
     débarquent »...), et elle peut y ajouter ce qu'elle veut dire d'elle ; toi, tu n'ajoutes rien ;
   - la liste à cocher : propose cette liste de départ, qu'elle garde, modifie ou supprime ligne à
     ligne : « La tisane, ma préférée », « Bonbons ou Nutella, ou du salé, selon mon envie », « La bouillotte
     prête, avant que je la demande », « Le plaid pilou-pilou sur le canapé », « Câlin ou paix royale :
     demande lequel. La réponse peut changer dans la journée, ce n'est pas un bug. », « La vaisselle,
     les courses ou le dîner : un des trois, en entier, sans qu'on te le demande. » En option :
     « Une soirée sans rien de prévu, si je te le demande. »,
     « Stock de protections vérifié : ma marque, ma taille. », « La phrase qui marche : “Je peux faire
     quelque chose pour toi ?” » ;
   - la rubrique « mots interdits cette semaine », facultative : propose cette liste de départ, avec
     sa touche d'humour, qu'elle garde, modifie ou supprime ligne à ligne, sans jamais l'imposer :
     « T'as tes règles ou quoi ? », « C'est juste tes hormones. », « Tu es trop sensible. », « Tu es
     sûre que ça fait si mal que ça ? », « Calme-toi. », « Tu ne te prives pas, dis donc. », « On en
     reparlera quand ce sera fini. », « Tu as l'air fatiguée. » Si elle ne s'accorde pas au féminin
     en parlant d'elle, propose ces deux lignes sans accord : « Ça fait vraiment si mal que ça ? » et
     « T'as une petite mine. » Sans liste, la rubrique disparaît ;
   - une phrase à elle, si elle le souhaite.
5. **Écris `reglages.md`** avec ses réponses, puis ses dates avec la commande `ajouter` (plus bas),
   montre le résumé et lance le calcul. Avant de conclure, vérifie que tu lui as dit :
   - la date estimée, avec « vers le » et « à quelques jours près » ;
   - le jour à partir duquel le mot sera prêt, et qu'il suffira de relancer le skill ce jour-là ;
   - qu'un rappel, si elle en veut un, c'est elle qui le pose, avec un intitulé neutre.

## À chaque lancement

1. Lance d'abord le calcul, même quand elle arrive avec une capture, une date ou une autre demande :
   il lit `reglages.md` pour toi.
   `python3 "<skill>/scripts/dates_cycle.py" calcul ~/.ca-arrive/reglages.md`
2. Traite ensuite l'argument s'il y en a un. Si le calcul affiche `a_completer`, pose ces questions
   avant de préparer le moindre mot.
3. Agis selon le `statut` :

| Statut | Ce que tu fais |
|---|---|
| `premier_lancement` | Le fichier n'existe pas, est vide ou n'a que des rubriques vides : suis « Premier lancement ». Si le calcul affiche `fichier: present`, c'est le fichier témoin du test de persistance qui a survécu : le test est réussi. Dis-le, ne le repropose pas et reprends à l'étape 2, sans refaire la présentation. Si elle dit avoir déjà fait le test et que le calcul affiche `fichier: absent`, le test a échoué : n'écris aucune date. |
| `pause` | Dis-le en une ligne et propose de reprendre. Rien d'autre, même si le calcul affiche `a_completer` ou si elle demande « le mot maintenant » : propose d'abord de reprendre. |
| `aucune_date` | Aucune date n'est notée : propose les façons de les donner (l'export seulement si tu tournes sur son ordinateur), ou « le mot maintenant ». |
| `date_illisible`, `date_future` | Montre la ligne en cause et propose de la corriger avec elle. |
| `pas_assez_de_dates` | Il faut trois dates, ou la durée habituelle que son appli affiche. D'ici là, « le mot maintenant » prépare le mot quand elle le décide. |
| `trop_variable`, `intervalle_hors_bornes` | Le calcul se met en retrait, sans jugement : l'écart entre ses derniers cycles est trop grand pour estimer une date (c'est un seuil de l'outil, pas un avis médical). Montre `intervalles_jours` et demande s'il manque une date ou s'il y en a une de trop : un mois oublié double un intervalle. N'emploie jamais « irrégulier », « anormal », « inhabituel » ni « retard ». Elle garde « le mot maintenant ». |
| `avant_fenetre` | Donne la date estimée (« vers le … », avec `jour_date_estimee`) et le jour où le mot sera prêt (`debut_fenetre`, avec `jour_debut_fenetre`). Rien d'autre. |
| `dans_fenetre` | Si `mot_deja_prepare: non`, prépare le mot. Sinon, dis où il se trouve ; si la note qui porte la date estimée du calcul donne un autre jour de préparation que `aujourdhui`, son annonce a vieilli : propose de la refaire d'après le calcul du jour. Si « # Phrases de l'ambiance » est vide (le calcul l'affiche dans `a_completer`), montre-lui d'abord les phrases de son ambiance, lues dans `phrases.json`, et note ses choix. |
| `date_estimee_passee` | Une phrase neutre : la date estimée est passée sans nouvelle date, donc tu ne prépares rien d'après le calcul. Propose d'ajouter une date ou de préparer le mot à sa demande. Aucune hypothèse sur la raison. |

## Préparer le mot

Le mot ne contient que ce qu'elle a retenu : les cases de sa check-list et ses mots interdits, avec
ses mots. Si la check-list est vide (et non `aucune`), propose d'abord la liste de départ, ligne à
ligne, et enregistre ses choix. Une rubrique vide ou `aucune` disparaît du mot, titre compris.

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
   `par défaut`), `annonce`, `cases` et `mots_interdits` (les lignes de ses rubriques, liste vide si
   `aucune`), `mot_perso`, `signature`, `objet` si elle change l'objet par défaut, « Ça arrive.
   Prépare-toi. », et, pour chaque phrase de l'ambiance qu'elle a changée ou retirée sous « # Phrases
   de l'ambiance », la clé `ouverture`, `apres_mots`, `merci` ou `fin` (son texte, ou `""` pour la
   retirer). Une clé absente garde la phrase de l'ambiance. Avec `--eml`, la clé `apercu` change ou
   retire le texte d'aperçu.
3. **Le gabarit** :
   `python3 "<skill>/scripts/preparer_mot.py" --ambiance <ambiance> --valeurs ~/.ca-arrive/mots/valeurs.json --dossier ~/.ca-arrive/mots`
   Il écrit `mot-<ambiance>.html` et `mot-<ambiance>.txt`. Ajoute `--eml` seulement si elle veut
   essayer un brouillon à ouvrir dans son logiciel de messagerie, en la prévenant que certains
   l'ouvrent comme un message reçu : le copier-coller marche partout. Avec `--eml`, montre-lui aussi
   le texte d'aperçu de l'ambiance (`apercu` dans `phrases.json`), que la boîte de réception affiche
   à côté de l'objet ; elle peut le garder, le changer ou le retirer.
4. **Montre la version texte** dans la conversation et retouche jusqu'à ce qu'elle soit contente.
5. **L'envoi, par elle**, en toutes lettres : ouvrir le `.html` dans son navigateur (tu peux
   l'ouvrir pour elle si elle le demande) ; tout sélectionner (Cmd+A sur Mac, Ctrl+A ailleurs) ;
   copier ; coller dans un nouveau mail ; taper l'objet (celui du mot, « Ça arrive. Prépare-toi. »
   par défaut) ; remplir le champ « À » ; envoyer. Pour un SMS, elle copie la version `.txt`.
   Dis-lui que l'annonce vaut pour aujourd'hui : si elle envoie le mot un autre jour, qu'elle te
   relance d'abord, pour que tu la refasses d'après le calcul du jour (« sans doute demain » ou
   « vers lundi » ne valent que pour le jour où le mot a été préparé). Si elle te parle depuis une
   messagerie (Telegram, WhatsApp, Discord...) et pas depuis l'ordinateur où tu tournes, donne-lui la version texte dans la conversation et propose le
   `.html` en pièce jointe dans cette même conversation : tout ce qui passe par la messagerie
   transite par ses serveurs, dis-le-lui une fois.
6. **Note sous « # Notes »** : `mot préparé le AAAA-MM-JJ pour la date estimée AAAA-MM-JJ` (ou `mot
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
- **« réglages »** : montre les réglages (sans les dates, sauf si elle les demande) et change ce
  qu'elle veut. Si elle change d'ambiance, montre-lui les phrases de la nouvelle et remplace ce qui
  est noté sous « # Phrases de l'ambiance ».
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
les premiers jours lus avec certitude, signale ceux dont tu doutes, et ne décris rien d'autre. Termine ta liste par la question « Je garde ces dates dans vos
réglages ? » Sur son oui, enregistre-les vraiment avec la commande `ajouter`, dis-lui ce qui a été
enregistré (et ce qui y était déjà), puis relance le calcul. Rappelle-lui ensuite de supprimer la
capture, puis de vider la corbeille des photos (« Supprimés récemment » sur iPhone).

**3. Export.** Seulement si tu tournes sur son ordinateur (dossier privé, étape 2) ; sinon, dis-lui
pourquoi et propose la saisie ou la capture. Lis `references/exports.md` et suis-le, selon son
appli.

## Arrêter et tout effacer

À « tout effacer », montre d'abord ce qui sera supprimé et demande son accord, puis :

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
   toute la machine ; les mots déjà envoyés ; les captures et exports restés sur son téléphone ou
   dans ses téléchargements. Si la section de son agent dit « non vérifié », dis-le tel quel.
5. Pour retirer le skill : supprimer son dossier, et, si elle n'en veut plus, les réglages ajoutés
   au premier lancement.
