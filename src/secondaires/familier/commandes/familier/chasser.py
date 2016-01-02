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


"""Fichier contenant le paramètre 'chasser' de la commande 'familier'."""

from primaires.format.constantes import ponctuations_finales
from primaires.format.fonctions import echapper_accolades
from primaires.interpreteur.masque.parametre import Parametre

class PrmChasser(Parametre):

    """Commande 'familier chasser'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "chasser", "hunt")
        self.schema = "<nom_familier>"
        self.aide_courte = "demande au fammilier de chasser"
        self.aide_longue = \
            "Cette commande permet d'ordonner à un familier de chasser. " \
            "Un familier carnivore a besoin de recevoir cet ordre " \
            "pour chercher du petit gibier avant de se nourrir. Un familier " \
            "qui chasse pourra s'éloigner petit à petit en quête de " \
            "viande, mais il restera souvent dans le même endroit, se " \
            "déplaçant juste assez pour trouver des proies qu'il pensera " \
            "pouvoir attaquer. Le carnivore qui reçoit l'ordre de " \
            "chasser ne fait pas dans la subtilité : il va se promener " \
            "et attaquer ce qu'il pense être une proie facile. Il aura " \
            "tendance à éviter les prédateurs aussi gros (ou plus " \
            "gros) que lui. Et bien entendu, il ne s'attaquera pas à son " \
            "propre maître. Si il a jugé correctement, il remportera " \
            "le combat et se nourrira sur le gibier qu'il vient de " \
            "tuer. Cette méthode n'est cependant pas sans risque et, " \
            "avec un familier carnivore, il faut considérer la " \
            "possibilité de le laisser dans un chenil ou un endroit " \
            "dans lequel il trouvera de la nourriture sans grand danger."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        fiche = familier.fiche
        if fiche.regime != "carnivore":
            personnage << "|err|{} n'est pas un carnivore.|ff|".format(
                    familier.nom)
            return

        pnj = familier.pnj
        if "chasse" in pnj.etats:
            pnj.etats.retirer("chasse")
            familier.doit_chasser = False
            personnage.salle.envoyer("{} arrête de chasser.", pnj)
            return

        familier.doit_chasser = True
        pnj.etats.ajouter("chasse")
        personnage.salle.envoyer("{} se déplace furtivement, cherchant " \
                "des proies.", pnj)
