# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant la classe Extenson, détaillée plus bas."""

import re

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.editeur.choix_objet import ChoixObjet
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.tableau import Tableau
from primaires.interpreteur.editeur.uniligne import Uniligne, CLE

# Constantes
TYPES = {
    "entier": re.compile(r"""
            ^nombre|entier
            # signe
            (\ (?P<signe>positif|negatif|positif\ ou\ nul|negatif\ ou\ nul))?
            # Bornes
            (\ entre\ (?P<min>[0-9]+)\ et\ (?P<max>[0-9]+))?$""", re.X),
    "chaîne": re.compile("^chaine$"),
    "clé": re.compile("^cle$"),
    "prototype d'objet": re.compile("^prototype d'objet$"),
    "tableau": re.compile(r"""
            tableau\ avec\ les\ colonnes
            # Colonne 1 (obligatoire)
            \ (?P<ncol1>.*?)\ \((?P<tcol1>.*?)\)(,|\ et)
            # Colonne 2 (obligatoire)
            \ (?P<ncol2>.*?)\ \((?P<tcol2>.*?)\)
            # Colonne 3 (optionnelle)
            ((,|\ et)\ (?P<ncol3>.*?)\ \((?P<tcol3>.*?)\))?
            # Colonne 4 (optionnelle)
            ((,|\ et)\ (?P<ncol4>.*?)\ \((?P<tcol4>.*?)\))?
            # Colonne 5 (optionnelle)
            ((,|\ et)\ (?P<ncol5>.*?)\ \((?P<tcol5>.*?)\))?
            $""", re.X),
}

class Extension(BaseObj):

    """Classe représentant une extension d'éditeur standard.

    Qunad le crafting veut étendre des éditeurs existants (par
    exemple l'éditeur de salle 'redit'), une nouvelle extension
    est créée reprenant les informations nécessaires à l'extension.

    Une extension à :
        Un éditeur (salle, PNJ, objet...)
        Un nom de configuration
        Un titre
        Un message d'aide

    La modification de l'information indiquée va créer une
    configuration propre au crafting. Par exemple, si on veut
    ajouter à l'éditeur de salle un choix afin de sélectionner
    les objets à extraire, pour la guilde des mineurs, la
    modification de cet objet entraînera la création d'un objet de
    configuration (présent dans importeur.crafting.configuration).

    """

    def __init__(self, parent, editeur, nom):
        """Constructeur du talent."""
        BaseObj.__init__(self)
        self.parent = parent
        self.editeur = editeur
        self.nom = nom
        self.titre = nom
        self.description = Description(parent=self, scriptable=False)
        self._type = "chaîne"
        self.sup = {}
        self.type_complet = "inconnu"
        self._construire()

    def __getnewargs__(self):
        return (None, "", "")

    def __repr__(self):
        return "<Extension d'éditeur {} ({})>".format(self.editeur, self.nom)

    def __str__(self):
        return "extension {}".format(self.nom)

    def _get_type(self):
        return self._type
    def _set_type(self, o_chaine):
        """Change le type."""
        chaine = supprimer_accents(o_chaine).lower()
        for n_type, expression in TYPES.items():
            match = expression.match(chaine)
            if match:
                self._type = n_type
                self.sup = match.groupdict()
                self.type_complet = o_chaine
                return

        raise ValueError("le type {} est invalide".format(repr(chaine)))
    type = property(_get_type, _set_type)

    @property
    def nom_complet(self):
        return "{} ({})".format(self.nom, self.type_complet)

    @property
    def type_editeur(self):
        """Retourne le type d'éditeur sélectionné."""
        nom_type = self._type
        sup = self.sup

        if nom_type == "chaîne":
            return Uniligne, ()
        elif nom_type == "clé":
            return Uniligne, (CLE, )
        elif nom_type == "prototype d'objet":
            return ChoixObjet, (importeur.objet.prototypes, )
        elif nom_type == "entier":
            borne_min = borne_max = None
            signe = sup["signe"]
            if signe == "positif":
                borne_min = 1
            elif signe == "negatif":
                borne_sup = -1
            elif signe == "positif ou nul":
                borne_min = 0
            elif signe == "negatif ou nul":
                borne_sup = 0

            if sup["min"] is not None:
                borne_min = int(sup["min"])
                borne_max = int(sup["max"])

            return Entier, (borne_min, borne_max)
        elif nom_type == "tableau":
            colonnes = []
            for i in range(4):
                ncol = sup["ncol{}".format(i + 1)]
                tcol = sup["tcol{}".format(i + 1)]
                if not ncol or not tcol:
                    break

                if tcol == "chaine":
                    tcol = "chaîne"
                elif tcol == "cl":
                    tcol = "clé"
                elif tcol == "prototype d'objet":
                    tcol = importeur.objet.prototypes.copy()
                elif tcol == "prototype de pnj":
                    tcol = importeur.pnj.prototypes.copy()
                elif tcol == "entier":
                    pass
                else:
                    raise ValueError("Colonne {} ({}) : type {} " \
                            "inconnu".format(i + 1, ncol, repr(tcol)))

                colonnes.append((ncol, tcol))

            return Tableau, (colonnes, )
        else:
            raise ValueError("type {} inconnu".format(repr(nom_type)))

    def creer(self, presentation, objet):
        """Création de l'extension grâce à l'éditeur."""
        titre = supprimer_accents(self.titre).lower()

        # On cherche le raccourci
        raccourci = None
        nb = 1
        while nb < len(titre):
            i = 0
            while i + nb <= len(titre):
                morceau = titre[i:i + nb]
                if morceau not in presentation.raccourcis:
                    raccourci = morceau
                    break

                i += 1

            if raccourci:
                break

            nb += 1

        if raccourci is None:
            raise ValueError("Impossible de trouver " \
                    "le raccourci pour {}".format(self))

        TypeEditeur, sup = self.type_editeur
        enveloppe = presentation.ajouter_choix(
                self.titre, raccourci, TypeEditeur,
                importeur.crafting.configuration[objet],
                self.nom, *sup)
        enveloppe.parent = presentation
        enveloppe.apercu = "{valeur}"
        enveloppe.aide_courte = str(self.description).replace("{",
        "{{").replace("}", "}}").replace("$valeur", "{valeur}")

    @staticmethod
    def etendre_editeur(editeur, presentation, objet):
        """Étend l'éditeur passé en paramètre.

        Cette méthode de classe est connectée à l'hook d'extension
        de l'éditeur. Elle doit se charger de trouver les extensiions
        à appliquer et créer les envelopes correspondantes. La
        présentation doit être un objet de type
        'primaires.interpreteur.editeur.presentation.Presentation'.

        """
        for guilde in sorted(importeur.crafting.guildes.values(),
                key=lambda guilde: guilde.cle):
            for extension in guilde.extensions:
                if extension.editeur == editeur:
                    extension.creer(presentation, objet)

            # Extensions de type
            if editeur == "objet":
                for n_type in guilde.types:
                    if objet.est_de_type(n_type.nom):
                        for extension in n_type.extensions:
                            extension.creer(presentation, objet)
