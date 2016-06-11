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


"""Fichier contenant la fonction creer_structure."""

from corps.fonctions import valider_cle
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution
from primaires.scripting.structure import StructureSimple

class ClasseFonction(Fonction):

    """Crée une structure du type indiqué.

    Une structure représente une information conservée en mémoire.
    La plus grande différence d'avec les mémoires est qu'elle peut
    contenir d'autres informations. C'est un ensemble potentiellement
    complexe (une structure peut contenir des chaînes, des nombres,
    des listes voire d'autres structures). Au lieu d'être conservée
    dans des salles ou personnages, les structures sont globales
    (on peut les récupérer de n'importe quel script). Elles sont
    groupées par type. Le type est précisé en paramètre au moment
    de créer une structure. Les exemples ci-dessous expliqueront
    un peu mieux ce dont il s'agit, ainsi que des manipulations
    possibles. Pour plus d'information, consultez
    http://redmine.kassie.fr/projects/documentation/wiki/Structure .

      # On crée une structure devant représenter un journal
      structure = creer_structure("journal")
      # Pour reconnaître la nouvelle structure, celle-ci possède un
      # ID, un nombre identifiant commençant à 1. Ainsi :
      id = recuperer(structure, "id")
      # 'id' contient 1
      ecrire structure "titre" "Les nouvelles sont toujorus bonnes"
      ecrire structure "date" "le troisième jour du mois des fêtes, an 39."
      ecrire structure "auteur" joueur("Kredh")
      ecrire structure "contributeurs" liste()
      ecrire structure "valeur" 15
      # Vous devez donc utiliser l'action 'ecrire' pour écrire des
      # informations dans la structure. Le premier paramètre est la
      # structure à écrire, le second est la clé de la case et le
      # troisième est la valeur de cette case. La valeur peut être
      # de tout type (chaîne, nombre, liste, autre structure, personnage,
      # salle, etc...). La clé permet de retrouver l'information.
      # Si cela vous aide, vous pouvez imaginer que les structures
      # contiennent des listes, mais au lieu de numéroter chaque
      # case, on place des noms (clés) dessus pour retrouver
      # l'information. On utilise l'action 'ecrire' pour modifier
      # la valeur d'une case et la fonction 'recuperer' pour lire
      # la valeur d'une case.
      auteur = recuperer(structure, "auteur")
      # 'auteur' contient le joueur Kredh
      # Vous pouvez récupérer le type de la structure sous la clé
      # 'structure' et son ID sous la clé 'id'. Ces informations sont
      # disponibles en lecteur seule et vous ne pouvez les modifier :
      ecrire structure "id" 5
      # **Cré une alerte**
      # Pour récupérer une structure dont vous connaissez le type
      # et l'ID, utilisez la fonction 'structure' :
      journal = structure("journal", 1)
      # Pour récupérer toutes les structures de même groupe, par exemple
      # toutes les structures de type 'journal' ici, utilisez 'structures' :
      journaux = structures("journal")
      # Retourne une liste, que vous pouvez parcourir bien sûr :
      pour chaque journal dans journaux:
          titre = recuperer(journal, "titre")
          auteur = recuperer(journal, "auteur")
          # ...
      fait
      # Vous pouvez enfin supprimer une structure grâce à l'action
      # 'supprimer_structure' :
      supprimer_structure journal
      # Ou bien :
      supprimer_structure "journal" 1

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.creer_structure_simple)
        cls.ajouter_types(cls.creer_structure, "str")

    @staticmethod
    def creer_structure_simple():
        """Crée une structure simple non enregistrée.

        La structure créée à l'aide de cette fonction sans paramètre
        n'est pas automatiquement enregistrée (il faut l'enregistrer
        dans une autre structure ou dans une mémoire pour ce faire).
        Une structure simple, sans groupe, peut être utile pour
        conserver des informations de façon plus logique que dans
        des listes. Le résultat est le même : vous pouvez lire et
        écrire dans des cases de cette structure sans contrainte.

        Exemple d'utilisation :

          simple = structure()
          ecrire simple "nom" "..."
          nom = recuperer(simple, "nom")

        """
        return StructureSimple()

    @staticmethod
    def creer_structure(groupe):
        """Crée une structure du groupe indiqué.

        Paramètres à entrer :

          * groupe : le nom du groupe de la structure

        Toutes les structures sont identiques au début : elles sont
        toutes créées absolument vides. Vous pouvez mettre les cases
        que vous souhaitez dedans, ou bien les transmettre à un
        éditeur pour les remplir manuellement. Le groupe détermine
        comment les structures seront groupées. Le groupe et l'ID
        forme une combinaison unique représentant chaque structure.

        Exemple d'utilisation :

          # Crée une structure dans le groupe 'journal'
          journal1 = creer-structure("journal")
          id1 = recuperer(journal1, "id")
          # 'id1' vaut 1
          journal2 = creer-structure("journal")
          id2 = recuperer(journal2, "id")
          # 'id2' vaut 2
          # Crée une structure vide de groupe 'poeme'
          poeme = creer-structure("poeme")
          id3 = recuperer(poeme, "id")
          # 'id3' vaut 1

        """
        valider_cle(groupe)
        return importeur.scripting.creer_structure(groupe)
