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


"""Package contenant la commande 'manger'."""

from primaires.interpreteur.commande.commande import Commande
from corps.fonctions import lisser

class CmdManger(Commande):
    
    """Commande 'manger'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "manger", "eat")
        self.nom_categorie = "objets"
        self.schema = "<nom_objet>"
        self.aide_courte = "mange un objet"
        self.aide_longue = \
                "Cette commande permet de se nourrir, à condition que " \
                "l'objet précisé soit comestible."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire, )"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        objet = dic_masques["nom_objet"].objet
        
        if hasattr(objet, "nourriture"):
            if not objet.nourriture:
                personnage << "Il n'y a rien à manger là-dedans."
                return
            personnage << "Vous commencez votre repas."
            personnage.agir("manger")
            for item in objet.nourriture:
                item.script["mange"].executer(personnage=personnage,
                        objet=objet)
                item.detruire()
                yield item.nourrissant
            objet.nourriture = []
            personnage << lisser("Vous mangez le contenu de {}.".format(
                    objet.nom_singulier))
            return
        
        if not objet.est_de_type("nourriture"):
            personnage << "Visiblement, ce n'est pas comestible."
            return
        
        objet.script["mange"].executer(personnage=personnage, objet=objet)
        personnage << objet.message_mange
        objet.detruire()
