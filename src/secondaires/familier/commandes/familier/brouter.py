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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'brouter' de la commande 'familier'."""

from primaires.format.constantes import ponctuations_finales
from primaires.format.fonctions import echapper_accolades
from primaires.interpreteur.masque.parametre import Parametre

class PrmBrouter(Parametre):

    """Commande 'familier brouter'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "brouter", "graze")
        self.schema = "<nom_familier>"
        self.aide_courte = "demande au fammilier de brouter"
        self.aide_longue = \
            "Cette commande permet d'ordonner à un familier de brouter " \
            "l'herbe ou les plantes qui l'entourent, ou bien de " \
            "chercher des fruits autour de lui si cela convient mieux " \
            "à ses habitudes alimentaires. C'est utile " \
            "et indispensable si vous possédez des familiers " \
            "herbivores ou frugivores : si vous ne les nourrissez pas, ils " \
            "finissent par mourir du manque d'eau et de nourriture. " \
            "Si ils ont l'ordre de brouter et qu'ils se trouvent dans " \
            "une plaine ou au bord d'un cours d'eau, ils vont " \
            "pouvoir boire et se nourrir, même si vous n'êtes pas " \
            "connecté. Notez que les carnivores chassent pour se " \
            "nourrir. Pour utiliser cette commande, précisez " \
            "simplement le nom du familier : vous devez vous trouver " \
            "dans la même salle que lui. Utilisez la même commande " \
            "pour demander au familier d'arrêter de brouter ou de " \
            "chercher des fruits."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        fiche = familier.fiche
        if fiche.regime not in ("herbivore", "frugivore"):
            personnage << "|err|{} n'est ni herbivore ni " \
                    "frugivore.|ff|".format(familier.nom)
            return

        pnj = familier.pnj
        if "broute" in pnj.etats:
            pnj.etats.retirer("broute")
            personnage.salle.envoyer("{} redresse la tête.", pnj)
            return
        elif "frugi" in pnj.etats:
            pnj.etats.retirer("frugi")
            personnage.salle.envoyer("{} arrête de chercher des fruits.", pnj)
            return

        if fiche.regime == "herbivore":
            pnj.etats.ajouter("broute")
            personnage.salle.envoyer("{} baisse la tête, à la recherche " \
                    "d'herbes et de plantes à manger", pnj)
        elif fiche.regime == "frugivore":
            pnj.etats.ajouter("frugi")
            personnage.salle.envoyer("{} commence à chercher des fruits " \
                    "mûrs ou tombés au sol.", pnj)
