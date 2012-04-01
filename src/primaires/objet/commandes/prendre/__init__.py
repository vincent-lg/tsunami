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


"""Package contenant la commande 'prendre'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.objet.conteneur import SurPoids

class CmdPrendre(Commande):
    
    """Commande 'prendre'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "prendre", "get")
        self.nom_categorie = "objets"
        self.schema = "(<nombre>) <nom_objet> " \
                "(depuis/from <conteneur:nom_objet>)"
        self.aide_courte = "ramasse un objet"
        self.aide_longue = \
                "Cette commande permet de ramasser un ou plusieurs objets."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "dic_masques['conteneur'] and " \
                "(dic_masques['conteneur'].objet.conteneur.iter_nombres(), " \
                ") or (personnage.salle.objets_sol.iter_nombres(), )"
        nom_objet.proprietes["quantite"] = "True"
        conteneur = self.noeud.get_masque("conteneur")
        conteneur.prioritaire = True
        conteneur.proprietes["conteneurs"] = \
                "(personnage.equipement.tenus.iter_nombres(), " \
                "personnage.salle.objets_sol.iter_nombres())"
        conteneur.proprietes["types"] = "('conteneur', )"
        conteneur.proprietes["quantite"] = "True"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre
        objets = list(dic_masques["nom_objet"].objets_qtt_conteneurs)
        objets = objets[:nombre]
        depuis = dic_masques["conteneur"]
        depuis = depuis and depuis.objet or None
        
        pris = 0
        for objet, qtt, conteneur in objets:
            if nombre > qtt:
                nombre = qtt
            try:
                dans = personnage.ramasser(objet, depuis, nombre)
            except SurPoids as err:
                personnage << "|err|" + str(err) + "|ff|"
                return
            
            if dans is None:
                break
            
            if depuis:
                depuis.conteneur.retirer(objet, nombre)
            else:
                personnage.salle.objets_sol.retirer(objet, nombre)
            pris += 1
            
        if pris == 0:
            personnage << "|err|Vous n'avez aucune main de libre.|ff|"
            return
        
        if pris < nombre:
            pris = nombre
        
        if depuis:
            personnage << "Vous prenez {} depuis {}.".format(
                    objet.get_nom(pris), depuis.nom_singulier)
            personnage.salle.envoyer("{{}} prend {} depuis {}.".format(
                    objet.get_nom(pris), depuis.nom_singulier), personnage)
        else:
            personnage << "Vous ramassez {}.".format(objet.get_nom(pris))
            personnage.salle.envoyer("{{}} ramasse {}.".format(
                    objet.get_nom(pris)), personnage)
