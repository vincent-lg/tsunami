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


"""Fichier contenant l'action ajouter_colonne."""

from primaires.format.tableau import GAUCHE, DROITE, CENTRE
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Ajoute une colonne au tableau.
    
    Voir l'aide de la fonction 'creer_tableau' pour un exemple complet.
    
    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ajouter_colonne, "Tableau", "str")
        cls.ajouter_types(cls.ajouter_colonne, "Tableau", "str", "str")

    @staticmethod
    def ajouter_colonne(tableau, nom, flags=""):
        """Ajoute une nouvelle colonne au tableau.

        Paramètres à préciser :

          * tableau : le tableau nouvellement créé
          * nom : le nom de la colonne (une chaïne)
          * flags : les flags d'alignement de la colonne (une chaîne)
        
        Flags disponibles :
        
          * "gauche" : aligne le texte à gauche de la colonne (défaut)
          * "droite" : aligne le texte à droite de la colonne
          * "centre" : centre le texte dans la colonne
        
        Exemples d'utilisation :
        
          tableau = creer_tableau("Outils de charpenterie")
          ajouter_colonne tableau "Nom de l'outil"
          ajouter_colonne tableau "Prix" "droite"

        """
        flags = flags.lower()
        if not flags or flags == "gauche":
            alignement = GAUCHE
        elif flags == "droite":
            alignement = DROITE
        elif flags == "centre":
            alignement = CENTRE
        else:
            raise ErreurExecution("Alignement inconnu : {}".format(flags))
        
        tableau.ajouter_colonne(nom, alignement)
