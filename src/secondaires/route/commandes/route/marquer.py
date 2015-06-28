# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Package contenant le paramètre 'marquer' de la commande 'route'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmMarquer(Parametre):

    """Commande 'route marquer'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "marquer", "mark")
        self.aide_courte = "marque la salle dans les routes"
        self.aide_longue = \
            "Cette commande ne prend aucun paramètre. Elle permet " \
            "de commencer à marquer une route, ou bien d'en finir " \
            "une. Vous devez entrer cette commande une première fois " \
            "dans la salle d'origine de la future route que vous " \
            "voulez tracer. Parcourez ensuite les sorties " \
            "successives menant à votre destination. Puis utilisez " \
            "cette commande de nouveau pour indiquer au système que " \
            "vous avez fini de marquer cette route. Vous devez vous " \
            "déplacer \"normalement\" entre l'origine et la " \
            "destination cette première fois : n'utilisez pas de " \
            "%goto%. Le système retient toutes les sorties que vous " \
            "empruntez. Si il n'arrive pas à faire le lien, la " \
            "route ne pourra être finalisée."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if personnage in importeur.route.en_cours:
            route = importeur.route.en_cours[personnage]
            importeur.route.enregistrer(personnage)
            personnage << "Vous avez bien enregistré la route {}.".format(
                    route.str_ident)
        else:
            route = importeur.route.enregistrer(personnage)
            msg = \
                "Vous commencez à marquer la route {}.\n" \
                "Déplacez-vous normalement jusqu'à atteindre la " \
                "destination de\ncette route, puis entrez la commande " \
                "à nouveau.".format(route.str_ident)

            personnage << msg
