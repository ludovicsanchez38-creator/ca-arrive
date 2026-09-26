#!/usr/bin/env python3
"""Ouvre, sur l'ordinateur où il tourne, un nouveau mail déjà mis en page avec le mot, sans destinataire.

Usage :
  ouvrir_brouillon.py --html <dossier>/mot-<ambiance>.html [--texte <dossier>/mot-<ambiance>.txt]
                      [--voie auto|safari|presse-papiers|eml]

Le mot vient de preparer_mot.py. Ce script n'envoie jamais rien, n'écrit aucune adresse et ne simule
aucune frappe : c'est elle qui ajoute le destinataire, relit et envoie.

Les voies, dans l'ordre de « auto » :
- macOS, « safari » : Safari est lancé (open -a Safari) s'il était fermé, ouvre le .html, puis sa
  commande AppleScript « email contents » crée dans
  Mail un nouveau message avec le contenu de la page (le format « Page web » de Mail garde la mise en
  page), l'objet étant le titre de la page.
- macOS, « presse-papiers », si la première échoue : le mail mis en page (HTML) et sa version texte vont
  dans le presse-papiers, puis Mail ouvre un nouveau message avec l'objet ; elle y colle le mail (Cmd+V).
  Ce qui se trouvait dans le presse-papiers est remplacé, et la ligne « detail » le dit, avec la raison
  pour laquelle la voie Safari a été écartée.
- Windows et Linux, « eml » : un .eml marqué non envoyé (X-Unsent: 1), ouvert avec la messagerie par
  défaut. Outlook l'ouvre en brouillon modifiable ; d'autres messageries l'ouvrent comme un message reçu.

Affiche « etat: ouvert_mail_safari », « etat: ouvert_mail_presse_papiers », « etat: eml_ouvert » ou
« etat: echec », puis une ligne « detail: ». Code de sortie 0 si un brouillon s'est ouvert, 1 sinon.
Le chemin du fichier et l'objet passent en arguments d'osascript, jamais dans le texte des scripts.
Bibliothèque standard seulement (Python 3.8 ou plus récent).
"""

from __future__ import annotations

import argparse
import html
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # aucun __pycache__ dans le dossier du skill
sys.path.insert(0, str(Path(__file__).resolve().parent))
from preparer_mot import OBJET_DEFAUT, ecrire_eml  # noqa: E402

DELAI = 60  # secondes accordées à chaque commande osascript (le temps d'une autorisation macOS comprise)
VOIES = ("auto", "safari", "presse-papiers", "eml")

# Safari ouvre la page, attend qu'elle porte son titre (dix secondes au plus), puis la confie à Mail.
# Safari est lancé juste avant par « open -a Safari » : quand il était fermé, le premier « activate »
# renvoyait l'erreur -600 (« application pas ouverte »). On attend donc qu'il tourne et qu'il réponde.
SCRIPT_SAFARI = """on run argv
	set adresse to item 1 of argv
	set titre to item 2 of argv
	repeat 50 times
		if application "Safari" is running then exit repeat
		delay 0.2
	end repeat
	repeat 25 times
		try
			tell application "Safari" to activate
			exit repeat
		on error number -600
			delay 0.2
		end try
	end repeat
	tell application "Safari"
		activate
		set doc to make new document with properties {URL:adresse}
		repeat 50 times
			try
				if name of doc is titre then exit repeat
			end try
			delay 0.2
		end repeat
		delay 0.5
		email contents of doc
	end tell
end run
"""

# Le mail mis en page et sa version texte dans le presse-papiers (types public.html et texte).
SCRIPT_PRESSE_PAPIERS = """ObjC.import("AppKit");
function run(argv) {
	var presse = $.NSPasteboard.generalPasteboard;
	presse.clearContents;
	if (!presse.setStringForType($(argv[0]), "public.html")) { throw new Error("HTML refusé par le presse-papiers"); }
	if (argv.length > 1 && argv[1]) { presse.setStringForType($(argv[1]), "public.utf8-plain-text"); }
	return "ok";
}
"""

# Un nouveau message vide dans Mail, avec l'objet seul, affiché : elle y colle le mail.
SCRIPT_MAIL = """on run argv
	tell application "Mail"
		make new outgoing message with properties {subject:(item 1 of argv), visible:true}
		activate
	end tell
end run
"""


def objet_de(page: str) -> str:
    """L'objet du mail : le <title> du .html, entités décodées, ou l'objet par défaut."""
    m = re.search(r"<title>(.*?)</title>", page, re.S | re.I)
    objet = html.unescape(m.group(1)).strip() if m else ""
    return objet or OBJET_DEFAUT


def sans_apercu(page: str) -> str:
    """Le .html sans le texte d'aperçu caché, pour le presse-papiers : un collage pourrait l'afficher."""
    return re.sub(r'<div style="display:none;.*?</div>\n?', "", page, count=1, flags=re.S)


def _osascript(script: str, *arguments: str, langage: str = "AppleScript") -> tuple[bool, str]:
    """Lance un script osascript lu sur l'entrée standard, avec ses arguments. Rend (réussite, message)."""
    try:
        r = subprocess.run(["osascript", "-l", langage, "-", *arguments], input=script, text=True,
                           capture_output=True, timeout=DELAI, check=False)
    except (OSError, subprocess.TimeoutExpired) as erreur:
        return False, type(erreur).__name__
    message = (r.stderr or r.stdout or "").strip().splitlines()
    return r.returncode == 0, message[-1][:200] if message else ""


