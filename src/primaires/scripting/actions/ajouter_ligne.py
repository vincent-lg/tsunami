# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant l'action ajouter_ligne."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Ajoute une ligne à un tableau.
    
    Voir l'aide de la fonction 'creer_tableau' pour un exemple complet.
    
    """

    verifier = False
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ajouter_ligne)

    @staticmethod
    def ajouter_ligne(tableau, *parametres):
        """Ajoute une ligne au tableau.

        Cette action permet d'ajouter une ligne au tableau, le
        premier paramètre de cette fonction. Le nombre de paramètres
        dépend du nombre de colonnes définies dans le tableau. Un
        tableau avec deux colonnes, par exemple, aura deux
        paramètres après 'tableau'. Consultez les exemples donnés
        plus bas, ainsi que ceux donnés dans l'aide de la fonction
        'creer_tableau'.
        
        Paramètres obligatoires :

          * tableau : le tableau à étendre
        
        Exemples d'utilisation :

          # Création d'un tableau simple avec deux colonnes
          tableau = creer_tableau()
          ajouter_colonne tableau "Joueur"
          ajouter_colonne tableau "Points"
          # Ajout des lignes
          ajouter_ligne tableau "Kredh" 10
          ajouter_ligne tableau "Anael" 19
          ajouter_ligne tableau "Arkane" 19
          # Création d'un tableau avec trois colonnes
          tableau = creer_tableau()
          ajouter_colonne tableau "Produit"
          ajouter_colonne tableau "Prix unitaire"
          ajouter_colonne tableau "Quantité"
          # Ajout des lignes
          ajouter_ligne tableau "un perroquet multicolore" 30 1
          ajouter_ligne tableau "un paquet de chips" 2 25
          ajouter_ligne tableau "un fer à cheval" 9 15
        
        """
        tableau.ajouter_ligne(*parametres)
