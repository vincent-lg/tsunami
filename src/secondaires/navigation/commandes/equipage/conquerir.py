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
# ARE DISCLAIMED. IN NO Eéquipage SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'conquérir' de la commande 'équipage'."""

from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.constantes import PCT_XP, est_capturable

class PrmConquerir(Parametre):

    """Commande 'équipage conquérir'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "conquérir", "conquer")
        self.tronquer = True
        self.aide_courte = "conquit un navire et équipage"
        self.aide_longue = \
            "Cette commande permet de conquérir un navire adverse : " \
            "si vous en avez le droit, vous en deviendrez son " \
            "propriétaire. Vous aurez également les droits de commander " \
            "les matelots de l'équipage. Vous pouvez utiliser cette " \
            "commande si vous abordez un navire adverse : il ne vous " \
            "sera pas possible de conquérir un navire dont l'équipage " \
            "est encore complet ou presque complet, mais si il est " \
            "affaibli (des matelots ont été tués), conquérir le navire " \
            "aura pour effet de rendre les matelots conquis dociles " \
            "et prêts à exécuter vos ordres. Si le navire adverse " \
            "a déjà un propriétaire, vous ne pourrez pas le conquérir, " \
            "à moins que l'ancien propriétaire ne soit mort."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        navire = getattr(salle, "navire", None)
        if navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        if navire.immobilise or not navire.modele.peut_conquerir or \
                (navire.proprietaire and navire.proprietaire.est_vivant()):
            personnage << "|err|Vous ne pouvez conquérir ce navire.|ff|"
            return

        actuels = getattr(navire.equipage, "points_actuels", 0)
        if not est_capturable(navire, actuels):
            personnage << "|err|L'équipage de ce navire ne s'est pas " \
                    "rendu.|ff|"
            return

        navire.proprietaire = personnage
        navire.equipage.pirate = False
        personnage << "Vous êtes le nouveau propriétaire de ce navire !"
        xp = importeur.perso.gen_niveaux.grille_xp[navire.modele.niveau][1]
        xp = xp * PCT_XP / 100
        personnage.gagner_xp("navigation", xp)
