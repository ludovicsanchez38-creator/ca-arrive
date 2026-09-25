# Installer le skill `ca-arrive`

Il vous faut un agent déjà installé qui lit le format Agent Skills (https://agentskills.io) et qui
peut lancer des commandes. Le ZIP contient un dossier `ca-arrive/` : il suffit de le placer dans le
dossier des skills de votre agent. Les commandes ci-dessous supposent que `ca-arrive.zip` est dans
votre dossier Téléchargements (`Downloads`). Si votre Mac l'a déjà décompressé, remplacez
`unzip ~/Downloads/ca-arrive.zip -d <dossier>` par `cp -R ~/Downloads/ca-arrive <dossier>`.

Si vous avez téléchargé le dépôt GitHub plutôt que `ca-arrive.zip`, vous obtenez un dossier
`ca-arrive-main/` qui contient `ca-arrive/` : remplacez chaque `unzip ~/Downloads/ca-arrive.zip -d <dossier>`
ci-dessous par la copie de ce seul dossier, `cp -R ~/Downloads/ca-arrive-main/ca-arrive <dossier>`.
Pour Cowork, compressez ce seul dossier `ca-arrive/` en ZIP et téléversez ce ZIP. Sous Windows, les
commandes sont dans le README du dépôt.

## Avec votre agent

| Agent | Où placer le dossier `ca-arrive/` | Pour le lancer |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `/ca-arrive` |
| Codex | `~/.agents/skills/` | `$ca-arrive` |
| Cowork | téléversez le ZIP dans Customize > Skills | « Utilise le skill ca-arrive » |
| Hermes | `~/.hermes/skills/` | `/ca-arrive` |
| OpenClaw | `~/.agents/skills/` | `$ca-arrive` |
| Un autre agent | consultez la documentation de votre agent | « Utilise le skill ca-arrive » |

Un même dossier `~/.agents/skills/ca-arrive/` sert à Codex et à OpenClaw. Les dossiers qui
commencent par un point sont cachés par le Finder du Mac : le plus simple est de passer par le
Terminal (ou PowerShell sous Windows), avec les commandes ci-dessous.

### Claude Code

```bash
mkdir -p ~/.claude/skills
unzip ~/Downloads/ca-arrive.zip -d ~/.claude/skills/
```

Sous Windows (PowerShell) :
`Expand-Archive "$HOME\Downloads\ca-arrive.zip" -DestinationPath "$HOME\.claude\skills"`.

Lancez ensuite Claude Code depuis le dossier privé du skill, pour que ses conversations s'effacent
plus tard d'une seule commande (`claude project purge ~/.ca-arrive`, ou
`claude project purge "$HOME\.ca-arrive"` sous Windows ; hors images et longs textes collés, que Claude
Code efface seul au bout de trente jours par défaut) :
`mkdir -p ~/.ca-arrive && cd ~/.ca-arrive && claude`, puis tapez `/ca-arrive`. Sous Windows :
`New-Item -ItemType Directory -Force "$HOME\.ca-arrive" | Out-Null; Set-Location "$HOME\.ca-arrive"; claude`.
Pour que Claude Code n'écrive ni la conversation ni l'historique de saisie sur le disque, et
n'alimente pas sa mémoire automatique, lancez-le plutôt ainsi :
`mkdir -p ~/.ca-arrive && cd ~/.ca-arrive && CLAUDE_CODE_SKIP_PROMPT_HISTORY=1 CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude` (la
conversation ne pourra alors pas être reprise). Sous Windows (PowerShell) :
`New-Item -ItemType Directory -Force "$HOME\.ca-arrive" | Out-Null; Set-Location "$HOME\.ca-arrive"; $env:CLAUDE_CODE_SKIP_PROMPT_HISTORY="1"; $env:CLAUDE_CODE_DISABLE_AUTO_MEMORY="1"; claude`
(valable jusqu'à la fermeture de la fenêtre). Au premier lancement, le skill vous propose de le
réserver à vos seules demandes (réglage `skillOverrides`) et de désactiver deux fonctions qui peuvent
envoyer vos conversations à Anthropic (la commande `/feedback` et le questionnaire de satisfaction).
Sources : https://code.claude.com/docs/en/skills et https://code.claude.com/docs/en/env-vars

### Codex

```bash
mkdir -p ~/.agents/skills
unzip ~/Downloads/ca-arrive.zip -d ~/.agents/skills/
```

Sous Windows (PowerShell) :
`Expand-Archive "$HOME\Downloads\ca-arrive.zip" -DestinationPath "$HOME\.agents\skills"`.

Lancez Codex depuis le dossier privé (`mkdir -p ~/.ca-arrive && cd ~/.ca-arrive && codex`), puis
tapez `$ca-arrive`. Sous Windows :
`New-Item -ItemType Directory -Force "$HOME\.ca-arrive" | Out-Null; Set-Location "$HOME\.ca-arrive"; codex`.
Le fichier `agents/openai.yaml` livré avec le skill empêche Codex de le lancer de lui-même. Si le
skill n'apparaît pas, relancez Codex. Si Codex vous demande l'autorisation d'écrire dans
`~/.ca-arrive` (cela arrive quand son bac à sable est limité), acceptez pour ce dossier seulement.
Codex garde vos conversations sur votre ordinateur : « tout effacer » vous donne la procédure pour
les supprimer (`codex resume`, puis `codex delete`), et le skill vous propose au premier lancement
de fermer la commande `/feedback`, qui peut envoyer une conversation à OpenAI.
Source : https://learn.chatgpt.com/docs/build-skills (l'ancienne adresse
developers.openai.com/codex/skills y renvoie)

