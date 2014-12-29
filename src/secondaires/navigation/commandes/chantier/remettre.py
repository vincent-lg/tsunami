# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'remettre' de la commande 'chantier'."""

from primaires.commerce.transaction import *
from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.constantes import *

class PrmRemettre(Parametre):

    """Commande 'chantier remettre'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "remettre", "launch")
        self.schema = "(<nombre>)"
        self.aide_courte = "remet à l'eau un navire"
        self.aide_longue = \
            "Cette commande demande à un chantier navale vos " \
            "navires actuellement en cale sèche. Un navire en cale " \
            "sèche n'occupe pas de place dans le port mais vous ne " \
            "pourrez l'utiliser sans le remettre à l'eau. Utilisez " \
            "donc cette commande sans argument pour connaître la " \
            "liste des navires que vous avez en cale sèche. Précisez " \
            "le numéro du navire pour demander qu'il soit remis à " \
            "l'eau. Notez que votre navire sera, après quelque temps, " \
            "remis à l'eau à l'endroit exact qui était le sien avant " \
            "d'être mis en cale sèche. Cependant, si un autre navire " \
            "occupe l'emplacement, l'opération ne sera pas possible."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        chantier = importeur.navigation.get_chantier_naval(salle)
        if chantier is None:
            personnage << "|err|Vous ne vous trouvez pas dans un chantier " \
                    "naval.|ff|"
            return

        if salle.magasin is None:
            personnage << "|err|Vous ne vous trouvez pas dans un chantier " \
                    "naval.|ff|"
            return

        magasin = salle.magasin
        vendeur = magasin.vendeur
        if vendeur is None:
            personnage << "|err|Aucun vendeur n'est présent pour l'instant.|ff|"
            return

        navires = chantier.cales_seches
        navires = [n for n in navires if n.proprietaire is personnage]

        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre
            try:
                navire = navires[nombre - 1]
            except IndexError:
                personnage << "|err|Numéro de navire introuvable.|ff|"
                return

            chantier.ajouter_commande(personnage, navire, "remettre", 5)
            personnage << "Votre requête a été envoyée au chantier naval."
        else:
            # On affiche la liste
            if navires:
                msg = "Vos navires en cale sèche :"
                for i, navire in enumerate(navires):
                    msg += "\n|ent|{:>2}|ff| : {}".format(i + 1,
                            navire.desc_survol)

                personnage << msg
            else:
                personnage << "|att|Vous n'avez aucun navire en cale " \
                        "sèche dans ce chantier navale.|ff|"
