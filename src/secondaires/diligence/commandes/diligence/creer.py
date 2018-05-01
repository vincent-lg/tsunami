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


"""Fichier contenant le paramètre 'créer' de la commande 'diligence'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCreer(Parametre):

    """Commande 'diligence créer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "créer", "create")
        self.schema = "<cle>"
        self.aide_courte = "crée une diligence maudite"
        self.aide_longue = \
                "Cette commande permet de créer une diligence maudite. " \
                "Vous devez préciser la clé de la diligence à créer, " \
                "sachant qu'elle ne peut pas être une clé de zone " \
                "existante, car la clé de la diligence sera le nom " \
                "de la zone choisie. Si la création marche " \
                "correctement, la première salle de la diligence sera " \
                "créée et vous pourrez vous y téléporter pour éditer " \
                "cette salle et en ajouter d'autres sans contraintes."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        if cle in importeur.salle.zones:
            personnage << "|err|La zone {} existe déjà.|ff|".format(cle)
            return

        diligence = importeur.diligence.creer_diligence(cle)
        diligence.creer_premiere_salle()

        editeur = importeur.interpreteur.construire_editeur(
                "diledit", personnage, diligence)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()
