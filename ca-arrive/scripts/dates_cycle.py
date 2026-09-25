#!/usr/bin/env python3
"""Outil local du skill ca-arrive.

Tout se passe sur votre ordinateur : ce programme n'ouvre aucune connexion.
Il n'affiche que des dates (les premiers jours de vos règles) et le résultat du
calcul, jamais le reste du contenu des fichiers qu'il lit. C'est ce qui permet
à votre agent de ne recevoir que ces dates, et pas tout votre export de santé.

Usage :
  dates_cycle.py calcul  <fichier-reglages> [--aujourdhui AAAA-MM-JJ]
  dates_cycle.py ajouter <fichier-reglages> <AAAA-MM-JJ | aujourdhui | hier>... [--aujourdhui AAAA-MM-JJ]
  dates_cycle.py effacer <dossier-prive>      (~/.ca-arrive : supprime reglages.md et les mots préparés)
  dates_cycle.py verifier <dossier-prive>     (~/.ca-arrive : le crée et vérifie qu'il n'est ni synchronisé ni dans Git)
  dates_cycle.py apple   <export.zip | export.xml> [--max 7]
  dates_cycle.py json   <fichier.json | archive.zip> [--max 7]
  dates_cycle.py liste  <fichier.txt> [--max 7]

Bibliothèque standard seulement (Python 3.8 ou plus récent).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

MAX_DATES = 7            # le calcul ne lit que les sept dates les plus récentes
MIN_DATES = 3            # en dessous, pas d'estimation (sauf durée habituelle)
ECART_MAX = 7            # au-delà, le cycle est jugé trop variable pour estimer
INTERVALLE_MIN = 15      # un intervalle hors de ces bornes signale une date
INTERVALLE_MAX = 60      # manquante ou en trop : on n'estime rien
DELAI_DEFAUT = 3
JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
NOUVELLE_PERIODE = 7     # plus de 7 jours sans saignement noté = nouvelle période

ISO = re.compile(r"^\s*(?:[-*]\s+)?(\d{4}-\d{2}-\d{2})\b")  # accepte « - 2026-09-14 »
DATE_AUTRE = re.compile(r"\d{1,4}[/.\-]\d{1,2}[/.\-]\d{1,4}")
DATE_DANS_TEXTE = re.compile(r"(\d{4}-\d{2}-\d{2})|(\d{1,2})[/.](\d{1,2})[/.](\d{4})")


def _sans_accents(texte: str) -> str:
    forme = unicodedata.normalize("NFD", texte)
    return "".join(c for c in forme if unicodedata.category(c) != "Mn").lower()


def _date_iso(texte: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(texte[:10])
    except ValueError:
        return None


def premiers_jours(jours: set[dt.date], debuts_marques: set[dt.date] | None = None) -> list[dt.date]:
    """Regroupe des jours de saignement en périodes et rend le premier jour de chacune."""
    debuts_marques = debuts_marques or set()
    debuts: list[dt.date] = []
    precedent: dt.date | None = None
    for jour in sorted(jours):
        if precedent is None or (jour - precedent).days > NOUVELLE_PERIODE:
            debuts.append(jour)
        elif jour in debuts_marques and debuts and debuts[-1] not in debuts_marques:
            # L'application a marqué ce jour comme début de cycle : on la croit.
            debuts[-1] = jour
        precedent = jour
    return debuts


def _afficher_debuts(debuts: list[dt.date], maximum: int) -> int:
    if not debuts:
        print("aucune_date_trouvee")
        return 1
    print("premiers_jours (du plus récent au plus ancien) :")
    for jour in sorted(debuts, reverse=True)[:maximum]:
        print(jour.isoformat())
    return 0


# ---------------------------------------------------------------- calcul

def _sections(chemin: Path) -> dict[str, list[str]]:
    """Découpe le fichier de réglages par titres (« # Dates », « # Délai »...), accents ignorés."""
    sections: dict[str, list[str]] = {}
    courante = ""
    for ligne in chemin.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        if ligne.startswith("#"):
            courante = _sans_accents(ligne.lstrip("#").strip())
            sections.setdefault(courante, [])
        else:
            sections.setdefault(courante, []).append(ligne)
    return sections


def _aide(lignes: list[str]) -> list[bool]:
    """Pour chaque ligne : aide entre parenthèses (même sur plusieurs lignes) ou citation ?
    Une ligne vide ou une ligne qui commence par une date referme toujours l'aide."""
    marques, profondeur = [], 0
    for ligne in lignes:
        texte = ligne.strip()
        if not texte or ISO.match(texte) or (profondeur == 0 and not texte.startswith("(")):
            profondeur = 0
            marques.append(texte.startswith(">"))
            continue
        marques.append(True)
        profondeur = max(profondeur + texte.count("(") - texte.count(")"), 0)
    return marques


def _utiles(lignes: list[str]) -> list[str]:
    """Lignes non vides, hors lignes d'aide entre parenthèses ou citées."""
    return [ligne.strip() for ligne, aide in zip(lignes, _aide(lignes)) if ligne.strip() and not aide]


def _dates(lignes: list[str]) -> tuple[list[dt.date], list[str]]:
    dates: list[dt.date] = []
    illisibles: list[str] = []
    for ligne in _utiles(lignes):
        trouve = ISO.match(ligne)
        jour = _date_iso(trouve.group(1)) if trouve else None
        if jour:
            dates.append(jour)
        elif trouve or DATE_AUTRE.search(ligne):
            illisibles.append(ligne)
    return dates, illisibles


def _entier(lignes: list[str]) -> int | None:
    for ligne in _utiles(lignes):
        trouve = re.search(r"\d+", ligne)
        if trouve:
            return int(trouve.group())
    return None


# Rubriques du mot : vides, elles n'ont pas encore été demandées. Une réponse comme « aucune » ou
# « par défaut » compte comme une réponse (elle a choisi de ne rien mettre).
A_DEMANDER = (("pour qui", "pour qui"), ("ambiance", "ambiance"), ("phrases de l", "phrases de l'ambiance"),
              ("salutation", "salutation"),
              ("comment le mot en parle", "comment le mot en parle"), ("check-list", "check-list"),
              ("mots interdits", "mots interdits"), ("ma phrase", "ma phrase à moi"),
              ("signature", "signature"))


def lire_reglages(chemin: Path) -> dict:
    sections = _sections(chemin)

    def section(prefixe: str) -> list[str]:
        return next((lignes for nom, lignes in sections.items() if nom.startswith(prefixe)), [])

    dates, illisibles = _dates(section("dates"))
    a_completer = [nom for prefixe, nom in A_DEMANDER if not _utiles(section(prefixe))]
    return {
        "vierge": not dates and not illisibles and len(a_completer) == len(A_DEMANDER),
        "a_completer": a_completer,
        "dates": dates,
        "illisibles": illisibles,
        "delai": _entier(section("delai")),
        "duree": _entier(section("duree habituelle")),
        "pause": bool(_utiles(section("pause")))
        and _sans_accents(re.sub(r"^[-*•]\s*", "", _utiles(section("pause"))[0])).startswith("oui"),
        "notes": _utiles(section("notes")),
    }


def _bloquant(r: dict, aujourdhui: dt.date) -> bool:
    """Affiche le statut et rend True si le fichier empêche tout calcul."""
    if r["pause"]:
        print("statut: pause")
        return True
    if r["illisibles"]:
        print("statut: date_illisible")
        for ligne in r["illisibles"]:
            print(f"ligne_a_corriger: {ligne}")
        return True
    futures = [d for d in r["dates"] if d > aujourdhui]
    if futures:
        print("statut: date_future")
        for d in futures:
            print(f"date_dans_le_futur: {d.isoformat()}")
        return True
    return False


def _delai(r: dict) -> int:
    delai = r["delai"]
    if delai is None or not 1 <= delai <= 14:
        print(f"delai_jours: {DELAI_DEFAUT} (réglage absent ou hors de 1 à 14, valeur par défaut)")
        return DELAI_DEFAUT
    print(f"delai_jours: {delai}")
    return delai


def _duree_moyenne(dates: list, duree: int | None) -> int | None:
    """Rend la durée de cycle retenue, ou None (le statut est alors déjà affiché)."""
    if len(dates) < MIN_DATES:
        if duree is None or not INTERVALLE_MIN <= duree <= INTERVALLE_MAX:
            print("statut: pas_assez_de_dates")
            return None
        print("base: duree_habituelle")
        return duree
    intervalles = [(a - b).days for a, b in zip(dates, dates[1:])]
    print("intervalles_jours: " + ", ".join(str(i) for i in intervalles))
    if any(i < INTERVALLE_MIN or i > INTERVALLE_MAX for i in intervalles):
        print("statut: intervalle_hors_bornes")
        return None
    ecart = max(intervalles) - min(intervalles)
    print(f"ecart_entre_cycles_jours: {ecart}")
    if ecart > ECART_MAX:
        # Seuil de l'outil, pas un avis médical : l'agent ne dit jamais « irrégulier ».
        print("statut: trop_variable")
        return None
    print("base: historique")
    n = len(intervalles)
    return (2 * sum(intervalles) + n) // (2 * n)  # arrondi, demi-jour vers le haut


def calcul(chemin: Path, aujourdhui: dt.date) -> int:
    print(f"aujourdhui: {aujourdhui.isoformat()}")
    if not chemin.exists():
        print("fichier: absent")
        print("statut: premier_lancement")
        return 0
    r = lire_reglages(chemin)
    if r["vierge"]:
        # Fichier vide, ou témoin aux rubriques vides : tout reste à demander. « present » dit à l'agent
        # que le fichier témoin a survécu d'une session à l'autre (test de persistance réussi).
        print("fichier: present")
        print("statut: premier_lancement")
        return 0
    if r["a_completer"]:
        print("a_completer: " + ", ".join(r["a_completer"]))
    if _bloquant(r, aujourdhui):
        return 0
    dates = sorted(set(r["dates"]), reverse=True)[:MAX_DATES]
    print(f"dates_lues: {len(dates)}")
    if not dates:
        print("statut: aucune_date")
        return 0
    delai = _delai(r)
    moyenne = _duree_moyenne(dates, r["duree"])
    if moyenne is None:
        return 0
    print(f"moyenne_jours: {moyenne}")

    estimee = dates[0] + dt.timedelta(days=moyenne)
    debut = estimee - dt.timedelta(days=delai)
    print(f"date_estimee: {estimee.isoformat()}")
    print(f"jour_date_estimee: {JOURS[estimee.weekday()]}")
    print(f"debut_fenetre: {debut.isoformat()}")
    print(f"jour_debut_fenetre: {JOURS[debut.weekday()]}")
    deja = any("mot" in _sans_accents(ligne) and estimee.isoformat() in ligne for ligne in r["notes"])
    print(f"mot_deja_prepare: {'oui' if deja else 'non'}")
    if aujourdhui < debut:
        print("statut: avant_fenetre")
        print(f"jours_avant_debut_fenetre: {(debut - aujourdhui).days}")
    elif aujourdhui <= estimee:
        print("statut: dans_fenetre")
        print(f"jours_avant_date_estimee: {(estimee - aujourdhui).days}")
        # Semaines du lundi au dimanche ; le délai (14 jours au plus) borne l'écart à deux semaines.
        semaines = ((estimee - dt.timedelta(days=estimee.weekday()))
                    - (aujourdhui - dt.timedelta(days=aujourdhui.weekday()))).days // 7
        print("semaine_date_estimee: " + ("cette_semaine", "semaine_prochaine", "dans_deux_semaines")[min(semaines, 2)])
    else:
        # Aucun décompte des jours écoulés : il inviterait à parler de « retard ».
        print("statut: date_estimee_passee")
    return 0


# ---------------------------------------------------------------- ajouter, effacer

def _lire_date(texte: str, aujourdhui: dt.date) -> dt.date | None:
    mot = _sans_accents(texte.strip()).replace("'", "").replace("\u2019", "")
    if mot == "aujourdhui":
        return aujourdhui
    if mot == "hier":
        return aujourdhui - dt.timedelta(days=1)
    trouve = ISO.match(texte.strip())
    return _date_iso(trouve.group(1)) if trouve else None


def ajouter(chemin: Path, entrees: list[str], aujourdhui: dt.date) -> int:
    """Ajoute des premiers jours sous « # Dates », sans doublon, les sept plus récents gardés."""
    nouvelles = []
    for entree in entrees:
        jour = _lire_date(entree, aujourdhui)
        if jour is None:
            print(f"date_illisible: {entree}")
            return 1
        if jour > aujourdhui:
            print(f"date_dans_le_futur: {jour.isoformat()}")
            return 1
        nouvelles.append(jour)
    nouvelles = sorted(set(nouvelles), reverse=True)
    lignes = chemin.read_text(encoding="utf-8-sig", errors="replace").splitlines() if chemin.exists() else []
    debut = next((i for i, ligne in enumerate(lignes)
                  if ligne.startswith("#") and _sans_accents(ligne.lstrip("#").strip()).startswith("dates")), None)
    if debut is None:
        lignes = ["# Dates", ""] + lignes
        debut = 0
    fin = next((i for i in range(debut + 1, len(lignes)) if lignes[i].startswith("#")), len(lignes))
    anciennes, illisibles = _dates(lignes[debut + 1:fin])
    if illisibles:
        print("statut: date_illisible")
        for ligne in illisibles:
            print(f"ligne_a_corriger: {ligne}")
        return 1
    # Deux jours à moins d'une semaine d'écart appartiennent à la même période : on ne garde que le
    # premier jour, et c'est à elle de dire lequel.
    proches = sorted({(n, a) for n in nouvelles if n not in anciennes for a in set(anciennes) | set(nouvelles)
                      if n != a and abs((n - a).days) <= NOUVELLE_PERIODE and (a in anciennes or a not in nouvelles or n > a)},
                     reverse=True)
    if proches:
        print("statut: meme_periode")
        for n, a in proches:
            print(f"meme_periode_que: {n.isoformat()} proche de {a.isoformat()}")
        return 1
    aide = [ligne for ligne, est_aide in zip(lignes[debut + 1:fin], _aide(lignes[debut + 1:fin])) if est_aide]
    autres = [ligne.strip() for ligne in lignes[debut + 1:fin]
              if ligne.strip() and ligne not in aide and not (ISO.match(ligne) and ISO.match(ligne).end() == len(ligne.rstrip()))]
    toutes = sorted(set(anciennes) | set(nouvelles), reverse=True)
    gardees, retirees = toutes[:MAX_DATES], toutes[MAX_DATES:]
    bloc = [lignes[debut], *aide, *(d.isoformat() for d in gardees), ""]
    resultat = lignes[:debut] + bloc + lignes[fin:]
    chemin.parent.mkdir(parents=True, exist_ok=True)
    _ecrire_atomique(chemin, "\n".join(resultat).rstrip("\n") + "\n")
    print("dates_enregistrees: " + ", ".join(d.isoformat() for d in gardees))
    if autres:
        print("lignes_retirees: " + " | ".join(autres))
    deja = sorted(set(nouvelles) & set(anciennes), reverse=True)
    if deja:
        print("deja_presentes: " + ", ".join(d.isoformat() for d in deja))
    if retirees:
        print("retirees_plus_de_sept: " + ", ".join(d.isoformat() for d in retirees))
    return 0


def _ecrire_atomique(chemin: Path, texte: str) -> None:
    """Écrit dans un fichier temporaire du même dossier (en 600), puis le met à la place de l'ancien."""
    fd, temporaire = tempfile.mkstemp(dir=chemin.parent, prefix=".reglages-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(texte)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(temporaire, 0o600)
        os.replace(temporaire, chemin)
    except BaseException:
        Path(temporaire).unlink(missing_ok=True)
        raise


FICHIERS_MOTS = (".html", ".txt", ".eml", ".json")


def effacer(dossier: Path) -> int:
    """Supprime reglages.md et les mots préparés. Laisse le dossier lui-même, vide."""
    if not dossier.is_dir():
        print(f"dossier_introuvable: {dossier}")
        return 1
    supprimes = []
    reglages = dossier / "reglages.md"
    if reglages.is_file():
        reglages.unlink()
        supprimes.append(reglages)
    mots = dossier / "mots"
    if mots.is_symlink():
        print(f"lien_ignore: {mots} (lien vers un autre dossier, rien n'y est supprimé)")
    elif mots.is_dir():
        for fichier in sorted(mots.iterdir()):
            if fichier.is_file() and fichier.suffix in FICHIERS_MOTS:
                fichier.unlink()
                supprimes.append(fichier)
        if not any(mots.iterdir()):
            mots.rmdir()
    for fichier in supprimes:
        print(f"supprime: {fichier}")
    restes = sorted(p.name for p in dossier.iterdir()) if dossier.is_dir() else []
    print("reste_dans_le_dossier: " + (", ".join(restes) if restes else "rien"))
    return 0


SYNCHRO = ("icloud", "mobile documents", "cloudstorage", "dropbox", "onedrive", "google drive", "googledrive",
           "nextcloud", "owncloud", "pcloud", "kdrive", "proton drive", "syncthing", "seafile")


def verifier(dossier: Path) -> int:
    """Crée le dossier privé (700) et vérifie, liens suivis, qu'il n'est ni synchronisé ni dans un dépôt Git."""
    try:
        (dossier / "mots").mkdir(parents=True, exist_ok=True)
        for d in (dossier, dossier / "mots"):
            if not d.is_symlink():  # ne jamais changer les droits du dossier vers lequel pointe un lien
                d.chmod(0o700)  # sans effet sous Windows, où le dossier personnel est déjà réservé à son compte
    except OSError as erreur:
        print(f"dossier_inaccessible: {erreur}")
        return 1
    reels = [dossier.resolve(), (dossier / "mots").resolve()]  # suit les liens, contrairement à « pwd »
    print(f"chemin_reel: {reels[0]}")
    if reels[1] != reels[0] / "mots":
        print(f"mots_ailleurs: {reels[1]}")
    lien = dossier / "reglages.md"
    if lien.is_symlink():
        print(f"reglages_ailleurs: {lien.resolve()}")
        reels.append(lien.resolve())
    synchro = sorted({s for r in reels for s in SYNCHRO if s in _sans_accents(str(r))})
    print("synchronise: " + (", ".join(synchro) if synchro else "non"))
    depot = next((p for r in reels for p in (r, *r.parents) if (p / ".git").exists()), None)
    print(f"depot_git: {depot or 'non'}")
    return 1 if synchro or depot or reels[1] != reels[0] / "mots" or lien.is_symlink() else 0


# ---------------------------------------------------------------- Apple Santé

TYPE_FLUX = "HKCategoryTypeIdentifierMenstrualFlow"
CLE_DEBUT = "HKMenstrualCycleStart"  # valeur texte observée dans les exports, non documentée par Apple ;
# sans elle, le script regroupe simplement les jours en périodes.


def _lire_flux_apple(flux) -> tuple[set[dt.date], set[dt.date]] | None:
    jours: set[dt.date] = set()
    debuts: set[dt.date] = set()
    racine = None
    for evenement, element in ET.iterparse(flux, events=("start", "end")):
        if evenement == "start":
            if racine is None:
                racine = element
                if element.tag != "HealthData":
                    return None
            continue
        if element.tag != "Record":
            continue
        if element.get("type") == TYPE_FLUX and not element.get("value", "").endswith("None"):
            jour = _date_iso(element.get("startDate", ""))
            if jour:
                jours.add(jour)
                for meta in element.iter("MetadataEntry"):
                    if meta.get("key") == CLE_DEBUT and meta.get("value", "").lower() in ("1", "true", "yes"):
                        debuts.add(jour)
        racine.clear()  # libère la mémoire : l'export complet peut peser des centaines de Mo
    return jours, debuts


def apple(chemin: Path, maximum: int) -> int:
    try:
        resultat = _lire_apple(chemin)
    except ET.ParseError:
        print("format_non_reconnu : export illisible (certaines versions d'iOS produisaient un fichier mal formé) ; "
              "passez par le PDF d'historique des cycles ou par la saisie")
        return 1
    if resultat is None:
        print("format_non_reconnu : ce fichier ne ressemble pas à un export de l'app Santé")
        return 1
    jours, debuts = resultat
    return _afficher_debuts(premiers_jours(jours, debuts), maximum)


def _lire_apple(chemin: Path):
    resultat = None
    if zipfile.is_zipfile(chemin):
        with zipfile.ZipFile(chemin) as archive:
            candidats = [i for i in archive.infolist()
                         if i.filename.lower().endswith(".xml") and "cda" not in i.filename.lower()]
            for info in sorted(candidats, key=lambda i: -i.file_size):
                with archive.open(info) as flux:
                    resultat = _lire_flux_apple(flux)
                if resultat is not None:
                    break
    else:
        with open(chemin, "rb") as flux:
            resultat = _lire_flux_apple(flux)
    return resultat


# ---------------------------------------------------------------- JSON (Clue, Flo, autres)

MOTS_REGLES = ("period", "menstru", "bleed", "flow", "regles")
MOTS_EXCLUS = ("predict", "forecast", "estimat", "expected", "prevision", "ovulat",
               "fertil", "pregnan", "grossesse")
VALEURS_NULLES = {"", "none", "no", "non", "0", "false", "null", "off", "nothing", "aucun"}


def _est_nul(valeur) -> bool:
    if valeur is None or valeur is False:
        return True
    if isinstance(valeur, (int, float)) and valeur == 0:
        return True
    if isinstance(valeur, str) and _sans_accents(valeur.strip()) in VALEURS_NULLES:
        return True
    return isinstance(valeur, (list, dict)) and not valeur


def _parcourir(noeud, chemin: tuple[str, ...], jours: set[dt.date]) -> None:
    chemin_bas = " ".join(_sans_accents(c) for c in chemin)
    if any(m in chemin_bas for m in MOTS_EXCLUS):
        return
    if isinstance(noeud, dict):
        cles = {str(k): v for k, v in noeud.items()}
        cles_bas = {_sans_accents(k): v for k, v in cles.items()}
        dates = [v for k, v in cles_bas.items()
                 if isinstance(v, str) and _date_iso(v) and ("date" in k or "day" in k or "start" in k or k in ("jour", "debut"))]
        exclu = any(m in k for k in cles_bas for m in MOTS_EXCLUS)
        if dates and not exclu:
            marque_ici = any(any(m in k for m in MOTS_REGLES) and not _est_nul(v)
                             for k, v in cles_bas.items() if not isinstance(v, str) or not _date_iso(v))
            valeur_type = any(isinstance(v, str) and any(m in _sans_accents(v) for m in MOTS_REGLES)
                              for k, v in cles_bas.items() if k in ("type", "category", "categorie", "kind", "name"))
            dans_liste_regles = any(m in chemin_bas for m in MOTS_REGLES)
            if marque_ici or valeur_type or dans_liste_regles:
                debut = next((v for k, v in cles_bas.items()
                              if isinstance(v, str) and _date_iso(v) and "start" in k), dates[0])
                jours.add(_date_iso(debut))
        for k, v in cles.items():
            _parcourir(v, chemin + (k,), jours)
    elif isinstance(noeud, list):
        for element in noeud:
            _parcourir(element, chemin, jours)


def json_generique(chemin: Path, maximum: int) -> int:
    contenus = []
    if zipfile.is_zipfile(chemin):
        with zipfile.ZipFile(chemin) as archive:
            for info in archive.infolist():
                if not info.filename.lower().endswith((".json", ".cluedata")):
                    continue
                if info.flag_bits & 0x1:
                    print("archive_protegee : décompressez-la vous-même avec le mot de passe fourni "
                          "par l'application, puis donnez le fichier .json")
                    return 1
                contenus.append(archive.read(info).decode("utf-8-sig", errors="replace"))
    else:
        contenus.append(chemin.read_text(encoding="utf-8-sig", errors="replace"))
    jours: set[dt.date] = set()
    for texte in contenus:
        try:
            donnees = json.loads(texte)
        except json.JSONDecodeError:
            print("format_non_reconnu : ce fichier n'est pas du JSON lisible")
            return 1
        _parcourir(donnees, (), jours)
    return _afficher_debuts(premiers_jours(jours), maximum)


# ---------------------------------------------------------------- liste de jours (raccourci)

def liste(chemin: Path, maximum: int) -> int:
    jours: set[dt.date] = set()
    for ligne in chemin.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        for iso, jj, mm, aaaa in DATE_DANS_TEXTE.findall(ligne):
            try:
                jour = dt.date.fromisoformat(iso) if iso else dt.date(int(aaaa), int(mm), int(jj))
            except ValueError:
                continue
            jours.add(jour)
    return _afficher_debuts(premiers_jours(jours), maximum)


def _chemin(texte: str) -> Path:
    return Path(texte).expanduser()  # « ~ » développé même quand il arrive entre guillemets


def main(argv: list[str] | None = None) -> int:
    os.umask(0o077)  # tout ce que ce programme crée n'est lisible que par son compte
    analyseur = argparse.ArgumentParser(description="Outil local du skill ca-arrive (aucune connexion).")
    sous = analyseur.add_subparsers(dest="commande", required=True)
    p = sous.add_parser("calcul", help="estime la prochaine date à partir du fichier de réglages")
    p.add_argument("fichier", type=_chemin)
    p.add_argument("--aujourdhui", type=dt.date.fromisoformat, default=None)
    p = sous.add_parser("ajouter", help="ajoute des premiers jours confirmés au fichier de réglages")
    p.add_argument("fichier", type=_chemin)
    p.add_argument("dates", nargs="+")
    p.add_argument("--aujourdhui", type=dt.date.fromisoformat, default=None)
    p = sous.add_parser("effacer", help="supprime reglages.md et les mots préparés du dossier")
    p.add_argument("fichier", type=_chemin, metavar="dossier")
    p = sous.add_parser("verifier", help="crée le dossier privé et vérifie qu'il n'est ni synchronisé ni dans Git")
    p.add_argument("fichier", type=_chemin, metavar="dossier")
    for nom in ("apple", "json", "liste"):
        p = sous.add_parser(nom)
        p.add_argument("fichier", type=_chemin)
        p.add_argument("--max", type=int, default=MAX_DATES)
    args = analyseur.parse_args(argv)
    if args.commande in ("calcul", "ajouter") and (args.fichier.is_dir() or not args.fichier.suffix):
        args.fichier = args.fichier / "reglages.md"  # le dossier donné à la place du fichier
    if args.commande in ("effacer", "verifier") and args.fichier.name == "reglages.md":
        args.fichier = args.fichier.parent  # le fichier donné à la place du dossier
    if args.commande == "calcul":
        return calcul(args.fichier, args.aujourdhui or dt.date.today())
    if args.commande == "ajouter":
        return ajouter(args.fichier, args.dates, args.aujourdhui or dt.date.today())
    if args.commande == "effacer":
        return effacer(args.fichier)
    if args.commande == "verifier":
        return verifier(args.fichier)
    if not args.fichier.exists():
        print(f"fichier_introuvable: {args.fichier}")
        return 1
    return {"apple": apple, "json": json_generique, "liste": liste}[args.commande](args.fichier, args.max)


if __name__ == "__main__":
    sys.exit(main())
