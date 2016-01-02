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


"""Fichier contenant la fonction ouvrir_sac_materiau."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Crée un sac de matériau."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ouvrir_sac_materiau, "Objet")

    @staticmethod
    def ouvrir_sac_materiau(sac):
        """Ouvre le sac de matériau en extrayant ce qu'il contient.

        Cette fonction extrait du sac de matériau précisé en argument
        les objets contenus, et retourne la liste des objets.
        Il vous appartiendra de les mettre quelque part (les
        poser dans un conteneur ou sur le sol, par exemple).

        Paramètres à préciser :

          * sac : l'objet de type sac

        Exemples d'utilisation :

          # 'sac' contient un sac de farine
          objets = ouvrir_sac_materiau(sac)
          # Et peut-être ensuite
          pour chaque objet dans objets:
              poser salle objet
          fait

        """
        if not sac.est_de_type("sac de matériau"):
            raise ErreurExecution("{} n'est pas un sac de matériau".format(
                    repr(sac.cle)))

        objets = []
        prototype = getattr(sac, "materiau", None)
        quantite = getattr(sac, "quantite", None)
        if prototype and quantite:
            for i in range(quantite):
                objets.append(importeur.objet.creer_objet(prototype))

        importeur.objet.supprimer_objet(sac.identifiant)
        return objets
