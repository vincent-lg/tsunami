# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Package contenant la commande 'aide'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.information.contextes.page import Page


class CmdAide(Commande):
    
    """Commande 'aide'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "aide", "help")
        self.nom_categorie = "info"
        self.schema = "(<message>)"
        self.aide_courte = "affiche de l'aide"
        self.aide_longue = \
            "Cette commande permet d'obtenir de l'aide en jeu. Sans " \
            "argument, elle affiche une liste des sujets d'aides " \
            "disponibles. Vous pouvez entrer %aide% |cmd|<nom du sujet>|ff| " \
            "pour obtenir de l'aide sur ce sujet en particulier."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if dic_masques["message"]:
            titre = dic_masques["message"].message
            sujet = importeur.information.get_sujet(titre)
            if sujet is None or not \
                    importeur.interpreteur.groupes.explorer_groupes_inclus(
                    personnage.grp, sujet.str_groupe):
                personnage << "|err|Il n'y a pas d'aide à ce sujet, désolé.|ff|"
            else:
                texte = sujet.afficher_pour(personnage)
                contexte = Page(personnage.instance_connexion, texte)
                personnage.contexte_actuel.migrer_contexte(contexte)
        else:
            personnage << importeur.information.construire_sommaire_pour(
                    personnage)
