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


"""Fichier contenant l'action enseigner_talent."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Enseigne un talent à un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.enseigner_talent, "Personnage", "str", "Fraction")

    @staticmethod
    def enseigner_talent(personnage, nom_talent, nombre):
        """Enseigne le talent au personnage spécifié.

        Paramètres :

          * personnage : le personnage à qui l'on veut enseigner le talent
          * nom_talent : le nom du talent, sous la forme d'une chaîne
          * nombre : le nombre de pourcents à apprendre.

        Exemple d'utilisation :

          enseigner_talent personnage "apprivoisement" 5
          # Donne 5% supplémentaire de plus pour le personnage

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

        nombre = int(nombre)
        if nombre < 1:
            raise ErreurExecution("le nombre {} est inférieur à 1".format(
                    nombre))
        elif nombre > 100:
            raise ErreurExecution("le nombre {} est supérieur à 100".format(
                    nombre))

        origine = actuel = personnage.talents.get(cle, 0)
        actuel += nombre
        if actuel > 100:
            actuel = 100

        personnage.talents[cle] = actuel
        if origine != actuel:
            personnage.envoyer_tip("Vous avez à présent {}|pc| en {} !".format(
                    actuel, talent.nom))
