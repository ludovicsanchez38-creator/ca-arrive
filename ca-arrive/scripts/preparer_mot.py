#!/usr/bin/env python3
"""Remplit un gabarit du skill ca-arrive, sur votre ordinateur, sans rien envoyer.

Usage :
  preparer_mot.py --ambiance douceur|complice|franc|cash --valeurs valeurs.json --dossier <dossier> [--eml]

valeurs.json (UTF-8) :
  {
    "prenom": "Alex",                          # prénom ou surnom de la personne
    "salutation": "Mon cœur,",                 # facultatif : sinon, formule de l'ambiance
    "annonce": "Mes règles arrivent vers mardi.",
    "cases": ["La bouillotte sortie du placard", "..."],
    "mots_interdits": ["« Calme-toi. »"],      # liste vide : la rubrique disparaît
    "mot_perso": "",                           # facultatif : une phrase à vous
    "signature": "Camille",
    "objet": "Ça arrive. Prépare-toi.",        # facultatif
    "ouverture": "...",                        # facultatif : phrases de l'ambiance (voir
    "apres_mots": "...",                       # assets/templates/phrases.json). Absente, null ou
    "merci": "...",                            # "par défaut" : la phrase de l'ambiance. "" ou
    "fin": "...",                              # "aucune" : la phrase est retirée. Sinon : votre
    "apercu": "..."                            # texte à la place (apercu : texte d'aperçu du .eml).
  }

Produit dans <dossier> : mot-<ambiance>.html (à ouvrir dans le navigateur puis copier-coller
dans un nouveau message), mot-<ambiance>.txt (version texte, pour un SMS ou une messagerie
sans mise en forme) et, avec --eml, mot-<ambiance>.eml (brouillon à ouvrir, selon les logiciels).
Aucune adresse n'est écrite nulle part : c'est vous qui choisissez à qui l'écrire et qui envoyez.
Bibliothèque standard seulement (Python 3.8 ou plus récent).
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from email.message import EmailMessage
from pathlib import Path

GABARITS = Path(__file__).resolve().parents[1] / "assets" / "templates"
AMBIANCES = ("douceur", "complice", "franc", "cash")
OBJET_DEFAUT = "Ça arrive. Prépare-toi."
SALUTATIONS = {"douceur": "Mon cœur,", "complice": "Salut {p},", "franc": "{p},", "cash": "{p}."}
PHRASES = ("ouverture", "apres_mots", "merci", "fin", "apercu")
NEANT = {"", "aucun", "aucune", "par defaut", "par défaut"}
# Les accolades saisies par l'utilisatrice sont mises de côté pendant le remplissage, pour qu'aucune
# valeur ne soit prise pour un marqueur du gabarit, puis rendues à la fin.
PROTEGE = str.maketrans({"{": "", "}": ""})
RENDU = str.maketrans({"": "{", "": "}"})


def _texte(valeur) -> str:
    """Une chaîne propre ; None, « aucune » ou « par défaut » donnent une chaîne vide."""
    if valeur is None:
        return ""
    texte = str(valeur).strip()
    return "" if texte.lower().strip(" .") in NEANT else texte


def _liste(valeur) -> list[str]:
    """Une liste de lignes : accepte une liste ou un texte à plusieurs lignes, et écarte « aucun »."""
    if valeur is None:
        return []
    if isinstance(valeur, str):
        elements = valeur.splitlines()
    elif isinstance(valeur, (list, tuple)):
        elements = list(valeur)
    else:
        elements = [str(valeur)]
    return [t for t in (_texte(re.sub(r"^\s*[-•*]\s*", "", str(e))) for e in elements if e is not None) if t]


def _insecables(texte: str) -> str:
    """Espaces insécables de la typographie française (un « » » ne finit jamais seul en ligne)."""
    for avant, apres in ((" »", "&nbsp;»"), ("« ", "«&nbsp;"), (" ?", "&nbsp;?"), (" !", "&nbsp;!"),
                         (" :", "&nbsp;:"), (" ;", "&nbsp;;")):
        texte = texte.replace(avant, apres)
    return texte


def _bloc(texte: str, nom: str, elements: list[str], marqueur: str, preparer) -> str:
    """Répète le contenu du bloc <!--NOM-->...<!--/NOM--> pour chaque élément, ou le retire."""
    motif = re.compile(rf"<!--{nom}-->(.*?)<!--/{nom}-->", re.S)

    def remplacer(m: re.Match) -> str:
        return "".join(m.group(1).replace(marqueur, preparer(e)) for e in elements)

    return motif.sub(remplacer, texte)


def phrases_de(ambiance: str, v: dict) -> dict[str, str]:
    """Phrases de l'ambiance : gardées (absentes, null, « par défaut »), remplacées ou retirées."""
    defaut = json.loads((GABARITS / "phrases.json").read_text(encoding="utf-8-sig"))[ambiance]
    phrases = {}
    for cle in PHRASES:
        brut = v.get(cle)
        garder = brut is None or str(brut).strip().lower().strip(" .") in ("par defaut", "par défaut")
        phrases[cle] = _texte(defaut.get(cle)) if garder else _texte(brut)
    return phrases


