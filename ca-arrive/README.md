# Ça arrive (bêta) : le mot qui prévient, quelques jours avant

## Ce qu'il fait

Quand vos règles approchent, votre agent vous prépare un mot pour la personne qui partage votre
vie, votre conjoint ou votre conjointe. Il vous pose une question de sécurité et deux questions (son
prénom, votre signature), puis ouvre dans votre messagerie un nouveau mail déjà mis en page, aux
couleurs de l'ambiance choisie. Vous ajoutez l'adresse, vous relisez (tout se retouche dans le
brouillon), et vous l'envoyez vous-même. Sur téléphone ou dans une session en ligne, le mail part en
version texte, qui s'ouvre d'un toucher dans votre messagerie. Le mot est écrit à la première
personne et signé de votre nom, avec vos mots. Les questions arrivent une à la fois, avec des
réponses à choix : un toucher ou un chiffre suffit.

En bonus, si votre agent tourne sur votre ordinateur, il peut noter vos dates, estimer celle de vos
prochaines règles et vous dire à partir de quel jour relancer le skill (un rappel à l'intitulé neutre
dans votre agenda suffit) : il ne tourne pas en arrière-plan. Si vos cycles varient beaucoup d'un
mois à l'autre, il n'estime rien et ne porte aucun jugement : il vous montre la durée de vos derniers
cycles, vous demande s'il manque une date ou s'il y en a une de trop, et prépare le mot le jour où
vous le lui demandez.

Le mot contient une petite liste à cocher (la tisane, la bouillotte prête, « câlin ou paix royale :
demande lequel »...) et une rubrique **« mots interdits cette semaine »**, avec une touche d'humour,
de « T'as tes règles ou quoi ? » à « T'as une petite mine. » Chaque ligne se retire dans le
brouillon, ou en le demandant à votre agent, et la rubrique disparaît si vous n'en voulez pas. Ces listes de départ
s'appuient sur des études, des témoignages de femmes et des articles de conseil,
dont certains publiés par des marques, sur ce qui aide et ce qui blesse avant et pendant les règles :
les sources, avec leur nature, sont dans `references/sources.md`.

Quatre ambiances au choix, avec leur aperçu dans `assets/apercus/` : **douceur** (couleurs tendres,
formes arrondies, ton câlin), **complice** (chaleureux et drôle), **franc** (net et bienveillant) et
**cash** (sobre, contrasté, direct et drôle). Chaque ambiance a quelques phrases toutes prêtes (une
ouverture, une phrase sous les mots interdits, un remerciement et, pour douceur et complice, une
formule avant la signature) : vous les gardez, les changez ou les retirez.

## Avec votre agent

Le skill suit le format ouvert Agent Skills. Il fonctionne avec les agents qui le lisent et qui
peuvent lancer des commandes :

| Agent | Où placer le dossier `ca-arrive/` | Pour le lancer |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `/ca-arrive` |
| Codex | `~/.agents/skills/` | `$ca-arrive` |
| Cowork | téléversez le ZIP dans Customize > Skills | « Utilise le skill ca-arrive » |
| Hermes | `~/.hermes/skills/` | `/ca-arrive` |
| OpenClaw | `~/.agents/skills/` | `$ca-arrive` |
| Un autre agent | consultez la documentation de votre agent | « Utilise le skill ca-arrive » |

Une version de travail (1.1) a été testée en conditions réelles sous Codex le 25/09/2026, et la 1.2
dans l'app Claude le même jour ; la 1.4 en tire une conversation plus courte et le brouillon mis en
page qui s'ouvre sur l'ordinateur. Essayée sur un vrai Mac le 26/09/2026, elle ouvrait bien le
brouillon dans Mail, mais seulement par la voie de secours quand Safari était fermé : la 1.5 lance
Safari elle-même. Pas encore testé sous Windows. Pour les
autres agents, le skill suit leur documentation officielle. Le détail, agent par agent, est dans
`INSTALL.md`. Pour Claude Code, Codex et Hermes, lancez l'agent depuis le dossier privé du skill
(`mkdir -p ~/.ca-arrive && cd ~/.ca-arrive && claude`, ou `codex`, ou `hermes`) : « tout effacer »
saura retrouver ces conversations.

## Au fil des mois

