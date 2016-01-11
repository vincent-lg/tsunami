# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 NOEL-BARON Léo
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


"""Fichier contenant le type livre."""

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.information.contextes.page import Page
from primaires.interpreteur.editeur.flag import Flag
from primaires.objet.types.editeurs.chapitres import EdtChapitres
from .base import BaseType

class Livre(BaseType):

    """Type d'objet: livre.

    """

    nom_type = "livre"
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.chapitres = []
        self.afficher_sommaire = True
        self.afficher_numeros = True
        self.etendre_editeur("ch", "chapitres", EdtChapitres, self, "")
        self.etendre_editeur("som", "affiche le sommaire", Flag,
                self, "afficher_sommaire")
        self.etendre_editeur("num", "affiche les numéros des chapitres",
                Flag, self, "afficher_numeros")

    def ajouter_chapitre(self, titre):
        """Ajoute un nouveau chapitre à la fin."""
        chapitre = Chapitre(self, titre)
        self.chapitres.append(chapitre)
        return chapitre

    def supprimer_chapitre(self, no):
        """Supprime le chapitre."""
        del self.chapitres[no]

    def monter_chapitre(self, no):
        """Remonte le chapitre indiqué."""
        chapitres = self.chapitres[:no]
        chapitres.insert(-1, self.chapitres[no])
        chapitres += self.chapitres[no + 1:]
        self.chapitres[:] = chapitres

    def descendre_chapitre(self, no):
        """Cette méthode descend un chapitre dans la liste."""
        chapitre = self.chapitres[no]
        chapitres = list(self.chapitres)
        del chapitres[no]
        chapitres.insert(no + 1, chapitre)
        self.chapitres[:] = chapitres

    def get_texte_pour(self, personnage):
        """Retourne le texte des chapitres sous la forme d'une chaîne."""
        # D'abord si il y a un sommaire
        msg = ""
        if self.afficher_sommaire:
            msg = "Sommaire :"
            for i, chapitre in enumerate(self.chapitres):
                msg += "\n  "
                if self.afficher_numeros:
                    msg += str(i + 1).rjust(2) + " - "
                msg += chapitre.titre
            msg += "\n|sp|\n"

        # Affiche à présent le contenu de chaque chapitre
        for i, chapitre in enumerate(self.chapitres):
            if self.afficher_numeros:
                msg += str(i + 1) + ". "
            msg += chapitre.titre
            msg += "\n\n" + chapitre.description.regarder(personnage, self)
            msg += "\n|sp|\n"

        return msg[:-5].rstrip("\n")

    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        msg = BaseType.regarder(self, personnage)
        if self.chapitres:
            texte = msg + "\n\n" + self.get_texte_pour(personnage)
            contexte = Page(personnage.instance_connexion, texte)
            personnage.contexte_actuel.migrer_contexte(contexte)
            return ""

        return msg


class Chapitre(BaseObj):

    """Classe représentant un unique chapitre.

    Un chapitre possède un titre et une description. Sa position dans le
    livre est déterminée par sa position dans la liste des autres chapitres.

    """

    def __init__(self, prototype, titre):
        BaseObj.__init__(self)
        self.prototype = prototype
        self.titre = titre
        self.description = Description(parent=self)

    def __getnewargs__(self):
        return (None, "inconnu")

    def __repr__(self):
        return "<Chapitre {} de {}>".format(self.titre, self.prototype)

    def __str__(self):
        return self.titre
