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


"""Fichier contenant l'action pratiquer_talent."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Fait pratiquer un talent à un personnage.

    Contrairement à l'action 'enseigner_talent', cette action se
    base sur la difficulté d'apprentissage d'un talent pour
    "l'apprendre naturellement". Si l'apprentissage réussit, le
    personnage verra le message "Vous progressez dans
    l'apprentissage du talent...".

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.pratiquer_talent, "Personnage", "str")
        cls.ajouter_types(cls.pratiquer_talent, "Personnage", "str", "Fraction")

    @staticmethod
    def pratiquer_talent(personnage, nom_talent, probabilite=1):
        """Fait pratiquer le talent au personnage spécifié.

        Paramètres à entrer :

          * personnage : le personnage à qui l'on veut enseigner le talent
          * nom_talent : le nom du talent, sous la forme d'une chaîne
          * probabilite (optionnelle) : un nombre influençant l'apprentissage.

        La probabilité est un nombre entre 0 et 1 qui affecte
        l'apprentissage du talent. La probabilité par défaut
        est de 1. Si la probabilité est plus faible, apprendre
        le talent devient plus difficile. Par exemple, une
        probabilité de 1/2 (0.5) rend l'apprentissage deux fois
        plus difficile. Il est parfois utile de faire varier la
        difficulté de l'apprentissage d'un talent (par exemple,
        en fonction de la qualité des actions réussies par le
        personnage).

        Exemple d'utilisation :

          pratiquer_talent personnage "apprivoisement"
          # Le personnage va peut-être apprendre le talent
          pratiquer_talent personnage "apprivoisement" 1/3
          # C'est trois fois moins probable

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

        personnage.pratiquer_talent(cle,  1 / int(probabilite))
