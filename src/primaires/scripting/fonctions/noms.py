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


"""Fichier contenant la fonction noms."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Renvoie une liste de noms de plusieurs informations.

    En paramètre de cette fonction doit être précisé le type
    d'information souhaitée. Par exemple, :

      identifiants = noms("salle")
      # identifiants contient la liste des identifiants de salle

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.noms, "str")

    @staticmethod
    def noms(type):
        """Retourne les noms des informations demandées.

        Paramètres à préciser :

          * type : le type d'information (voir plus bas).

        Types possibles :

          * "joueur" : retourne le nom des joueurs ;
          * "salle" : retourne les identifiants de toutes les salles.

        Exemples d'utilisation :

          noms = noms("joueur")
          # noms contient la liste des noms de tous les joueurs
          identifiants = noms("salle")

        """
        type = type.lower()
        if type == "joueur":
            return [j.nom for j in importeur.joueur.joueurs.values()]
        elif type == "salle":
            return [s.ident for s in importeur.salle._salles.values()]
        else:
            raise ErreurExecution("Type inconnu {}".format(repr(type)))