### Cowork

Cowork ne lit pas les skills rangés sur votre ordinateur (`~/.claude/skills/`) : dans l'app Claude,
ouvrez **Customize > Skills**, cliquez sur « + », puis « Create skill » et « Upload a skill », et
téléversez `ca-arrive.zip` tel quel. L'exécution de code doit être activée. Écrivez ensuite
« Utilise le skill ca-arrive ». Attention : d'après l'aide de Claude, une session Cowork tourne par
défaut dans le cloud (en bêta), et ses fichiers sont alors enregistrés sur votre compte Claude ; le
mode local, qui reste disponible pour les installations de bureau existantes, fait tourner le code
dans une machine virtuelle de votre ordinateur. Dans le premier cas, vos dates seraient stockées sur
votre compte Claude, et non sur votre ordinateur : le skill vous le dit avant d'écrire la moindre
date, et c'est à vous de décider.
Sources : https://support.claude.com/en/articles/12512180-use-skills-in-claude,
https://support.claude.com/en/articles/12512198-how-to-create-custom-skills,
https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork,
https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview et
https://code.claude.com/docs/en/skills

### Hermes

```bash
mkdir -p ~/.hermes/skills
unzip ~/Downloads/ca-arrive.zip -d ~/.hermes/skills/
```

Avec un profil nommé, le dossier est `~/.hermes/profiles/<nom>/skills/`. En ligne de commande,
lancez Hermes depuis le dossier privé (`mkdir -p ~/.ca-arrive && cd ~/.ca-arrive && hermes`), pour
que « tout effacer » retrouve ses conversations, puis tapez `/ca-arrive` ; depuis votre messagerie,
tapez simplement `/ca-arrive`. Hermes peut réécrire ses skills
et sa mémoire de lui-même : au premier lancement, le skill vous propose d'activer l'approbation des
modifications (`skills.write_approval`, `memory.write_approval`).
Source : https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md

### OpenClaw

```bash
mkdir -p ~/.agents/skills
unzip ~/Downloads/ca-arrive.zip -d ~/.agents/skills/
```

Ou, pour tous vos agents locaux, depuis le dossier où vous avez décompressé le ZIP :
`openclaw skills install ./ca-arrive --global`. Tapez ensuite `$ca-arrive` (dans une messagerie
reliée : `/ca_arrive` ou `/skill ca-arrive`), de préférence dans un fil incognito (interface Control
UI, écran New thread, option Incognito) : la conversation n'est alors pas écrite sur le disque. Au
premier lancement, le skill vous propose d'ajouter `disable-model-invocation: true` à son en-tête,
pour qu'OpenClaw ne le lance qu'à votre demande.
Sources : https://docs.openclaw.ai/tools/skills et https://docs.openclaw.ai/tools/slash-commands

### Un autre agent

Consultez la documentation de votre agent pour savoir où ranger un skill au format Agent Skills.
Le skill vous dira franchement ce qu'il ne sait pas de votre agent.

## Python (conseillé)

`python3 --version` doit répondre. Sans Python, la saisie et la capture fonctionnent quand même ;
l'option « export » de votre appli n'est alors pas disponible.

## Si le skill n'apparaît pas

Vérifiez que le fichier `ca-arrive/SKILL.md` est bien dans le dossier indiqué (et non dans un
sous-dossier en trop, comme `ca-arrive-main/ca-arrive/`), puis relancez votre agent.

## Désinstaller

Lancez le skill avec « tout effacer » et suivez ses indications, puis supprimez le dossier
`ca-arrive/` des skills de votre agent (ou retirez-le de Customize > Skills dans Cowork).

## Licence

MIT : voir `LICENSE.txt` et le résumé en français, section « Licence, garantie et responsabilité »
de `README.md`.
