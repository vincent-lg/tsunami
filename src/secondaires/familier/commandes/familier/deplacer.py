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


"""Fichier contenant le paramètre 'déplacer' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmDeplacer(Parametre):

    """Commande 'familier deplacer'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "déplacer", "move")
        self.schema = "<nom_familier> <nom_sortie>"
        self.tronquer = True
        self.aide_courte = "demande au familier de se déplacer"
        self.aide_longue = \
            "Cette commande permet d'ordonner à un familier, présent " \
            "dans la salle, de se déplacer vers l'une des sorties " \
            "disponibles. Vous devez entrer en premier paramètre le " \
            "nom du familier et en second paramètre la sortie que doit " \
            "prendre le familier. Notez que, si vous pouvez harnacher " \
            "le familier avec une bride (ou même une corde), vous " \
            "pouvez le diriger avec la commande %familier% " \
            "%familier:mener%, ce qui reste malgré tout bien plus " \
            "pratique."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        sortie = dic_masques["nom_sortie"].sortie
        fiche = familier.fiche
        pnj = familier.pnj
        personnage.envoyer("Vous ordonnez à {{}} de se déplacer vers " \
                "{}.".format(sortie.nom_complet), pnj)
        pnj.deplacer_vers(sortie.nom)
