# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant le masque <objet_cale>."""

from primaires.format.fonctions import contient
from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class ObjetCale(Masque):

    """Masque <objet_cale>.

    On attend un nom d'objet en paramètre.

    """

    nom = "objet_cale"
    nom_complet = "objet en cale"

    def init(self):
        """Initialisation des attributs"""
        self.prototype = None

    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        message = liste_vers_chaine(commande).lstrip()
        self.a_interpreter = message
        commande[:] = []
        if not message:
            raise ErreurValidation(
                "Précisez un nom d'objet.")

        if getattr(personnage.salle, "navire", None) is None:
            raise ErreurValidation("Vous n'êtes pas sur un navire.")

        masques.append(self)
        return True

    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom = self.a_interpreter
        salle = personnage.salle
        cale = salle.navire.cale
        for conteneur in cale.conteneurs.values():
            for cle in conteneur.keys():
                try:
                    prototype = importeur.objet.prototypes[cle]
                except KeyError:
                    continue

                if contient(prototype.nom_singulier, nom) or contient(
                        prototype.nom_pluriel, nom):
                    self.prototype = prototype
                    return True

        raise ErreurValidation("Cet objet n'est pas trouvable dans la " \
                "cale de ce navire.")
        return True
