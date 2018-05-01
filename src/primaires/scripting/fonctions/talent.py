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


"""Fichier contenant la fonction talent."""

from fractions import Fraction

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne le niveau d'un talent connu par un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.talent, "Personnage", "str")

    @staticmethod
    def talent(personnage, nom_talent):
        """Retourne le pourcentage du talent connu par le personnage.

        Si le personnage ne connaît pas le talent, retourne 0.

        Paramètres à entrer :

          * personnage : le personnage à tester
          * nom_talent : le nom du talent (chaîne)

        Exemple d'utilisation :

          niveau = talent(personnage, "maniement de l'épée")

        """
        nom_talent = supprimer_accents(nom_talent).lower()
        cle = None
        talent = None
        for t_talent in importeur.perso.talents.values():
            if supprimer_accents(t_talent.nom) == nom_talent:
                talent = t_talent
                cle = talent.cle
                break

        if talent is None:
            raise ErreurExecution("talent inconnu : {}".format(repr(
                    nom_talent)))

        return Fraction(personnage.get_talent(cle))
