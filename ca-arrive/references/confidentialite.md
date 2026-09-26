# Confidentialité et réglages, agent par agent

L'agent qui exécute le skill lit la section qui le concerne au premier lancement, propose les
réglages indiqués (chacun avec l'accord explicite de l'utilisatrice) et donne, à « tout effacer », la
procédure de sa section « Tout effacer », mot pour mot. Tout vient de la documentation officielle de
chaque agent, lue le 25/09/2026, avec sa source, ou d'un test réel quand c'est précisé. Ce qui n'est
pas vérifié est écrit comme tel : dans ce cas, dis-le et renvoie à la documentation de son agent.

## Pour tous les agents

- Tout ce que l'agent lit (les dates tapées, une capture, ce que le script affiche) passe par le
  modèle d'IA de l'agent, chez son fournisseur, et la plupart des agents gardent en plus, sur
  l'ordinateur, la transcription de chaque conversation. C'est pour cela que « tout effacer » a
  toujours deux temps : les fichiers du skill, puis les conversations de l'agent.
- Si l'agent est joint par une messagerie (Telegram, WhatsApp, Discord...), toute la conversation
  transite aussi par les serveurs de cette messagerie.
- Si le dossier de configuration de l'agent est sauvegardé dans Git (certaines personnes versionnent
  `~/.claude`, `~/.codex`, `~/.hermes` ou `~/.openclaw`), ses conversations pourraient partir dans
  cet historique : vérifie ce que le dépôt ignore, et arrête-toi si tu ne peux pas l'établir.
- Une sauvegarde de toute la machine (Time Machine ou autre) garde ses propres copies, que « tout
  effacer » n'atteint pas.
- Si tu cherches sur le web, tes requêtes ne contiennent jamais ses dates, son prénom ni rien qui la
  concerne.
