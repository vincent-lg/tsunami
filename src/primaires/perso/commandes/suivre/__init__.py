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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'suivre'."""

from primaires.interpreteur.commande.commande import Commande

class CmdSuivre(Commande):

    """Commande 'suivre'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "suivre", "follow")
        self.nom_categorie = "bouger"
        self.schema = "(<personnage_present>)"
        self.aide_courte = "suit un autre personnage"
        self.aide_longue = \
            "Cette commande permet de suivre un personnage présent. " \
            "Vous devez préciser en paramètre un fragment du nom du " \
            "personnage à suivre. Quand ce personnage se déplacera, " \
            "vous vous déplacerez avec lui (cela inclut l'escalade " \
            "ou la nage). Entrez cette commande sans paramètre pour " \
            "arrêter de suivre le personnage."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        personnage.agir("bouger")
        a_suivre = None
        if dic_masques["personnage_present"]:
            a_suivre = dic_masques["personnage_present"].personnage

        if a_suivre:
            # On ajoute le suivi et le suiveur dans le dictionnaire
            importeur.perso.suivre[personnage] = a_suivre
            personnage.envoyer("Vous commencez à suivre {}.", a_suivre)
            a_suivre.envoyer("{} commence à vous suivre.", personnage)
        else:
            if importeur.perso.suivre.get(personnage):
                suivi = importeur.perso.suivre[personnage]
                personnage.envoyer("Vous cessez de suivre {}.", suivi)
                if suivi.salle is personnage.salle:
                    suivi.envoyer("{} cesse de vous suivre.", personnage)
                del importeur.perso.suivre[personnage]
            else:
                personnage << "Vous ne suivez personne actuellement."
