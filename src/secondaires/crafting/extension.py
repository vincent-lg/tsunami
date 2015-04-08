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

from abstraits.obase import BaseObj
from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.editeur.uniligne import Uniligne

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

    def __init__(self, guilde, editeur, nom):
        """Constructeur du talent."""
        BaseObj.__init__(self)
        self.guilde = guilde
        self.editeur = editeur
        self.nom = nom
        self.titre = nom
        self.type = "chaîne"
        self.aide = "non précisée"
        self._construire()

    def __getnewargs__(self):
        return (None, "", "")

    def __repr__(self):
        return "<Extension d'éditeur {} ({})>".format(self.editeur, self.nom)

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
                    titre = supprimer_accents(extension.titre).lower()
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
                                "le raccourci pour {}".format(extension))
                    enveloppe = presentation.ajouter_choix(
                            extension.titre, raccourci, Uniligne,
                            importeur.crafting.configuration[objet],
                            extension.nom)
                    enveloppe.parent = presentation
                    enveloppe.aide_courte = extension.aide
