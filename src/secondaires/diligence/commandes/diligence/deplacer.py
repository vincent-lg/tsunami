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


"""Fichier contenant le paramètre 'déplacer' de la commande 'diligence'."""

from primaires.interpreteur.masque.parametre import Parametre
from secondaires.diligence.diligence import DiligenceMaudite

class PrmDeplacer(Parametre):

    """Commande 'diligence déplacer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "déplacer", "move")
        self.tronquer = True
        self.schema = "<cle>"
        self.aide_courte = "déplace une diligence"
        self.aide_longue = \
                "Cette commande permet de déplacer aléatoirement une " \
                "diligence d'une salle. Vous devez préciser en paramètre " \
                "la clé de la diligence (identique au nom de zone, " \
                "c'est-à-dire la clé de la diligence-modèle, un " \
                "signe souligné et un nombre)."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.salle.zones:
            personnage << "|err|Cette clé de diligence est introuvable.|ff|"
            return

        salle = importeur.salle.salles.get(cle + ":1")
        if salle is None:
            personnage << "|err|L'entrée de la diligence {} est " \
                    "introuvable.|ff|".format(cle)
            return

        # Vérifie que la salle est bien une entrée de diligence
        dans = False
        for zone in importeur.diligence.zones:
            if salle in zone.salles:
                dans = True
                break

        if not dans:
            personnage << "|err|La salle {} n'est pas une salle de " \
                    "diligence.|ff|".format(salle.ident)
            return

        salle = DiligenceMaudite.deplacer(salle)
        personnage << "La diligence {} se déplace en {}.".format(
                cle, salle.ident)