def _raison(message: str) -> str:
    if message.startswith("Safari ne s'est pas lancé"):  # déjà précis : ne pas le relire comme une erreur AppleScript
        return message
    if "-600" in message:
        return "Safari ne répondait pas encore (erreur -600, application pas ouverte)"
    if "-1743" in message or "not authorized" in message.lower() or "autoris" in message.lower():
        return ("autorisation refusée : Réglages Système > Confidentialité et sécurité > Automatisation, "
                "laisser votre agent piloter Safari et Mail")
    return message or "sans message"


def lancer_safari() -> tuple[bool, str]:
    """« open -a Safari », qui rend la main une fois Safari lancé (essai sur Mac du 26/09/2026 : sans lui,
    la voie Safari échouait toujours quand Safari était fermé)."""
    try:
        r = subprocess.run(["open", "-a", "Safari"], capture_output=True, text=True, timeout=DELAI, check=False)
    except (OSError, subprocess.TimeoutExpired) as erreur:
        return False, type(erreur).__name__
    return r.returncode == 0, (r.stderr or "").strip()[:200]


def voie_safari(chemin_html: Path, objet: str) -> tuple[bool, str]:
    ok, message = lancer_safari()
    if not ok:
        return False, f"Safari ne s'est pas lancé ({message or 'sans message'})"
    return _osascript(SCRIPT_SAFARI, chemin_html.resolve().as_uri(), objet)


def voie_presse_papiers(page: str, texte: str, objet: str) -> tuple[bool, str]:
    ok, message = _osascript(SCRIPT_PRESSE_PAPIERS, sans_apercu(page), texte, langage="JavaScript")
    if not ok:
        return False, message
    return _osascript(SCRIPT_MAIL, objet)


def ouvrir_fichier(chemin: Path, systeme: str) -> tuple[bool, str]:
    """Ouvre un fichier avec l'application par défaut du système, sans attendre qu'elle se ferme."""
    try:
        if systeme == "Windows":
            os.startfile(str(chemin))  # type: ignore[attr-defined]  # n'existe que sous Windows
            return True, ""
        commande = "open" if systeme == "Darwin" else "xdg-open"
        if not shutil.which(commande):
            return False, f"{commande} introuvable"
        r = subprocess.run([commande, str(chemin)], capture_output=True, text=True, timeout=DELAI, check=False)
        return r.returncode == 0, (r.stderr or "").strip()[:200]
    except (OSError, subprocess.TimeoutExpired, AttributeError) as erreur:
        return False, type(erreur).__name__


def ouvrir(chemin_html: Path, chemin_texte: Path | None, voie: str = "auto",
           systeme: str | None = None) -> tuple[str, str]:
    """Essaie les voies dans l'ordre et rend (etat, detail)."""
    systeme = systeme or platform.system()
    page = chemin_html.read_text(encoding="utf-8")
    texte = chemin_texte.read_text(encoding="utf-8") if chemin_texte and chemin_texte.is_file() else ""
    objet = objet_de(page)
    if voie == "auto":
        voies = ["safari", "presse-papiers"] if systeme == "Darwin" else ["eml"]
    else:
        voies = [voie]
    raisons = []
    for v in voies:
        if v in ("safari", "presse-papiers") and (systeme != "Darwin" or not shutil.which("osascript")):
            raisons.append(f"{v} : réservé à macOS")
            continue
        if v == "safari":
            ok, message = voie_safari(chemin_html, objet)
            if ok:
                return "ouvert_mail_safari", ("nouveau message ouvert dans Mail, mis en page, sans destinataire ; "
                                              "la page reste ouverte dans Safari")
        elif v == "presse-papiers":
            ok, message = voie_presse_papiers(page, texte, objet)
            if ok:
                detail = ("Le brouillon est ouvert : cliquez dans le corps du message puis Cmd+V. "
                          "Le mot est dans le presse-papiers, à la place de ce qui s'y trouvait avant.")
                if raisons:  # la voie Safari a été essayée et écartée : le dire, jamais en silence
                    detail += " Voie Safari écartée : " + " ; ".join(raisons) + "."
                return "ouvert_mail_presse_papiers", detail
        else:
            eml = ecrire_eml(chemin_html.with_suffix(".eml"), objet, texte or objet, page)
            ok, message = ouvrir_fichier(eml, systeme)
            if ok:
                return "eml_ouvert", f"{eml} ouvert avec la messagerie par défaut"
        raisons.append(f"{v} : {_raison(message)}")
    return "echec", " ; ".join(raisons) or "aucune voie"


def main(argv: list[str] | None = None) -> int:
    os.umask(0o077)  # le .eml n'est lisible que par son compte
    analyseur = argparse.ArgumentParser(description="Ouvre un nouveau mail mis en page avec le mot, sans rien envoyer.")
    analyseur.add_argument("--html", required=True, type=lambda s: Path(s).expanduser())
    analyseur.add_argument("--texte", type=lambda s: Path(s).expanduser(),
                           help="version texte (par défaut, le .txt à côté du .html)")
    analyseur.add_argument("--voie", choices=VOIES, default="auto")
    args = analyseur.parse_args(argv)
    if not args.html.is_file():
        print("etat: echec")
        print(f"detail: fichier introuvable : {args.html}")
        return 1
    etat, detail = ouvrir(args.html, args.texte or args.html.with_suffix(".txt"), args.voie)
    print(f"etat: {etat}")
    print(f"detail: {detail}")
    return 0 if etat != "echec" else 1


if __name__ == "__main__":
    sys.exit(main())
