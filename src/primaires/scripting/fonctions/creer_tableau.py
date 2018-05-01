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


"""Fichier contenant la fonction creer_tableau."""

from primaires.format.tableau import Tableau
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Crée un tableau vide.
    
    Les tableaux sont très utiles pour le formattage de données
    ordonnées. Voici un exemple scripting de ce que vous pouvez faire :
    
      # Création d'un tableau avec deux colonnes, nom et quantité
      # La seconde colonne est alignée sur la droite
      tableau = creer_tableau()
      # Vous pouvez passer en paramètre le titre du tableau
      # Création des colonnes
      ajouter_colonne tableau "Nom"
      ajouter_colonne tableau "Quantité" "droite"
      # Ajout des lignes du tableau
      ajouter_ligne tableau "un chien empaillé" 5
      ajouter_ligne tableau "un moule à gâteau" 12
      ajouter_ligne tableau "une soucoupe volante" 8
      # Affichage du tableau
      dire personnage "${tableau}"
    
    Résultat :
    
      +----------------------+----------+
      | Nom                  | Quantité |
      +----------------------+----------+
      | un chien empaillé    |        5 |
      | un moule à gâteau    |       12 |
      | une soucoupe volante |        8 |
      +----------------------+----------+

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.creer_tableau)
        cls.ajouter_types(cls.creer_tableau, "str")

    @staticmethod
    def creer_tableau(titre=""):
        """Crée un tableau vide.

        Paramètres à entrer :
        
          * titre (optionnel) : le titre du tableau
        
        Exemple d'utilisation :
        
          # Cré un tableau vide sans titre
          tableau = creer-tableau()
          # Cré un tableau vide avec titre
          tableau = creer-tableau("Inventaire du magasin")
          # Utilisez les actions 'ajouter_colonne' et 'ajouter_ligne'
          # pour étendre ce tableau. Consultez l'aide de la fonction.
        
        """
        return Tableau(titre)
