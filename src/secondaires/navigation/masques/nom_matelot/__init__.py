# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant le masque <nom_matelot>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class NomMatelot(Masque):

    """Masque <nom_matelot>.

    On attend un nom unique de matelot. Deux matelots ne
    peuvent avoir le même nom dans l'équipage.

    """

    nom = "nom_matelot"
    nom_complet = "nom d'un matelot"

    def __init__(self):
        """Constructeur du masque"""
        Masque.__init__(self)
        self.proprietes["nouveau"] = "False"

    def init(self):
        """Initialisation des attributs"""
        self.nom_matelot = ""
        self.matelot = None

    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        nom = liste_vers_chaine(commande)

        if not nom:
            raise ErreurValidation(
                "Précisez un nom de matelot.")

        nom = nom.split(" ")[0].lower()
        self.a_interpreter = nom
        commande[:] = commande[len(nom):]
        masques.append(self)
        return True

    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom = self.a_interpreter

        salle = personnage.salle
        if not hasattr(salle, "navire"):
            raise ErreurValidation(
                "|err|Vous n'êtes pas sur un navire.|ff|")

        navire = salle.navire
        equipage = navire.equipage

        matelot = None
        try:
            matelot = equipage.get_matelot(nom)
        except KeyError:
            pass

        if not self.nouveau and matelot is None:
            raise ErreurValidation(
                "|err|Le matelot {} ne peut être trouvé.|ff|".format(nom))
        elif self.nouveau and matelot:
            raise ErreurValidation(
                "|err|Le matelot {} existe déjà.|ff|".format(nom))

        self.nom_matelot = nom
        self.matelot = matelot
        return True
