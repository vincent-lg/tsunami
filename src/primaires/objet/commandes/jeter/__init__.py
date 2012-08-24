# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Package contenant la commande 'jeter'."""

from primaires.interpreteur.commande.commande import Commande

class CmdJeter(Commande):
    
    """Commande 'jeter'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "jeter", "throw")
        self.nom_categorie = "objets"
        self.schema = "<nom_objet> sur/to <element_observable>"
        self.aide_courte = "jète un objet"
        self.aide_longue = \
                "Cette commande permet de jeter un objet vers ou sur " \
                "quelque chose ou quelqu'un. Vous devez posséder l'objet " \
                "devant être jeté (soit dans une main, soit dans l'un de " \
                "vos sacs) et la cible peut être autant un objet, un " \
                "personnage, un détail descriptif... |att|Cette commande " \
                "n'en est encore qu'à ses premiers stades de développement. " \
                "De nouvelles choses seront ajoutées par la suite.|ff|"
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple.iter_objets_qtt(" \
                "True), )"
        nom_objet.proprietes["quantite"] = "True"
        nom_objet.proprietes["conteneur"] = "True"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("jeter")
        objet, qtt, conteneur = list(dic_masques[ \
                "nom_objet"].objets_qtt_conteneurs)[0]
        elt = dic_masques["element_observable"].element
        nom = objet.veut_jeter(personnage, elt)
        if nom:
            print(conteneur, objet)
            conteneur.retirer(objet)
            tentative = objet.jeter(personnage, elt)
            if not tentative:
                return
            
            getattr(objet, nom)(personnage, elt)
        else:
            personnage << "|err|Vous ne pouvez jeter {} sur {}.".format(
                    objet.get_nom(), elt)
