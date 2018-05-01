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


"""Package contenant la commande 'chercher'."""

from primaires.interpreteur.commande.commande import Commande

class CmdChercher(Commande):

    """Commande 'chercher'"""

    def __init__(self):
        """Constructeur de la commande."""
        Commande.__init__(self, "chercher", "lookfor")
        self.schema = "<texte_libre>"
        self.nom_categorie = "bouger"
        self.aide_courte = "permet de chercher quelque chose"
        self.aide_longue = \
            "Cette commande permet de chercher quelque chose dans la " \
            "salle où vous vous trouvez. Vous devez entrer ce que vous " \
            "souhaitez trouver : il peut s'agir d'un mot contenu dans " \
            "la description ou dans celle d'un détail ou alors de " \
            "quelque chose de plus subtile. C'est une commande " \
            "d'exploration avancée, c'est-à-dire que vous n'en aurez " \
            "pas l'utilité dans toutes les salles, mais il pourra " \
            "être utile parfois de chercher sous une pile de " \
            "couvertures par exemple. Préférez préciser l'information " \
            "à rechercher en un seul mot (il est possible d'en mettre " \
            "plus mais ce sera bien moins courant)."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        texte = dic_masques["texte_libre"].texte
        personnage.agir("bouger")
        salle = personnage.salle
        personnage << "Vous commencez à chercher {}.".format(texte)
        salle.envoyer("{} commence à chercher quelque chose...", personnage)
        personnage.etats.ajouter("recherche")
        yield 7
        if "recherche" in personnage.etats:
            personnage.etats.retirer("recherche")
            nb = salle.script["recherche"].executer(personnage=personnage,
                    salle=salle, texte=texte)
            if nb == 0:
                personnage << "Vous n'avez rien trouvé qui vaille la " \
                        "peine d'en parler."