Si vous avez choisi le suivi, le jour où vos règles arrivent, lancez le skill avec « c'est arrivé
aujourd'hui » (ou « hier ») : il note la date, et la prochaine estimation en tient compte. Pour estimer la date suivante, il lui faut
au moins trois dates, ou la durée habituelle de votre cycle que votre appli affiche. Avec « le mot maintenant », il prépare le mot
tout de suite ; avec « réglages », vous changez l'ambiance, les listes ou le délai ; « pause » et
« reprendre » font ce qu'ils disent.

## Ce qu'il ne fait jamais

- **Il n'envoie rien**, et ne dépose aucun brouillon dans votre messagerie. Il ne cherche aucune
  adresse. Le mot reste chez vous jusqu'à ce que vous l'envoyiez.
- **Il attend que vous l'appeliez.** Sa description dit à votre agent d'attendre que vous
  l'appeliez par son nom. Codex l'impose d'office, grâce à un réglage livré avec le skill ; pour
  Claude Code et OpenClaw, le skill vous propose au premier lancement un réglage équivalent ; pour
  Cowork et Hermes, seule sa description le demande.
- **Il ne donne pas d'avis** sur votre humeur, votre santé ou vos capacités.
- **Ce n'est pas un outil médical.** La date qu'il calcule est une estimation. Il ne diagnostique
  rien et ne sert ni à la contraception ni à un projet de grossesse.
- **Il ne suit que votre cycle**, jamais celui de quelqu'un d'autre.

## Vos dates, si vous choisissez le suivi : trois façons, au choix

Sans suivi, le skill ne vous demande aucune date. Avec, ces dates sont des données de santé au sens
du RGPD (article 9). Elles restent dans un fichier privé
sur votre ordinateur, dans le dossier `~/.ca-arrive`, hors de tout dépôt Git et de tout dossier synchronisé.
Dans une session qui tourne dans le cloud, comme celles de Cowork par défaut, le skill ne note
aucune date et ne propose pas de suivi. Avec un agent installé sur un serveur que vous joignez par
une messagerie, le fichier serait sur ce serveur : le skill vous le dit avant d'écrire la moindre
date.

Sur un ordinateur ou un compte d'agent que quelqu'un d'autre utilise avec vous ou administre (un
poste ou un abonnement fourni par votre employeur, par exemple), d'autres peuvent accéder à ces
dates : le skill n'est pas fait pour ce cas, et il vous pose la question au premier lancement.

| Vous choisissez | Ce que l'agent lit | Par où ça passe | Ce qui reste chez vous |
|---|---|---|---|
| **Vous tapez vos dates** (proposé par défaut) | Les dates que vous tapez | Le modèle d'IA de votre agent, en général dans le cloud, comme tout ce que vous lui écrivez | Votre fichier de dates, et la trace de la conversation que garde votre agent |
| **Vous montrez une capture** de votre appli | L'image entière : recadrez sur le calendrier | Le modèle d'IA, image comprise | Votre capture et la copie éventuelle qu'en garde votre agent (à supprimer ensuite), et les seules dates que vous confirmez |
| **Vous passez par l'export** de votre appli (Apple Santé, Clue, Flo) | Seulement les premiers jours, qu'un petit programme extrait sur votre ordinateur | Le modèle d'IA, pour ces seules dates | L'export complet, qui ne quitte pas votre ordinateur (à supprimer ensuite), et votre fichier de dates. Cette façon n'est proposée que si votre agent tourne sur votre ordinateur |

Si vous parlez à votre agent par une messagerie (Telegram, WhatsApp...), la conversation passe aussi
par ses serveurs. Le détail par application est dans `references/exports.md`, et ce que chaque agent
conserve, avec ses réglages, dans `references/confidentialite.md`.

## Envoyer le mot

**Sur votre ordinateur**, votre agent ouvre un nouveau message déjà mis en page, avec l'objet (« Ça
arrive. Prépare-toi. ») et sans destinataire : ajoutez l'adresse, relisez, envoyez.

- Sur Mac, il passe par Safari (qu'il ouvre lui-même s'il était fermé), qui confie la page à Mail
  (comme le bouton Partager, puis Mail, au format « Page web ») ; la première fois, macOS vous demande
  sans doute d'autoriser votre agent à piloter Safari et Mail. Si ce chemin échoue, Mail ouvre un
  message vide avec l'objet et le mot est dans le presse-papiers, à la place de ce que vous y aviez
  copié : cliquez dans le corps du message puis Cmd+V. Si vous enregistrez le
  brouillon dans Mail, il devrait vous attendre aussi dans Mail sur votre iPhone, selon votre compte.
