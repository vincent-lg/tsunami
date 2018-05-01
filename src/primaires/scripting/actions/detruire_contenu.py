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


"""Fichier contenant l'action detruire_contenu."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Détruit le contenu d'un objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.detruire_contenu, "Objet")

    @staticmethod
    def detruire_contenu(objet):
        """Détruit le contenu de l'objet précisé.

        Détruit le contenu d'un conteneur de potion, conteneur de nourriture
        ou conteneur standard (cela inclut les meubles et machines). Dans
        tous les cas, tous le qu'il contient est __DÉFINITIVEMENT__ supprimé.

        Paramètres à préciser :

          * conteneur : l'objet que l'on souhaite vider.

        Exemples d'utilisation :

          # Détruit le contenu dans un pot rempli d'eau, qui devient
          # donc vide.
          detruire_contenu pot
          # La même chose pour un conteneur de nourriture
          detruire_contenu poelon
          # On pour un conteneur standard
          detruire_contenu coffre
          detruire_contenu armoire
          # ...

        """
        if objet.est_de_type("conteneur de potion"):
            objet.potion = None
            objet.onces = 0
            return
        elif objet.est_de_type("conteneur de nourriture"):
            objet.nourriture = []
            return

        if not hasattr(objet, "conteneur"):
            raise ErreurExecution("{} n'est pas un conteneur".format(
                    objet.cle))
        for o in list(objet.conteneur._objets):
            try:
                importeur.objet.supprimer_objet(o.identifiant)
            except KeyError:
                pass

        objet.conteneur._objets = []
        objet.conteneur._non_uniques = []
