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

"""Fichier contenant la fonction attributs."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Retourne vrai si la salle a l'attribut de météo indiqué."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.attributs, "Salle", "str")

    @staticmethod
    def attributs(salle, attributs):
        """Retourne vrai si la salle a l'attribut de météo indiqué.

        Les perturbations météorologiques ont des attributs qui
        les caractérisent. Par exemple, un nuage de neige est un
        nuage (un attribut) et de couleur blanc (un second attribut).
        Il existe une grande variété d'attributs qui permettent de
        varier les descriptions dynamiques, entre autres usages.
        Voir les exemples ci-dessous. La liste des attributs est
        également donnée.

        Paramètres à préciser :

          * salle : la salle courante ;
          * attributs : une chaîne contenant un ou plusieurs attributs.

        Pour renseigner plusieurs attributs, il faut les séparer
        par une barre verticale (|). Le système retournera alors
        vrai si la perturbation au-dessus de la salle contient l'un
        des attributs mentionnés.

        Attributs actuels :

          * Précipitations : averse, pluie, neige, grêle.
          * Couleurs du ciel : noir, gris, blanc.
          * Visibilité : clair, nuage, brouillard.
          * Température : glacial, doux, tiède, chaud.
          * Humidité : sec, humide.
          * Mouvements : immobile, brise, vent, tempête.

        Pour savoir quel attribut est actif sur quelle perturbation,
        entrez la commande **meteo créer/create** sans paramètre.

        Exemples d'utilisation :

          # La salle 'salle' se trouve sous une tempête de neige
          # La tempête de neige a les attributs neige, blanc,
          # nuage, glacial, humide et tempête
          si attributs(salle, "humide"):
              # vrai
          finsi
          si attributs(salle, "sec"):
              # Faux
          finsi
          si attributs(salle, "soleil|vent|neige"):
              # Vrai, l'attribut neige est actif
          finsi
          # Si la salle n'est sous aucune perturbation, les attributs clair,
          # sec, immobile, doux sont actifs.

        """
        expressions = supprimer_accents(attributs.lower())
        soleil = ("clair", "immobile", "sec", "doux")
        if salle.interieur:
            attributs = soleil
        else:
            perturbation = importeur.meteo.salles.get(salle)
            if perturbation is None:
                attributs = soleil
            else:
                attributs = perturbation.attributs

        attributs = [supprimer_accents(a) for a in attributs]
        return any(e in attributs for e in expressions.split("_b_"))
