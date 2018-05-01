# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 NOEL-BARON Léo
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


"""Package contenant le paramètre 'lister' de la commande 'recettes'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmLister(Parametre):

    """Commande 'recettes lister'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "lister", "list")
        self.schema = "(<texte_libre>)"
        self.aide_courte = "liste les recette"
        self.aide_longue = \
            "Cette commande permet de rechercher dans les recettes " \
            "actuelles. Sans argument, retourne un tableau ordonné des " \
            "recettes. Vous pouvez spécifier un argument pour le moteur " \
            "de recherche (entrez %recette% %recette:lister%|cmd| " \
            "-a|ff| pour voir la liste des options possibles)."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cherchable = importeur.recherche.cherchables["recette"]
        if dic_masques["texte_libre"]:
            chaine = dic_masques["texte_libre"].texte
        else:
            chaine = ""

        message = cherchable.trouver_depuis_chaine(chaine)
        personnage << message
