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
# ARE DISCLAIMED. IN NO Ematelot SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'affecter' de la commande 'matelot'."""

from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.equipage.ordres.revenir import Revenir

class PrmAffecter(Parametre):

    """Commande 'matelot affecter'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "affecter", "affect")
        self.schema = "<nom_matelot>"
        self.tronquer = True
        self.aide_courte = "change l'affectation d'un matelot"
        self.aide_longue = \
            "Cette commande demande à un matelot de changer d'affectation. " \
            "Le matelot précisé en paramètre voit la salle où vous " \
            "vous trouvez devenir sa nouvelle affectation et il tentera " \
            "de s'y rendre dès que sa nouvelle affectation lui sera " \
            "parvenue. Après la plupart des ordres que vous émeterez, " \
            "les matelots retournent à leur salle d'affectation. Plus " \
            "les matelots sont logiquement répartis sur le navire " \
            "(en fonction des différents postes et des abilités de " \
            "chacun), moins ils se déplacent, plus ils sont réactifs " \
            "et moins ils se fatiguent."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        navire = salle.navire
        matelot = dic_masques["nom_matelot"].matelot
        if navire.proprietaire and navire.proprietaire is not personnage and \
                not personnage.est_immortel():
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        equipage = navire.equipage
        affectation = matelot.affectation
        if affectation is salle:
            personnage << "|err|Ce matelot est déjà affecté ici.|ff|"
            return

        msg = "{distinction} s'écrie: {nom}, tu es affecté {titre}.".format(
                distinction=personnage.get_distinction_audible().capitalize(),
                nom=matelot.nom.capitalize(), titre=salle.titre_court.lower())
        navire.envoyer(msg)
        yield 1
        matelot.affectation = salle
        revenir = Revenir(matelot, navire)
        matelot.ordonner(revenir)
        matelot.executer_ordres()
