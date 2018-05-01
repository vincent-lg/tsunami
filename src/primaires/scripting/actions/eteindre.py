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


"""Fichier contenant l'action eteindre."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Eteint la lumière d'une salle"""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.eteindre_salle, "Salle")

    @staticmethod
    def eteindre_salle(salle):
        """Éteint la lumière d'une salle.

        Paramètres à préciser :

          * salle : la salle qui doit voir son illumination désactivée

        Cette fonction éteint une salle, c'est-à-dire modifie
        son flag 'illuminée'. Si la salle n'est pas illuminée, rien
        ne sera fait. Une salle illuminée peut être vue par tous,
        qu'ils aient des torches ou non. En combinaison avec l'action
        'allumer', cette action permet de faire varier le flag
        illuminée d'une salle, ce qui peut être utile par exemple
        si un marchand entre dans son magasin au matin et
        allume les lampes.

        NOTE : cette action ne modifie pas le statut des personnages
        présents. Ils pourront toujours s'éclairer grâce à des torches,
        des sorts ou autre. Si ils sont nyctalopes, ils y verront
        toujours. Si il y a un feu dans la salle, le feu continuera
        d'éclairer les lieux.

        Exemple d'utilisation :

          eteindre salle

        """
        salle.illuminee = False