def remplir(modele: str, v: dict, ambiance: str, en_html: bool) -> str:
    if en_html:
        def preparer(s: str) -> str:
            return _insecables(html.escape(s.translate(PROTEGE), quote=False))
    else:
        def preparer(s: str) -> str:
            return s.translate(PROTEGE)
    texte = re.sub(r"<!-- Gabarit.*?-->\n?", "", modele, flags=re.S)  # note de fabrication, inutile à la personne qui reçoit le mot
    inconnus = set(re.findall(r"\{\{([A-Z_]+)\}\}", texte)) - {
        "OBJET", "TITRE", "SALUTATION", "ANNONCE", "SIGNATURE", "CASE", "MOT", "MOT_PERSO",
        "OUVERTURE", "APRES_MOTS", "MERCI", "FIN", "APERCU"}
    if inconnus:
        raise ValueError(f"marqueurs inconnus dans le gabarit : {', '.join(sorted(inconnus))}")

    phrases = phrases_de(ambiance, v)
    mots = _liste(v.get("mots_interdits"))
    cases = _liste(v.get("cases"))
    perso = _texte(v.get("mot_perso"))
    # Une rubrique vide disparaît entière, titre compris.
    texte = re.sub(r"<!--MOTS_INTERDITS-->(.*?)<!--/MOTS_INTERDITS-->",
                   lambda m: m.group(1) if mots else "", texte, flags=re.S)
    texte = re.sub(r"<!--CHECKLIST-->(.*?)<!--/CHECKLIST-->", lambda m: m.group(1) if cases else "",
                   texte, flags=re.S)
    texte = _bloc(texte, "MOT", mots, "{{MOT}}", preparer)
    texte = _bloc(texte, "CASES", cases, "{{CASE}}", preparer)
    texte = _bloc(texte, "MOT_PERSO", [perso] if perso else [], "{{MOT_PERSO}}", preparer)
    for cle, marqueur in (("ouverture", "OUVERTURE"), ("apres_mots", "APRES_MOTS"), ("merci", "MERCI"), ("fin", "FIN")):
        texte = _bloc(texte, marqueur, [phrases[cle]] if phrases[cle] else [], "{{" + marqueur + "}}", preparer)

    salutation = _texte(v.get("salutation")) or SALUTATIONS[ambiance].format(p=_texte(v.get("prenom")))
    objet = _texte(v.get("objet")) or OBJET_DEFAUT
    # Titre affiché : les mots à trait d'union ne se coupent pas (« Prépare-toi » reste entier).
    # <wbr> devant et derrière : le copier-coller change en espaces insécables les espaces qui touchent le
    # span, le titre garde donc un point de coupure de chaque côté.
    titre = (re.sub(r"(\S*-\S*)( ?)", r'<wbr><span style="white-space:nowrap;">\1</span>\2<wbr>', preparer(objet))
             if en_html else preparer(objet))
    valeurs = {
        "TITRE": titre,
        "OBJET": preparer(objet),
        "SALUTATION": preparer(salutation),
        "ANNONCE": preparer(_texte(v.get("annonce"))),
        "SIGNATURE": preparer(_texte(v.get("signature"))),
        "APERCU": preparer(phrases["apercu"]),
    }
    texte = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: valeurs.get(m.group(1), m.group(0)), texte)
    reste = re.findall(r"\{\{[A-Z_]+\}\}|<!--/?[A-Z_]+-->", texte)
    if reste:
        raise ValueError(f"marqueurs non remplis : {', '.join(sorted(set(reste)))}")
    return texte.translate(RENDU)


def main(argv: list[str] | None = None) -> int:
    os.umask(0o077)  # le mot et ses valeurs ne sont lisibles que par son compte
    analyseur = argparse.ArgumentParser(description="Remplit un gabarit du mot, sans rien envoyer.")
    analyseur.add_argument("--ambiance", required=True, choices=AMBIANCES)
    analyseur.add_argument("--valeurs", required=True, type=lambda s: Path(s).expanduser())
    analyseur.add_argument("--dossier", required=True, type=lambda s: Path(s).expanduser())
    analyseur.add_argument("--eml", action="store_true", help="produit aussi un brouillon .eml")
    args = analyseur.parse_args(argv)

    try:
        valeurs = json.loads(args.valeurs.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as erreur:
        print(f"valeurs_illisibles: {erreur}")
        return 1
    if not isinstance(valeurs, dict):
        print("valeurs_illisibles: un objet JSON entre accolades est attendu")
        return 1
    manquants = [c for c in ("annonce", "signature") if not _texte(valeurs.get(c))]
    if not _texte(valeurs.get("salutation")) and not _texte(valeurs.get("prenom")) and args.ambiance != "douceur":
        manquants.append("prenom")
    if manquants:
        print(f"valeurs_manquantes: {', '.join(manquants)}")
        return 1
    modele_html = (GABARITS / f"{args.ambiance}.html").read_text(encoding="utf-8")
    modele_txt = (GABARITS / f"{args.ambiance}.txt").read_text(encoding="utf-8")
    page = remplir(modele_html, valeurs, args.ambiance, en_html=True)
    texte = remplir(modele_txt, valeurs, args.ambiance, en_html=False)
    texte = re.sub(r"[ \t]+\n", "\n", texte)
    texte = re.sub(r"\n{3,}", "\n\n", texte).strip() + "\n"

    args.dossier.mkdir(parents=True, exist_ok=True)
    base = args.dossier / f"mot-{args.ambiance}"
    base.with_suffix(".html").write_text(page, encoding="utf-8")
    base.with_suffix(".txt").write_text(texte, encoding="utf-8")
    print(f"html: {base.with_suffix('.html')}")
    print(f"texte: {base.with_suffix('.txt')}")
    if args.eml:
        message = EmailMessage()
        message["Subject"] = _texte(valeurs.get("objet")) or OBJET_DEFAUT
        message["X-Unsent"] = "1"  # demande d'ouverture en brouillon, respectée par certains logiciels seulement
        message.set_content(texte)
        message.add_alternative(page, subtype="html")
        base.with_suffix(".eml").write_bytes(message.as_bytes())
        print(f"eml: {base.with_suffix('.eml')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
