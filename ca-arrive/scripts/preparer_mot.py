#!/usr/bin/env python3
"""Remplit un gabarit du skill ca-arrive, sur votre ordinateur, sans rien envoyer.

Usage :
  preparer_mot.py --ambiance douceur|complice|franc|cash --valeurs valeurs.json --dossier <dossier> [--eml]

valeurs.json (UTF-8) :
  {
    "prenom": "Alex",                          # prénom ou surnom de la personne
    "salutation": "Mon cœur,",                 # facultatif : sinon, formule de l'ambiance
    "annonce": "Mes règles arrivent vers mardi.",  # ou, à la place : "annonce_debut" (« Ça arrive »,
                                               # « Mes règles arrivent »...) et "annonce_moment" (« bientôt »)
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

Produit dans <dossier> : mot-<ambiance>.html (le mail mis en page, styles en ligne, dont le <title>
est l'objet), mot-<ambiance>.txt (version texte, pour un SMS ou une messagerie sans mise en forme)
et, avec --eml, mot-<ambiance>.eml (brouillon à ouvrir, selon les logiciels). Affiche enfin un lien
mailto: sans destinataire (objet et version texte), pour le téléphone, ou « trop_long » s'il
dépasse 1 800 caractères. Pour ouvrir le brouillon mis en page sur l'ordinateur :
scripts/ouvrir_brouillon.py.
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
from urllib.parse import quote

GABARITS = Path(__file__).resolve().parents[1] / "assets" / "templates"
AMBIANCES = ("douceur", "complice", "franc", "cash")
OBJET_DEFAUT = "Ça arrive. Prépare-toi."
SALUTATIONS = {"douceur": "Mon cœur,", "complice": "Salut {p},", "franc": "{p},", "cash": "{p}."}
PHRASES = ("ouverture", "apres_mots", "merci", "fin", "apercu")
NEANT = {"", "aucun", "aucune", "par defaut", "par défaut"}
# Un lien mailto: plus long se coupe dans certaines messageries : au-delà, le copier-coller prend le relais.
LIMITE_LIEN = 1800
# Laissés tels quels dans le lien (RFC 6068) ; tout le reste est encodé en UTF-8, y compris « + », que
# certaines messageries lisent comme une espace, et les parenthèses, qui couperaient un lien Markdown.
SURS_MAILTO = ",;:@!"
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


def lien_mailto(objet: str, corps: str) -> str:
    """Lien mailto: sans destinataire, qui ouvre le mail tout prêt (objet et corps en texte).

    Objet et corps sont encodés en UTF-8, les espaces en %20 et les sauts de ligne en %0D%0A, comme le
    demande la RFC 6068 : accents, guillemets français et retours à la ligne arrivent intacts.
    """
    corps = corps.replace("\r\n", "\n").replace("\r", "\n").strip("\n").replace("\n", "\r\n")
    return "mailto:?subject=" + quote(objet.strip(), safe=SURS_MAILTO) + "&body=" + quote(corps, safe=SURS_MAILTO)


def annonce_de(v: dict) -> str:
    """L'annonce telle quelle, ou bâtie : « Ça arrive » + « bientôt » + point."""
    annonce = _texte(v.get("annonce"))
    if annonce:
        return annonce
    debut, moment = _texte(v.get("annonce_debut")), _texte(v.get("annonce_moment"))
    if not debut:
        return ""
    if not moment:
        return debut if re.search(r"[.!?…]$", debut) else debut + "."
    return re.sub(r"[\s.]+$", "", debut) + " " + moment + "."


def ecrire_eml(chemin: Path, objet: str, texte: str, page: str) -> Path:
    """Brouillon .eml sans destinataire : version texte et version mise en page, marqué « non envoyé ».

    L'en-tête X-Unsent demande l'ouverture en brouillon modifiable : Outlook le respecte, d'autres
    messageries ouvrent le fichier comme un message reçu.
    """
    message = EmailMessage()
    message["Subject"] = objet
    message["X-Unsent"] = "1"
    message.set_content(texte)
    message.add_alternative(page, subtype="html")
    # Lisible par son seul compte, quel que soit le masque de création du processus qui l'appelle.
    with os.fdopen(os.open(chemin, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "wb") as fichier:
        fichier.write(message.as_bytes())
    os.chmod(chemin, 0o600)
    return chemin


def corps_du_mail(texte: str, objet: str) -> str:
    """La version texte sans sa première ligne quand c'est l'objet, déjà porté par le lien."""
    premiere, _, reste = texte.lstrip("\n").partition("\n")
    return reste.strip("\n") if premiere.strip() == objet.strip() else texte.strip("\n")


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
        "ANNONCE": preparer(annonce_de(v)),
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
    manquants = [c for c in ("signature",) if not _texte(valeurs.get(c))]
    if not annonce_de(valeurs):
        manquants.insert(0, "annonce")
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
    objet = _texte(valeurs.get("objet")) or OBJET_DEFAUT
    lien = lien_mailto(objet, corps_du_mail(texte, objet))
    print(f"longueur_lien: {len(lien)} (limite {LIMITE_LIEN})")
    print(f"lien_envoi: {lien if len(lien) <= LIMITE_LIEN else 'trop_long'}")
    if args.eml:
        print(f"eml: {ecrire_eml(base.with_suffix('.eml'), objet, texte, page)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
