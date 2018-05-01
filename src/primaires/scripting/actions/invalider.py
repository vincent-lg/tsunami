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


"""Fichier contenant l'action invalider."""

from primaires.scripting.action import Action

class ClasseAction(Action):

    """Invalide la quête d'un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.invalider_personnage, "Personnage", "str")

    @staticmethod
    def invalider_personnage(personnage, cle_de_quete):
        """Invalide la quête pour le personnage.

        Une quête invalidée ne pourra plus être faite par ce personnage,
        peu importe son niveau, peu importe qu'il l'ait commencé ou
        non.

        Paramètres à préciser :

          * personnage : le personnage pour qui la quête doit être invalidée
          * cle_de_quete : la clé de quête sous la forme d'une chaîne
            de caractères.

        """
        print("J'invalide", personnage, personnage.quetes[cle_de_quete].valide)
        personnage.quetes[cle_de_quete].valide = False
        print("Jai invalidé", id(personnage), personnage.quetes[cle_de_quete].valide)
