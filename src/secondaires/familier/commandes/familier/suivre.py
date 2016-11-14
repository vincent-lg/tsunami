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


"""Fichier contenant le paramètre 'suivre' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmSuivre(Parametre):

    """Commande 'familier suivre'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "suivre", "follow")
        self.schema = "<nom_familier>"
        self.aide_courte = "demande à un familier de vous suivre"
        self.aide_longue = \
            "Cette commande demande à un familier se trouvant dans " \
            "la même salle que vous de vous suivre. Vous devez préciser " \
            "en paramètre le nom du familier. Utilisez la même commande " \
            "pour demander au familier d'arrêter de vous suivre. Le " \
            "familier doit connaître le tour consistant à suivre son " \
            "maître sans laisse ou bride, ce qui n'est pas donné à " \
            "tous les familiers. Certains d'entre eux apprendront " \
            "ce tour en devenant plus puissant, mais d'autres ne " \
            "le pourront tout simplement pas."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        familier = self.noeud.get_masque("nom_familier")
        familier.proprietes["salle_identique"] = "True"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        fiche = familier.fiche
        pnj = familier.pnj
        if pnj in importeur.perso.suivre:
            del importeur.perso.suivre[pnj]
            pnj << "Vous cessez de suivre votre maître."
            personnage << "{} cesse de vous suivre.".format(
                    familier.nom)
        else:
            if "suivre_maitre" not in familier.tours:
                personnage << "|err|{} ne connaît pas ce tour.|ff|".format(
                        familier.nom)
                return

            importeur.perso.suivre[pnj] = personnage
            pnj << "Vous commencez à suivre votre maître."
            personnage << "{} commence à vous suivre.".format(
                    familier.nom)
