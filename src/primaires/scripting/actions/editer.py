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


"""Fichier contenant l'action editer."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Ouvre un éditeur pour le personnage indiqué."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.editer, "Personnage", "Structure")

    @staticmethod
    def editer(personnage, structure):
        """Ouvre un éditeur pour la structure et l'affiche pour le personnage.

        La structure précisée doit être enregistrable, c'est-à-dire
        être dans un groupe et avoir un ID valide. Consultez les
        exemples pour voir comment récupérer ou créer de telles structures.

        Paramètres à renseigner :

          * personnage : le personnage pour lequel afficher l'éditeur
          * structure : une structure enregistrable.

        Exemples d'utilisation :

          # On pourrait récupérer la structure 'journal' d'ID 4 ainsi :
          journal = structure("journal", 4:
          # Ou bien on pourrait créer une nouvelle structure 'journal' :
          journal = creer_structure("journal")
          # Dans tous les cas, on peut ensuite l'éditer
          editer personnage journal
          # Un éditeur 'journal' doit exister. C'est lui qui sera appelé
          # pour éditer la structure. L'éditeur portant le nom du
          # groupe de la structure est toujours utilisé.

        """
        groupe = structure.structure
        if groupe is None:
            raise ErreurExecution("La structure précisée n'est de " \
                    "toute évidence pas enregistrable, elle n'a pas " \
                    "de groupe ni d'ID")

        editeur = importeur.scripting.editeurs.get(groupe)
        if editeur is None:
            raise ErreurExecution("L'éditeur {} pour la structure {} " \
                    "n'a pas été trouvé".format(repr(groupe), structure))

        editeur.editer(personnage, structure)
