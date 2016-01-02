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


"""Fichier contenant la fonction PNJ."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne tous les PNJ présents."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.PNJ_salle, "Salle")
        cls.ajouter_types(cls.PNJ_salle, "Salle", "str")
        cls.ajouter_types(cls.tous_PNJ, "str")
        cls.ajouter_types(cls.zone_PNJ, "str", "str")

    @staticmethod
    def PNJ_salle(salle, cle=""):
        """Retourne tous les PNJ présents dans la salle.

        Cette fonction retourne les PNJ présents (pas les joueurs).

        Paramètres à préciser :

          * salle : la salle dans laquelle trouver les PNJ
          * cle (optionnel) : la clé de prototype des PNJ

        Exemple d'utilisation :

          # En admettant qu'une salle est contenue dans la variable salle
          # Capture tous les PNJ d'une salle
          liste = PNJ(salle)
          pour chaque pnj dans liste:
              ...
          fait
          # Capture seulement les PNJ de prototype 'souris'
          liste = PNJ(salle, "souris")
          pour chaque pnj dans liste:
              ...
          fait

        """
        pnj = salle.PNJ
        if cle:
            pnj = [p for p in pnj if p.cle == cle]
        
        return pnj
    
    @staticmethod
    def tous_PNJ(cle_prototype):
        """Retourne tous les PNJ d'un prototype.

        Paramètres à préciser :

          * cle_prototype : la clé du prototype de PNJ

        Vous devez préciser la clé du prototype sous la
        forme d'une chaîne. Une liste contenant tous les
        PNJ du prototype, peu importe l'endroit où ils
        se trouvent, sera retournée. La liste sera
        vide si le prototype n'a aucun PNJ créé
        actuellement. Vous pouvez partir du principe que
        tous les PNJ retournés sont vivants (ceux morts
        sont automatiquement supprimés).

        Utilisez la fonction 'salle' pour connaître la
        salle dans laquelle un PNJ se trouve.

        Exemple d'utilisation :

          pour chaque pnj dans PNJ("marchand_myr"):
              salle = salle(pnj)
              # salle contient la salle du PNJ parcouru

        """
        try:
            prototype = importeur.pnj.prototypes[cle_prototype.lower()]
        except KeyError:
            raise ErreurExecution("prototype inconnu {}".format(
                    repr(cle_prototype)))

        return list(prototype.pnj)

    @staticmethod
    def zone_PNJ(zone, prototype):
        """Retourne les PNJ d'une zone particulière.

        Cette fonction retourne les PNJ d'une clé indiquée d'une zone
        indiquée. Ce peut être très utile de savoir que dans une zone
        donnée, il y a 12 PNJ de ce prototype. C'est encore plus utile
        pour les portions semi-isolées de l'univers (les diligences,
        les navires).

        Paramètres à préciser :

          * zone : la clé de la zone (une chaîne de caractères)
          * prototype : la clé du prototype de PNJ (une chaîne de caractères)

        Exemples d'utilisation :

          # On veut obtenir tous les PNJ 'lapin' de la zone 'depart'
          lapins = PNJ("depart", "lapin")
          # On veut obtenir tous les PNJ 'lapin' de la zone de la
          # salle actuelle (contenue dans la variable salle)
          zone = zone(salle)
          lapins = PNJ(zone, "lapin")

        """
        zone = zone.lower()
        try:
            prototype = importeur.pnj.prototypes[prototype.lower()]
        except KeyError:
            raise ErreurExecution("prototype inconnu {}".format(
                    repr(prototype)))

        return [p for p in prototype.pnj if p.salle and \
                p.salle.nom_zone == zone]