- **Le brouillon mis en page** (sur son ordinateur, `scripts/ouvrir_brouillon.py`) ne passe par
  aucun serveur tant qu'elle ne l'envoie pas. Sur Mac, Safari ouvre le fichier du mot, sans appel
  réseau (le gabarit n'a ni image ni ressource externe), et le garde dans son historique, avec son
  titre « Ça arrive. Prépare-toi. » ; Mail reçoit la page comme au bouton Partager, format « Page
  web » (aide d'Apple : https://support.apple.com/fr-fr/guide/safari/sfri40722/mac et
  https://support.apple.com/en-euro/guide/mail/mail40723/16.0/mac/15.0, lues le 25/09/2026). La
  commande AppleScript de Safari qui fait ce geste (`email contents`) n'est décrite que par des
  échanges d'utilisateurs (https://discussions.apple.com/thread/200240, 2005, et
  https://www.macscripter.net/t/safari-and-mail/49024, 2007) : non vérifié sur le Safari actuel,
  d'où le repli. En repli, le mot passe par le presse-papiers, où il reste jusqu'à la copie
  suivante (un gestionnaire d'historique du presse-papiers peut le garder plus longtemps). Sous
  Windows et Linux, un fichier `.eml` est écrit dans `~/.ca-arrive/mots/`, effacé avec les autres.
  Si elle enregistre le brouillon, il rejoint le dossier Brouillons de son compte de messagerie,
  sur le serveur de ce compte, comme tout brouillon (et, selon le compte, sur ses autres appareils).
- **Sur téléphone ou dans une session en ligne**, le lien vers Mail et le texte du mot font partie
  de la conversation avec l'agent, comme tout ce qu'elle y écrit. Le fichier `.html` n'est jamais
  joint à la conversation ni publié.

### Le test de persistance (environnement inconnu, bac à sable, cloud)

Avant toute date : crée `~/.ca-arrive/reglages.md` avec les seuls titres des rubriques, sans valeur ni ligne d'aide, affiche le chemin
réel (`cd ~/.ca-arrive && pwd -P`), et demande-lui de relancer le skill dans une nouvelle session.
À la relance, le calcul affiche `fichier: present` si le fichier témoin a survécu : le test est
réussi. S'il affiche `fichier: absent`, ce dossier ne convient pas : dis-le-lui et n'écris aucune
date. Si le
chemin montre que tu tournes sur une machine distante, dis-lui que ses dates y seraient stockées.

## Claude Code

Sources : https://code.claude.com/docs/en/skills, https://code.claude.com/docs/en/data-usage,
https://code.claude.com/docs/en/claude-directory, https://code.claude.com/docs/en/env-vars

- **Emplacement du skill** : `~/.claude/skills/ca-arrive/`. Invocation : `/ca-arrive`.
- **Invocation manuelle seulement** (à proposer) : dans `~/.claude/settings.json`, ajouter
  `"skillOverrides": { "ca-arrive": "user-invocable-only" }` en fusionnant sans toucher au reste. Le
  skill disparaît de la liste que Claude consulte seul, et reste dans le menu `/`. (Le champ
  `disable-model-invocation: true` fait la même chose dans l'en-tête du skill, mais un téléversement
  vers claude.ai le refuse : il n'est donc pas dans le fichier livré.)
- **Deux portes à fermer** (à proposer) : dans le bloc `env` du même fichier,
  `"DISABLE_FEEDBACK_COMMAND": "1"` et `"CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY": "1"`. La commande
  `/feedback` envoie la conversation, conservée cinq ans ; un « oui » à la question qui suit parfois
  le questionnaire de satisfaction l'envoie aussi, conservée jusqu'à six mois. Effet au prochain
  lancement.
- **Chez Anthropic** : avec un abonnement Free, Pro ou Max, cinq ans si l'utilisatrice autorise
  l'usage de ses données pour améliorer les modèles, trente jours sinon (réglage :
  `claude.ai/settings/data-privacy-controls`) ; avec Team, Enterprise ou une clé API, trente jours,
  sans entraînement.
- **Session sans transcription** (à proposer) : `mkdir -p ~/.ca-arrive && cd ~/.ca-arrive &&
  CLAUDE_CODE_SKIP_PROMPT_HISTORY=1 CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude` (PowerShell :
  `New-Item -ItemType Directory -Force "$HOME\.ca-arrive" | Out-Null; Set-Location "$HOME\.ca-arrive";
  $env:CLAUDE_CODE_SKIP_PROMPT_HISTORY="1"; $env:CLAUDE_CODE_DISABLE_AUTO_MEMORY="1"; claude` ; ces
  deux réglages valent jusqu'à la fermeture de la fenêtre). Claude Code n'écrit alors ni la
  transcription ni l'historique de saisie sur le disque, et n'alimente pas sa mémoire automatique ;
  la conversation ne pourra pas être reprise. À ne pas mettre dans `settings.json`, qui
  l'appliquerait partout. Non vérifié : si les images collées et les copies de fichiers modifiés
  (`file-history`) sont aussi épargnées.
- **Sur l'ordinateur** : les conversations sont gardées en clair dans `~/.claude/projects/`, trente
  jours par défaut (`cleanupPeriodDays`), sauf les sessions ouvertes ou reprises dans l'app de bureau
  Claude ou dans Cowork, gardées sans limite d'âge (réglage `desktopSessionCleanupPeriodDays`) ; ce
  qu'elle tape va dans `~/.claude/history.jsonl`, gardé jusqu'à ce qu'on l'efface ; les images collées vont dans un dossier temporaire, effacé au bout de
  la même durée. La mémoire automatique de Claude Code est rangée par projet.
- **Si `~/.claude` est un dépôt Git** : `git -C ~/.claude check-ignore projects/x file-history/x
  paste-cache/x image-cache/x history.jsonl` doit afficher les cinq chemins (l'option `-q` n'accepte
  qu'un seul chemin). S'il en manque un, arrête-toi et montre les lignes à ajouter à
  `~/.claude/.gitignore`. Si `git -C ~/.claude log --oneline -- projects
  file-history paste-cache image-cache history.jsonl` affiche quelque chose, ces fichiers sont déjà dans l'historique :
  déconseille de continuer.
- **Lancer depuis le dossier privé** : `cd ~/.ca-arrive && claude`, pour que la purge ci-dessous
  vise ce seul dossier.

### Tout effacer, sous Claude Code

Après avoir quitté Claude Code : `claude project purge ~/.ca-arrive` (PowerShell :
`claude project purge "$HOME\.ca-arrive"`). La commande supprime, pour ce
dossier, les conversations, la mémoire du projet, les copies de fichiers modifiés et les lignes de
l'historique de saisie ; elle affiche la liste et demande confirmation. Si elle a utilisé le skill
depuis un autre dossier, la même commande sur ce dossier-là effacerait aussi ses autres
conversations de ce dossier : préviens-la. La purge ne touche pas les images collées ni les longs
textes collés (`~/.claude/paste-cache/`), effacés seuls au bout de trente jours par défaut.

## Codex (CLI, extension d'éditeur, app de bureau ChatGPT)

Sources : https://learn.chatgpt.com/docs/build-skills (ancienne adresse
developers.openai.com/codex/skills), https://learn.chatgpt.com/docs/developer-commands (commandes
`codex resume`, `codex delete`, `/archive`), https://learn.chatgpt.com/docs/config-file/config-advanced,
https://learn.chatgpt.com/docs/config-file/config-reference,
https://learn.chatgpt.com/docs/reference/troubleshooting, https://learn.chatgpt.com/docs/auth

- **Emplacement du skill** : `~/.agents/skills/ca-arrive/` (niveau utilisateur). Invocation :
  `$ca-arrive`, ou `/skills` pour choisir (dans l'app de bureau ChatGPT : tapez `@` et choisissez le
  skill ; non testé). Codex repère les nouveaux skills seul ; sinon, le relancer.
- **Invocation manuelle seulement** : c'est déjà réglé par le fichier `agents/openai.yaml` livré avec
  le skill (`allow_implicit_invocation: false`) ; `$ca-arrive` fonctionne toujours.
- **Sur l'ordinateur** : Codex garde son état sous `~/.codex`, chaque conversation dans
  `~/.codex/sessions` et les conversations archivées dans `~/.codex/archived_sessions`
  (documentation, page Troubleshooting). Constaté lors d'un test réel le 25/09/2026 avec Codex CLI
  0.155.1 : chaque conversation y est gardée en entier, images jointes comprises, sous la forme
  `~/.codex/sessions/AAAA/MM/JJ/rollout-*.jsonl`, et indexée dans des bases `~/.codex/*.sqlite`.
- **Le réglage `history.persistence = "none"`** ne concerne que le fichier `~/.codex/history.jsonl` :
  il ne protège pas ces transcriptions de sessions (constaté en test ; une page de la documentation
  laisse entendre le contraire). Ne le présente pas comme une protection.
- **Mémoires** : désactivées par défaut (`features.memories`). Si elle les a activées, dis-le-lui :
  une conversation de ce skill pourrait servir à en générer.
- **Une porte à fermer** (à proposer) : la commande `/feedback` peut joindre la conversation en cours
  et l'envoyer à l'équipe de Codex chez OpenAI. Pour la désactiver, ajouter à `~/.codex/config.toml`
  la section `[feedback]` avec `enabled = false`, en fusionnant sans toucher au reste ; effet au
  prochain lancement de Codex (réglage `feedback.enabled`, page config-reference).
- **Trace du dossier** (constaté lors du même test) : Codex inscrit le dossier de travail dans
  `~/.codex/config.toml`, sous la forme `[projects."/chemin/vers/.ca-arrive"]` suivie de
  `trust_level = "trusted"`. Aucune date n'y figure, mais le nom du dossier y reste : ces deux lignes
  se retirent à la main après l'effacement.
- **Recherches web** : Codex peut consulter sa propre documentation en ligne pendant une session ;
  ses requêtes ne doivent jamais contenir ses dates.
- **Chez OpenAI** : connectée avec ChatGPT, la conservation suit les réglages de son espace ChatGPT ;
  avec une clé API, ceux de son organisation API. Durée exacte non vérifiée : renvoie à ces réglages.

### Tout effacer, sous Codex

La commande `/delete` ne supprime que la conversation en cours : elle ne suffit pas. Après avoir
quitté Codex :

1. depuis le dossier privé, lancer `codex resume` : la liste ne montre que les conversations
   ouvertes depuis ce dossier. Si elle a aussi lancé Codex ailleurs pour ce skill, `codex resume
   --all` montre toutes ses conversations : repérer celles du skill. Noter l'identifiant de chacune,
   puis sortir sans en reprendre aucune ;
2. pour chaque identifiant : `codex delete <identifiant>` (la commande demande confirmation) ;
3. une conversation archivée (`/archive`) n'apparaît plus dans les listes mais reste dans
   `~/.codex/archived_sessions` : `codex unarchive <identifiant>`, puis `codex delete <identifiant>` ;
4. retirer de `~/.codex/config.toml` les deux lignes du dossier `.ca-arrive`.

Testé le 25/09/2026 : les fichiers de session et les lignes des bases disparaissent. Quelques
fragments de texte peuvent subsister dans l'espace libéré des bases SQLite de Codex, sans l'image.

## Cowork (Claude)

Sources : https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork,
https://support.claude.com/en/articles/12512198-how-to-create-custom-skills (mise à jour le
22/07/2026), https://support.claude.com/en/articles/12512180-use-skills-in-claude,
https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview,
https://support.claude.com/en/articles/13455879-use-claude-cowork-on-team-and-enterprise-plans,
https://code.claude.com/docs/en/skills (section sur Cowork)

- **Emplacement du skill** : Cowork ne lit pas `~/.claude/skills/`. Il charge les skills activés sur
  le compte claude.ai : **Customize > Skills**, « + », « Create skill », « Upload a skill », puis
  téléverser le ZIP du skill (le dossier `ca-arrive/` en tête, c'est le format livré). L'exécution de
  code doit être activée.
- **Invocation** : pas de réglage « manuel seulement » dans claude.ai ; la description demande de ne
  l'utiliser que sur demande explicite. Elle écrit « Utilise le skill ca-arrive ».
- **Où vont les dates** : d'après l'aide de Claude, une session Cowork tourne par défaut dans le
  cloud (en bêta), sur les serveurs d'Anthropic, et ses sessions et fichiers sont alors enregistrés
  sur le compte Claude ; le mode local, qui reste disponible pour les installations de bureau
  existantes, fait tourner le code dans une machine virtuelle de l'ordinateur et garde l'historique
  sur l'ordinateur. Dans le cloud, chaque session tourne dans un bac à sable temporaire, détruit à la
  fin de la session, et ce qui est gardé l'est sur son compte Claude : c'est « le cas du cloud » de
  `SKILL.md`, où le mot se prépare sur le moment, sans date ni suivi, ce que tu lui dis dès la
  présentation. En local, le code tourne dans la machine virtuelle de Cowork : le test de
  persistance dit si le fichier survit d'une session à l'autre, pas où il se trouve ; fais-le avant
  toute date, et laisse-la décider.
- **Mémoire de Claude** : dans le cloud, Cowork partage la mémoire de Claude avec le chat. Par
  défaut, Claude ne mémorise pas les sujets de santé, sauf si « Include sensitive topics in memory »
  est activé dans Settings > Memory. Propose-lui de vérifier ce réglage, ou de mettre la mémoire en
  pause (Settings > Memory, « Pause memory ») le temps d'utiliser le skill. Source :
  https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context
- **Chez Anthropic** : selon les réglages de confidentialité de son compte Claude
  (`claude.ai/settings/data-privacy-controls`).

### Tout effacer, sous Cowork

Supprimer chaque tâche Cowork du skill : dans la liste des tâches, **⋮** puis **Delete** (ou la
corbeille après sélection). Si son compte n'affiche plus le choix « Chat » / « Cowork » (nouvelle
expérience, en cours de déploiement sur les offres Pro et Max), la tâche est une conversation de la
liste Recents (« Chats and tasks ») : **⋮** puis **Delete**, avec le même délai de trente jours
(https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude et
https://support.claude.com/en/articles/8230524-delete-or-rename-a-conversation). D'après l'aide de Claude, la tâche disparaît aussitôt de l'historique et
est supprimée des serveurs d'Anthropic sous trente jours. Non vérifié : si les fichiers écrits
pendant la tâche (le dossier `~/.ca-arrive`) partent avec elle ; demande-lui de vérifier par le test
de persistance qu'ils ont bien disparu. Pour une session locale, l'historique reste sur l'ordinateur,
hors des règles de conservation d'Anthropic ; d'après la documentation de Claude Code, la
transcription d'une session commencée ou reprise dans Cowork est gardée sans limite d'âge, sauf
réglage `desktopSessionCleanupPeriodDays` ; non vérifié : comment l'effacer au-delà de Delete.

## Hermes Agent

Sources : https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md,
https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/sessions.md et
https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/memory.md
(documentation officielle), et https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/profiles.md

- **Profils** : les chemins ci-dessous sont ceux du profil par défaut. Avec un profil nommé, tout vit
  sous `~/.hermes/profiles/<nom>/` (skills, `config.yaml`, `state.db`, `memories/`), et chaque
  commande `hermes` prend `-p <nom>` (par exemple `hermes -p <nom> sessions list --workspace
  .ca-arrive`).
- **Emplacement du skill** : `~/.hermes/skills/ca-arrive/`, ou un dossier externe déclaré dans
  `~/.hermes/config.yaml` sous `skills.external_dirs` (par exemple `~/.agents/skills`). Invocation :
  `/ca-arrive`, en ligne de commande ou depuis n'importe quelle messagerie reliée.
- **L'agent peut réécrire ses skills** (revue après session, consolidation). Pour qu'il ne modifie
  pas ces règles sans son accord, proposer `skills.write_approval: true` (ou `/skills approval on`).
  Même principe pour sa mémoire : `memory.write_approval`, afin que rien de ce skill n'y entre sans
  son accord.
- **Sur l'ordinateur** : chaque conversation, qu'elle vienne du terminal ou d'une messagerie, est
  gardée en entier dans `~/.hermes/state.db`, avec une recherche plein texte ; Hermes peut retrouver
  d'anciennes conversations pour s'en servir dans une autre. Les sessions terminées et inactives
  depuis 90 jours sont supprimées seules, par défaut (`sessions.retention_days`).
- **Non vérifié** : la conservation chez le fournisseur du modèle choisi dans Hermes.

### Tout effacer, sous Hermes

1. `hermes sessions list --workspace .ca-arrive` pour les conversations ouvertes depuis le dossier
   privé (si elle a lancé Hermes depuis un autre dossier, `hermes sessions list` sans filtre, et
   repérer celles du skill) ; pour une conversation menée par messagerie, `hermes sessions list --source telegram` (ou
   le nom de sa messagerie), et repérer celles du skill ;
2. pour chaque identifiant : `hermes sessions delete <identifiant>` (avec confirmation) ;
3. relire `~/.hermes/memories/MEMORY.md` et `~/.hermes/memories/USER.md` (profil par défaut ; avec
   un profil nommé, `~/.hermes/profiles/<nom>/memories/`), ainsi que `/memory pending` si
   l'approbation est active, et retirer toute ligne liée au skill : par défaut, la revue
   d'arrière-plan de Hermes enregistre en mémoire sans demander ;
4. Hermes arrêté : `hermes sessions optimize`, qui compacte `state.db` et en retire l'espace libéré.

La commande `/compress` réduit une conversation mais n'efface rien : ne la présente pas comme un
effacement. Les messages restent aussi dans l'historique de la messagerie utilisée.

## OpenClaw

Sources : https://docs.openclaw.ai/tools/skills, https://docs.openclaw.ai/tools/slash-commands,
https://docs.openclaw.ai/cli/sessions, https://docs.openclaw.ai/cli/memory,
https://docs.openclaw.ai/concepts/session (sources sur GitHub : `docs/tools/skills.md`,
`docs/cli/sessions.md`, `docs/concepts/session.md` du dépôt openclaw/openclaw)

- **Emplacement du skill** : `~/.agents/skills/ca-arrive/` (skills personnels, profil par défaut ;
  avec un autre profil, utiliser `--global` ou le dossier `skills/` de l'espace de travail), ou pour
  tous les agents locaux `openclaw skills install ./ca-arrive --global` (dossier partagé, `~/.openclaw/skills` par défaut),
  ou `<workspace>/skills/` pour un seul agent. Invocation : `$ca-arrive`, ou, dans un message
  d'une messagerie reliée, `/ca_arrive` (OpenClaw remplace le tiret par un tiret bas dans les
  commandes) ou `/skill ca-arrive`. OpenClaw relit ses skills au début d'une session.
- **Invocation manuelle seulement** (à proposer) : OpenClaw reconnaît `disable-model-invocation: true`
  dans l'en-tête du `SKILL.md`. Avec son accord, ajoute cette ligne sous `description:` ; `$ca-arrive`
  fonctionne toujours, tapé en entier (le skill n'apparaît plus dans la liste du `$` ; OpenClaw
  2026.8.1 ou plus récent, sinon `/skill ca-arrive`).
- **Le mode à conseiller : un fil incognito.** Dans l'interface Control UI, écran **New thread**,
  activer **Incognito** avant de commencer : la conversation reste en mémoire au lieu d'être écrite
  sur le disque, expire au bout de 24 heures ou au redémarrage, et part sans archive. Les fichiers
  que le skill écrit dans `~/.ca-arrive` restent, eux, ce qui est voulu.
- **Non vérifié** : la conservation chez le fournisseur du modèle.

### Tout effacer, sous OpenClaw

1. `openclaw sessions` pour lister les conversations, et repérer les clés de celles du skill ;
2. pour chacune : `openclaw sessions delete "<clé>"` (avec confirmation). Pour une conversation
   ordinaire, OpenClaw garde la transcription dans une archive `.jsonl.deleted.<horodatage>`, qui
   peut encore servir à sa recherche en mémoire : c'est documenté, et cette archive n'est pas
   effacée par la commande ;
3. pour retirer ce qui a été indexé en mémoire : `openclaw memory forget --agent <agent> --session
   <clé>`, sur la machine qui fait tourner OpenClaw, d'abord avec `--dry-run` pour voir ce qui sera
   retiré, puis sans : cette commande efface sans demander de confirmation.

Les transcriptions archivées vivent dans `~/.openclaw/agents/<agent>/sessions/` ; non vérifié : que
l'archive `.jsonl.deleted.*` s'y trouve aussi, et la façon de la supprimer. Un
fil incognito évite ce problème.

## Un autre agent

Si ton agent lit le format Agent Skills (https://agentskills.io) mais n'est pas listé ici, dis-le-lui
franchement : tu ne connais ni ses emplacements, ni ce qu'il conserve, ni sa commande d'effacement.
Renvoie à sa documentation, fais le test de persistance, et applique toutes les autres règles.
