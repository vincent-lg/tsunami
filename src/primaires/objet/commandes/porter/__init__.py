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


"""Package contenant la commande 'porter'."""

from primaires.interpreteur.commande.commande import Commande

class CmdPorter(Commande):
    
    """Commande 'porter'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "porter", "wear")
        self.nom_categorie = "objets"
        self.schema = "<nom_objet>"
        self.aide_courte = "équipe un objet"
        self.aide_longue = \
                "Cette commande permet d'équiper des objets (vêtements, " \
                "armures, armes...). Vous devez pour cela avoir au moins " \
                "une main libre, ainsi qu'un emplacement corporel adéquat " \
                "(un pied nu pour une chaussette)."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple, )"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        objets = list(dic_masques["nom_objet"].objets_conteneurs)[0]
        objet, conteneur = objets
        personnage.agir("porter")
        
        if personnage.equipement.cb_peut_tenir() < 1:
            personnage << "|err|Il vous faut au moins une main libre pour " \
                    "vous équiper.|ff|"
            return
        
        for membre in personnage.equipement.membres:
            if membre.peut_equiper(objet):
                objet.contenu.retirer(objet)
                membre.equiper(objet)
                personnage << "Vous équipez {}.".format(objet.nom_singulier)
                personnage.salle.envoyer(
                    "{{}} équipe {}.".format(objet.nom_singulier), personnage)
                return
        
        personnage << "|err|Vous ne pouvez équiper {}.|ff|".format(
                objet.nom_singulier)
