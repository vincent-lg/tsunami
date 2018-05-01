# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 DAVY Guillaume
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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur 'SelectionTags'."""

from primaires.interpreteur.editeur.selection import Selection
from primaires.format.fonctions import supprimer_accents

class SelectionTags(Selection):

    """Contexte-éditeur pour la sélection de tags."""

    nom = "editeur:tags:selection"

    def __init__(self, pere, objet=None, attribut=None, liste=None,
            tagge=None):
        Selection.__init__(self, pere, objet, attribut, liste)
        self.tagge = tagge

    @staticmethod
    def afficher_apercu(apercu, objet, valeur, liste=None, tagge=None):
        """Affichage de l'aperçu."""
        return Selection.afficher_apercu(apercu, objet, valeur, liste)

    def interpreter(self, msg):
        """Interprétation du contexte"""
        nom = msg
        msg_sa = supprimer_accents(msg).lower()
        liste = getattr(self.objet, self.attribut)
        cles = list(self.liste)
        cles_sa = [supprimer_accents(c).lower() for c in cles]
        if msg_sa in cles_sa:
            cle = cles[cles_sa.index(msg_sa)]
            if cle in liste:
                while cle in liste:
                    liste.remove(cle)
            else:
                liste.append(cle)

                # Ajout des évènements à l'objet taggé
                tag = importeur.tags.tags[cle]
                script = tag.script
                for evenement in script.evenements.values():
                    evt = self.tagge.script[evenement.nom]
                    evt.copier_depuis(evenement)
                    self.pere << "Copie de l'évènement {}.".format(
                            evenement.nom)

            liste[:] = [e for e in liste if e]
            self.actualiser()
        else:
            self.pere << "|err|La clé {} est introuvable.|ff|".format(
                    repr(msg))
