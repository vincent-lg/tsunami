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


"""Module contenant la commande 'scripting alerte rebase'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmRebase(Parametre):

    """Commande 'scripting alerte rebase'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "rebase", "rebase")
        self.nom_groupe = "administrateur"
        self.aide_courte = "re-numérote les alertes"
        self.aide_longue = \
            "Cette commande permet de réordonner les alertes en les " \
            "numérotant proprement de 1 à N. Ceci est souvent un " \
            "plus si le nombre d'alertes commence à devenir important " \
            "et leur ID est trop élevé."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        alertes = sorted(list(importeur.scripting.alertes.values()),
                key=lambda a: a.no)
        for i, alerte in enumerate(alertes):
            del importeur.scripting.alertes[alerte.no]
            alerte.no = i + 1
            importeur.scripting.alertes[i + 1] = alerte

        type(alerte).no_actuel = len(alertes)
        personnage << "{} alertes renumérotées.".format(len(alertes))
