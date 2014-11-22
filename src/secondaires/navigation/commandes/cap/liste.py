# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Package contenant la commande 'cap liste'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'cap liste'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "affiche la liste des caps"
        self.aide_longue = \
            "Cette commande permet d'afficher la liste des " \
            "caps maritimes. Un cap qui n'a qu'un seul point n'est " \
            "pas utilisable."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande."""
        trajets = list(importeur.navigation.trajets.values())
        trajets.sort(key=lambda t: t.cle)
        if not trajets:
            personnage << "|att|Aucun cap maritime n'a été créé.|ff|"
            return

        msg = "Caps existants :\n"
        for trajet in trajets:
            s = "s" if len(trajet.points) > 1 else ""
            msg += "\n  {:<20} {} point{s}".format(trajet.cle,
                    len(trajet.points), s=s)

        personnage << msg
