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


"""Fichier contenant le paramètre 'apparaître' de la commande 'diligence'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmApparaitre(Parametre):

    """Commande 'diligence apparaître'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "apparaître", "spawn")
        self.tronquer = True
        self.schema = "<cle> <ident_salle>"
        self.aide_courte = "fait apparaître une diligence"
        self.aide_longue = \
                "Cette commande permet de faire apparaître une diligence " \
                "de la clé indiquée. Vous devez préciser en premier " \
                "paramètre la clé de la diligence et en second, " \
                "l'identifiant de la salle (|ent|zone:mnémonique|ff|) " \
                "où faire apparaître la diligence."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.diligence.diligences:
            personnage << "|err|La diligence {} n'existe pas.|ff|".format(cle)
            return

        diligence = importeur.diligence.diligences[cle]
        salle = dic_masques["ident_salle"].salle

        # Vérifications
        if not diligence.ouverte:
            personnage << "|err|Cette diligence n'est pas encore " \
                    "ouvrable.|ff|"
            return

        if salle.sorties.sortie_existe("haut"):
            personnage << "|err|La sortie haut est déjà définie dans " \
                    "{}.|ff|".format(salle.ident)
            return

        cle = diligence.apparaitre()
        origine = importeur.salle.salles.get(cle + ":1")
        if origine is None:
            personnage << "|err|Le début de la diligence est " \
                    "introuvable.|ff|"
            return

        diligence.lier(origine, salle)
        personnage << "|La diligence {} a bien été créée en {}.".format(
                cle, salle.ident)
