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


"""Fichier contenant l'action changer_poids."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Change le poids unitaire de l'objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.changer_poids, "Objet", "Fraction")
        cls.ajouter_types(cls.changer_poids, "PrototypeObjet", "Fraction")

    @staticmethod
    def changer_poids(prototype_ou_objet, poids):
        """Change le poids unitaire de l'objet ou du prototype précisé.

        Le poids (tel que renvoyé par la fonction 'poids') et le
        poids unitaire (tel que modifié par l'action 'changer_poids')
        peuvent varier pour certains types. Par exemple, les
        conteneurs ont un poids formé de leur poids unitaire et de
        la somme des poids des objets qu'ils contiennent. L'action
        'changer_poids' ne s'applique qu'au poids unitaire.

        Paramètres à préciser :

          * prototype_ou_objet : l'objet dont on veut changer le poids
          * poids : le nouveau poids (en kilo).

        Exemple d'utilisation :

          changer_poids(objet, 10)

        """
        prototype_ou_objet.poids_unitaire = float(poids)
