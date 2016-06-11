# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 NOEL-BARON Léo
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


"""Package contenant la commande 'trouver'."""

from primaires.interpreteur.commande.commande import Commande

class CmdTrouver(Commande):

    """Commande 'trouver'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "trouver", "find")
        self.groupe = "administrateur"
        self.nom_categorie = "divers"
        self.schema = "<cherchable> (<message>)"
        self.aide_courte = "permet de rechercher dans l'univers"
        self.aide_longue = \
                "Cette commande est le moteur de recherche de l'univers. " \
                "Elle permet d'effectuer des recherches dans diverses " \
                "catégories, selon des paramètres optionnels fins (la " \
                "syntaxe est celle des options sous Linux). Pour plus de " \
                "l'aide sur une catégorie en particulier, entrez %trouver% " \
                "|cmd| <objet de la recherche> -a|ff|/|cmd|--aide|ff|. Les " \
                "objets de recherche disponibles sont : "
        self.aide_longue += ", ".join(
                sorted([c for c in importeur.recherche.cherchables.keys()])) + \
                        "."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cherchable = dic_masques["cherchable"].cherchable
        if dic_masques["message"]:
            chaine = dic_masques["message"].message
        else:
            chaine = ""

        message = cherchable.trouver_depuis_chaine(chaine)
        personnage << message
