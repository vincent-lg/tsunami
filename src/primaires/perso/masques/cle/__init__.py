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
# LIABLE FOR ANY DIRECT, INDIRECT, INCcleAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le masque <cle>."""

import re

from corps.fonctions import valider_cle
from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class Cle(Masque):

    """Masque <cle>.

    On attend une clé en paramètre (voir valider_cle).

    """

    nom = "cle"
    nom_complet = "clé identifiante"

    def __init__(self):
        """Constructeur du masque"""
        Masque.__init__(self)
        self.proprietes["regex"] = "None"

    def init(self):
        """Initialisation des attributs"""
        self.cle = ""

    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        cle = liste_vers_chaine(commande).lstrip()

        if not cle:
            raise ErreurValidation( \
                "Précisez une clé identifiante.")

        cle = cle.lower()
        cle = cle.split(" ")[0]
        commande[:] = commande[len(cle):]
        self.a_interpreter = cle
        masques.append(self)
        return True

    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        cle = self.a_interpreter
        if self.regex:
            res = re.search(self.regex, cle)
            if res is None:
                raise ErreurValidation(
                    "|err|Cette clé identifiante est invalide.|ff|")
        else:
            try:
                valider_cle(cle)
            except ValueError:
                raise ErreurValidation(
                    "|err|Cette clé identifiante est invalide.|ff|")

        self.cle = cle

        return True
