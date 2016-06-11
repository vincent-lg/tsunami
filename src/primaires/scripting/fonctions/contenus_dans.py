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


"""Fichier contenant la fonction contenus_dans."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Renvoie les objets contenus dans un conteneur."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.contenus_dans, "Objet")

    @staticmethod
    def contenus_dans(conteneur):
        """Renvoie la liste des objets contenus dans ce conteneur.

        On doit donc utiliser une boucle pour pardcourir les objets
        retournés par cette fonction. Le conteneur peut être un conteneur
        simple, une machine, un sac de matériau, un conteneur de nourriture
        ou
        de potion. Le sac de matériau et conteneur de potion sont deux
        importantes exceptions à garder à l'esprit :

          * Le sac de matériau retourne une liste de prototypes d'objet,
            pas d'objets. Cette liste est de longueur N (N correspondant
            à la quantité d'objets dans ce sac).
          * Le conteneur de potion retourne une liste d'objets identiques,
            de longueur correspondant au nombre d'onces restantes
            dans ce conteneur de potion. Ne pas traiter cette liste
            comme des objets individuels, car ils sont tous identiques.
            Mieux vaut récupérer la clé du prototype du premier objet,
            ainsi que la longueur de la liste.

        NOTE IMPORTANTE : si le conteneur est un conteneur standard
        ou une machine, ne retourne que les objets uniques. C'est-à-dire,
        principalement, que l'argent ne sera pas retourné.

        Vous pouvez utiliser la fonction 'grouper_par_nom' pour
        avoir un groupage par nom d'objets, ce qui a tendance à
        être plus agréable, notamment pour l'affichage.

        Exemple d'utilisation :

          # 'conteneur' contient un conteneur standard
          pour chaque objet dans conteneur:
             # ...
          fait
          # 'flacon' contient un conteneur de potion
          liquides = contenus_dans(flacon)
          si liquides:
              cle = cle_prototype(recuperer(liquides, 1))
              quantite = longueur(liquides)
              # Verse le liquide au sol...
              poser salle cle quantite
          finsi
          # 'sac' contient un sac de matériau contenant 2 livres de farine
          materiaux = contenus_dans(sac)
          si materiaux:
              cle = cle_prototype(recuperer(materiaux, 1))
              quantite = longueur(materiaux)
              dire personnage "Ce sac contient $quantite livres de $cle."
          finsi

        """
        if conteneur.est_de_type("conteneur de potion"):
            onces = getattr(conteneur, "onces", 1)
            return [conteneur.potion] * onces if conteneur.potion else []
        elif conteneur.est_de_type("sac de matériau"):
            if conteneur.materiau and conteneur.quantite:
                prototype = conteneur.materiau
                return [prototype] * conteneur.quantite

            return []
        elif conteneur.est_de_type("conteneur de nourriture"):
            return list(conteneur.nourriture)

        elif conteneur.est_de_type("conteneur") or conteneur.est_de_type(
                "machine"):
            return list(conteneur.conteneur._objets)

        raise ErreurExecution("{} n'est pas un conteneur".format(conteneur))