- Sous Windows, il ouvre un brouillon `.eml` : Outlook l'ouvre modifiable, prêt à envoyer ; d'autres
  messageries l'ouvrent comme un message reçu, et votre agent vous donne alors la version texte.
- Sous Linux, le même `.eml`, selon votre messagerie.

Le skill ne remplit jamais le destinataire et n'envoie jamais rien.

**Sur téléphone ou dans une session en ligne** (app Claude, ChatGPT, messagerie), le mail part en
texte : votre agent vous donne un lien qui ouvre votre messagerie avec l'objet et le mot déjà
écrits, et le texte en clair, à copier au besoin. Pour la version mise en page, lancez le skill sur
votre ordinateur.

L'annonce (« vers mardi », « sans doute demain ») est calculée pour le jour où le mot est préparé : si
vous l'envoyez un autre jour, relancez d'abord le skill, il la met à jour.

Pour un message WhatsApp, collez la version texte que votre agent vous donne, telle quelle.

## Arrêter, tout effacer

Lancez le skill avec « pause » pour le suspendre, ou avec « tout effacer » : il supprime vos dates et
vos mots. Votre agent garde aussi, de son côté, la trace de vos conversations. Le skill vous donne la
procédure connue pour l'effacer (Claude Code, Codex, Hermes, OpenClaw, Cowork) et signale ce qui n'a
pas pu être vérifié. Il vous dit aussi franchement ce qu'il ne peut pas effacer : ce que le
fournisseur du modèle conserve selon votre compte, et les mots déjà envoyés, qui vivent dans votre
messagerie.

## Vos données et Synoptïa

Le skill ne transmet rien à Synoptïa : tout se passe entre vous, votre ordinateur, votre agent, le fournisseur du modèle d'IA qu'il utilise et, si vous
parlez à votre agent par une messagerie, cette messagerie.

Si vous l'avez téléchargé sur espace.synoptia.fr, nous connaissons l'adresse e-mail de votre compte,
et les journaux techniques de l'espace gardent douze mois au plus la trace de ce téléchargement,
avec l'adresse IP et le navigateur utilisés. Si vous demandez la suppression de votre compte, votre
adresse e-mail est effacée et, si vous le précisez dans la même demande, la trace de téléchargement
liée à votre compte aussi ; les autres traces techniques, qui ne portent pas votre adresse e-mail,
s'effacent au plus tard au bout de douze mois. Pour ces demandes, comme pour vos autres droits
(accès, rectification), écrivez à ludo@synoptia.fr, comme l'indiquent nos mentions légales. Le même skill est public sur GitHub, où il
se télécharge sans compte chez nous.

## Pourquoi il est offert

Il est offert pour circuler le plus largement possible : chacune le prend tel quel ou l'adapte à sa
façon.

## Licence, garantie et responsabilité

Ce skill est distribué gratuitement sous licence MIT (texte officiel en anglais dans `LICENSE.txt`).
Elle couvre tout le contenu créé pour ce skill : code, textes, gabarits et aperçus. Les courtes
citations reprises dans `references/sources.md` restent à leurs auteurs. En résumé : vous pouvez
l'utiliser, le copier, le modifier et le partager, y compris à des fins commerciales, à condition de
garder la mention de copyright et la licence. Il est fourni « tel quel », sans garantie, notamment
sur l'exactitude de la date calculée, qui n'est qu'une estimation. Le texte officiel exclut aussi la
responsabilité des auteurs et du titulaire des droits (SYNOPTIA). Si vous l'utilisez à titre
personnel, ni cette absence de garantie ni cette exclusion ne limitent les droits que vous tenez du
Code de la consommation, ni votre droit à réparation d'un dommage causé par un manquement de
Synoptïa ; pour un usage professionnel, elles s'appliquent dans la mesure permise par la loi.

Les noms d'agents, d'applications et de produits cités (Claude Code, Cowork, Codex, Hermes, OpenClaw,
Apple Santé, Clue, Flo, Nutella) sont des marques de leurs titulaires. Ce skill n'est affilié à aucun
d'eux ni approuvé par eux.

## Éditeur

Synoptïa (SYNOPTIA, SARL à associé unique au capital de 5 000 €, RCS Manosque 991 606 781).
Contact : ludo@synoptia.fr. Mentions légales, dont le directeur de la publication :
https://synoptia.fr/mentions-legales
