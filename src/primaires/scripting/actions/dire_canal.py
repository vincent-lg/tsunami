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
# LIABLE FOR ANY dire_canalCT, INdire_canalCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action dire_canal."""

import textwrap

from primaires.scripting.action import Action

class ClasseAction(Action):

    """Envoi un message sur un canal précisé."""

    entrer_variables = True

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.dire_canal, "str", "str")

    @staticmethod
    def dire_canal(nom_canal, message, variables=None):
        """Envoie un message au canal.

        Les paramètres attendus sont :

          * nom_canal : le nom du canal (par exemple "imm")
          * message : le message à envoyer au canal

        Exemple d'usage :
            envoyer_canal "info" "Ouverture de zone !"

        Vous pouvez très bien utiliser des variables dans la chaîne,
        comme pour dire. Par exemple :
            nom = nom(personnage)
            dire_canal "imm" "Le joueur ${nom} vient d'accomplir cette quête"

        """
        try:
            canal = importeur.communication.canaux[nom_canal]
        except KeyError:
            raise ErreurExecution("le canal {} n'existe pas".format(repr(
                    nom_canal)))

        message = message.format(**variables)
        espace = "\n" + (len(canal.nom) + 3 ) * " "
        message = espace.join(textwrap.wrap(message, 65))
        canal.envoyer_imp(message)
