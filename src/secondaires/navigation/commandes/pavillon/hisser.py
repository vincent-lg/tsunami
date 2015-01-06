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


"""Fichier contenant le paramètre 'hisser' de la commande 'pavillon'."""

from corps.fonctions import lisser
from primaires.interpreteur.masque.parametre import Parametre

class PrmHisser(Parametre):

    """Commande 'pavillon hisser'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "hisser", "up")
        self.schema = "<nom_objet>"
        self.aide_courte = "hisse le pavillon"
        self.aide_longue = \
            "Cette commande vous permet de hisser un pavillon en " \
            "tête de mât (ou tout autre moyen disponible dans cette " \
            "embarcation pour montrer vos couleurs). Vous devez " \
            "préciser en paramètre un fragment du nom du pavillon " \
            "hissé. Le pavillon doit être un objet présent dans " \
            "votre inventaire."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple.iter_objets_qtt(" \
                "True), )"
        nom_objet.proprietes["quantite"] = "True"
        nom_objet.proprietes["conteneur"] = "True"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        personnage.agir("poser")
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        pavillon = navire.pavillon
        if pavillon:
            personnage << "|err|Il y a déjà un pavillon hissé.|ff|"
            return

        objets = list(dic_masques["nom_objet"].objets_qtt_conteneurs)
        objets = [c[0] for c in objets]
        pavillon = objets[0]
        if not pavillon.est_de_type("pavillon"):
            personnage << "|err|{} n'est pas un pavillon.|ff|".format(
                    pavillon.get_nom().capitalize())
            return

        navire.pavillon = pavillon.prototype
        navire.envoyer("{} est hissé en tête de mât.".format(
                pavillon.get_nom().capitalize()))
        navire.envoyer_autour(lisser("{} est hissé en tête de mat de " \
                "{}.".format(pavillon.get_nom().capitalize(),
                navire.desc_survol)), 10)
        importeur.objet.supprimer_objet(pavillon.identifiant)
