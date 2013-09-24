# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant la classe Description, détaillée plus bas."""

import re
from textwrap import wrap

from abstraits.obase import BaseObj
from .fonctions import *

# Constantes
TAILLE_LIGNE = 75
RE_FLOTTANTE = re.compile(r"@([a-z0-9_:]{3,})")

class Description(BaseObj):

    """Cette classe définit une description générique.

    Ce peut être une description de salle, d'objet, de balise, de
    véhicule...

    Elle propose plusieurs méthodes facilitant son déploiement dans un
    éditeur et sa mise en forme.

    Paramètres à préciser à la création :
            description -- la description de base (aucune par défaut)
            parent -- l'objet décrit
            scriptable -- permet de scripter la description
            callback -- permet d'appeler un callback en cas de mise à jour

        Ce dernier paramètre doit être une chaîne de caractères
        représentant le nom de méthode du parent qui sera appelée
        à chaque fois que la description sera modifiée.
        Cela permet d'effectuer d'autres actions si la description
        est modifiée. Voir la méthode maj_auto.

    """

    nom_scripting = "description"
    def __init__(self, description=None, parent=None, scriptable=True,
            callback=None):
        """Constructeur"""
        BaseObj.__init__(self)
        self.paragraphes = [] # une liste des différents paragraphes
        self.saut_de_ligne = False
        self.parent = parent
        self.script = ScriptDescription(self)
        self.scriptable = scriptable
        self.callback = callback
        if description:
            self.ajouter_paragraphe(description)

    def __getnewargs__(self):
        return ("", )

    def __str__(self):
        """Retourne la description sous la forme d'un texte 'str'"""
        res = []
        for paragraphe in self.paragraphes:
            paragraphe = self.wrap_paragraphe(paragraphe)
            paragraphe = paragraphe.replace("|nl|", "\n")
            res.append(paragraphe)
        return "\n".join(res)

    def __bool__(self):
        """Retourne True si la description n'est pas vide, False sinon."""
        return bool(str(self))

    def maj_auto(self):
        """Appelle le callback (si défini) pour mettre à jour le parent."""
        if self.parent and self.callback:
            getattr(self.parent, self.callback)()

    def ajouter_paragraphe(self, paragraphe):
        """Ajoute un paragraphe.

        """
        self.paragraphes.append(paragraphe)
        self.maj_auto()

    def supprimer_paragraphe(self, no):
        """Supprime le paragraphe #no"""
        del self.paragraphes[no]
        self.maj_auto()

    def vider(self):
        """Supprime toute la description"""
        self.paragraphes[:] = []
        self.maj_auto()

    def remplacer(self, origine, par):
        """Remplace toutes les occurences de 'origine' par 'par'.

        Cette recherche & remplacement se fait dans tous les paragraphes.
        Le remplacement ne tient compte ni des majuscules, ni des accents.

        """
        origine = supprimer_accents(origine).lower()
        diff = len(origine) - len(par)
        for i, paragraphe in enumerate(self.paragraphes):
            paragraphe = supprimer_accents(paragraphe).lower()
            # On cherche 'origine'
            no_car = paragraphe.find(origine)
            while no_car >= 0:
                self.paragraphes[i] = self.paragraphes[i][:no_car] + \
                        par + self.paragraphes[i][no_car + len(origine):]
                paragraphe = supprimer_accents(self.paragraphes[i]).lower()
                no_car = paragraphe.find(origine, no_car + len(par))

        self.maj_auto()

    def wrap_paragraphe(self, paragraphe, lien="\n", aff_sp_cars=False):
        """Wrap un paragraphe et le retourne"""
        if aff_sp_cars:
            paragraphe = echapper_sp_cars(paragraphe)
        else:
            paragraphe = paragraphe.replace("|tab|", "   ")
        return lien.join(wrap(paragraphe, TAILLE_LIGNE))

    @property
    def paragraphes_indentes(self):
        """Retourne les paragraphes avec une indentation du niveau spécifié"""
        indentation = "\n   "
        res = []
        for paragraphe in self.paragraphes:
            paragraphe = self.wrap_paragraphe(paragraphe, lien=indentation)
            paragraphe = paragraphe.replace("|nl|", "\n")
            res.append(paragraphe)

        if not res:
            res.append("Aucune description.")

        return indentation + indentation.join(res)

    def regarder(self, personnage, elt=None):
        """Le personnage regarde la description."""
        description = ""
        desc_flottantes = []
        elt = elt or self.parent
        for paragraphe in self.paragraphes:
            paragraphe = paragraphe.replace("|nl|", "\n").replace(
                    "|tab|", "   ")
            if self.scriptable:
                # On charge récursivement les descriptions flottantes
                paragraphe, flottantes = self.charger_descriptions_flottantes(
                        paragraphe)
                desc_flottantes += [fl.description for fl in flottantes if \
                        fl.description not in desc_flottantes]

            description += paragraphe + "\n"

        description = description.rstrip("\n ")
        if self.scriptable:
            evts = re.findall(r"(\$[a-z0-9]+)([\n ,.]|$)", description)
        else:
            evts = []

        evts = [e[0] for e in evts]
        desc_flottantes.insert(0, self)
        for nom_complet in evts:
            nom = nom_complet[1:]
            trouve = False
            for desc in desc_flottantes:
                evt = desc.script["regarde"]
                if nom in evt.evenements:
                    evt = evt.evenements[nom]
                    evt.executer(True, regarde=elt, personnage=personnage)
                    retour = evt.espaces.variables["retour"]
                    description = description.replace(nom_complet, retour)
                    trouve = True
                    break

            if not trouve:
                raise ValueError("impossible de trouver la description " \
                    "dynamique '{}'".format(nom))

        paragraphes = []
        for paragraphe in description.split("\n"):
            paragraphes.append("\n".join(wrap(paragraphe, TAILLE_LIGNE)))


        return "\n".join(paragraphes)

    def charger_descriptions_flottantes(self, paragraphe):
        """Charge récursivement les descriptions flottantes."""
        flottantes = []
        for flottante in RE_FLOTTANTE.findall(paragraphe):
            try:
                desc_flottante = importeur.format.descriptions_flottantes[
                        flottante]
            except KeyError:
                raise ValueError("la description flottante '{}' est " \
                        "introuvable".format(flottante))

            flottantes.append(desc_flottante)
            description = "\n".join([paragraphe.replace("|nl|", "\n").replace(
                    "|tab|", "   ") for paragraphe in \
                    desc_flottante.description.paragraphes])
            paragraphe = paragraphe.replace("@" + flottante, description)

        if RE_FLOTTANTE.search(paragraphe):
            paragraphe, autres = self.charger_descriptions_flottantes(
                    paragraphe)
            return paragraphe, flottantes + autres

        return paragraphe, flottantes

# On importe ici pour éviter les boucles
from primaires.scripting.script import Script

class ScriptDescription(Script):

    def init(self):
        """Initialisation du script."""
        evt = self.creer_evenement("regarde")
        var_regarde = evt.ajouter_variable("regarde", "BaseObj")
        var_personnage = evt.ajouter_variable("personnage", "Personnage")
        var_regarde.aide = "l'élément regardé"
        var_personnage.aide = "le personnage regardant"
