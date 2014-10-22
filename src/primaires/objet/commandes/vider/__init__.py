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


"""Package contenant la commande 'vider'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.objet.conteneur import SurPoids

class CmdVider(Commande):
    
    """Commande 'vider'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "vider", "empty")
        self.nom_categorie = "objets"
        self.schema = "(<nombre>) <nom_objet> depuis/from <plat:nom_objet>"
        self.aide_courte = "vide un plat"
        self.aide_longue = \
                "Cette commande permet d'enlever un ou plusieurs objets " \
                "d'un plat, du moins si l'opération est faisable (difficile " \
                "par exemple de retirer une soupe d'un bol autrement qu'en " \
                "la mangeant)."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(dic_masques['plat'].objet.nourriture, )"
        plat = self.noeud.get_masque("plat")
        plat.prioritaire = True
        plat.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire, " \
                "personnage.salle.objets_sol)"
        plat.proprietes["types"] = "('conteneur de nourriture', )"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("prendre")
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre
        objets = list(dic_masques["nom_objet"].objets)
        objets = objets[:nombre]
        plat = dic_masques["plat"].objet
        
        pris = 0
        for objet in objets:
            if not objet.peut_prendre:
                personnage << "Vous ne pouvez pas prendre {} avec vos " \
                        "mains...".format(objet.nom_singulier)
                return
            try:
                dans = personnage.ramasser(objet, plat)
            except SurPoids as err:
                personnage << "|err|" + str(err) + "|ff|"
                return
            if dans is None:
                break
            plat.nourriture.remove(objet)
            pris += 1
            
        if pris == 0:
            personnage << "|err|Vous n'avez aucune main de libre.|ff|"
            return
        
        personnage << "Vous prenez {} depuis {}.".format(
                objet.get_nom(pris), plat.nom_singulier)
        personnage.salle.envoyer("{{}} prend {} depuis {}.".format(
                objet.get_nom(pris), plat.nom_singulier), personnage)
