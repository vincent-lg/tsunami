# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Package contenant le paramètre 'liste' de la commande 'louer'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'louer liste'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "liste", "list")
        self.tronquer = True
        self.aide_courte = "affiche les chambres libres"
        self.aide_longue = \
            "Cette commande permet de lister les chambres libres d'une " \
            "auberge ainsi que leur prix au jour. Vous devez vous " \
            "trouver auprès d'un aubergiste pour cela. Les chambres " \
            "affichées sont celles libres, c'est-à-dire que celles déjà " \
            "louées ne seront pas listées. Utilisez la commande %louer% " \
            "%louer:chambre% pour louer une chambre libre. Notez que " \
            "le prix affiché est celui pour un jour. Mais le prix pour " \
            "deux jours ne sera pas tout à fait le double du prix pour " \
            "un jour : plus le nombre de jours réservés est élevé, plus " \
            "le prix diminue en proportion. En somme, réserver une " \
            "chambre pour dix jours coûtera moins cher que de réserver " \
            "une chambre pour un jour et la renouveler neuf fois. Si vous " \
            "voulez savoir combien coûterai la location d'une chambre " \
            "pour une durée précise, utilisez la commande %louer% " \
            "%louer:valeur%."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        try:
            auberge = importeur.auberge.get_auberge(personnage.salle)
        except KeyError:
            personnage << "|err|Vous n'êtes pas dans une auberge.|ff|"
            return

        if auberge.aubergiste is None:
            personnage << "|err|Aucun aubergiste n'est présent pour s'en charger.|ff|"
            return

        auberge.verifier_chambres()
        chambres = sorted([c for c in auberge.chambres.values() if \
                c.proprietaire is None], key=lambda c: c.numero)
        en_tete_titre = "+-" + "-" * 25 + "-+"
        en_tete = "+-" + "-" * 9 + "-+-" + "-" * 13 + "-+"
        msg = en_tete_titre + "\n"
        msg += "| " + auberge.titre.ljust(25) + " |\n"
        msg += en_tete + "\n"
        msg += "| Numéro    | Prix par jour |\n"
        msg += en_tete
        for chambre in chambres:
            msg += "\n| " + chambre.numero.ljust(9) + " | "
            msg += str(chambre.prix_par_jour).rjust(13) + " |"

        if not chambres:
            msg += "\n| |att|" + "Aucune chambre disponible".ljust(
                    25) + "|ff| |"

        msg += "\n" + en_tete
        personnage << msg
