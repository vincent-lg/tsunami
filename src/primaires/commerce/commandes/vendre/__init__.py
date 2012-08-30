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


"""Package contenant la commande 'vendre'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.commerce.transaction import *

class CmdVendre(Commande):
    
    """Commande 'vendre'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "vendre", "sell")
        self.nom_categorie = "objets"
        self.schema = "(<nombre>) <nom_objet>"
        self.aide_courte = "vend un ou plusieurs objet(s)"
        self.aide_longue = \
            "Cette commande permet de vendre des objets dans un magasin."
    
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
        personnage.agir("poser")
        
        salle = personnage.salle
        magasin = salle.magasin
        if magasin is None:
            personnage << "|err|Il n'y a pas de magasin ici.|ff|"
            return
        
        vendus = 0
        a_prototype = None
        objets = list(dic_masques["nom_objet"].objets_qtt_conteneurs)
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre
        
        argent = {}
        for objet, qtt, conteneur in objets:
            if a_prototype and objet.prototype is not a_prototype:
                break
            
            if vendus + qtt > nombre:
                qtt = nombre - vendus
            
            valeur = magasin.peut_acheter(personnage, objet, qtt)
            if isinstance(valeur, bool) and not valeur:
                break
            
            # On crée la transaction associée
            transaction = Transaction.initier(personnage, magasin, -valeur)
            
            # On prélève l'argent
            transaction.payer()
            
            # Ajout à l'argent rendu
            for t_argent, t_qtt in transaction.argent_rendu.items():
                if t_argent in argent:
                    argent[t_argent] += t_qtt
                else:
                    argent[t_argent] = t_qtt
            
            # Distribution des objets
            conteneur.retirer(objet, qtt)
            magasin.ajouter_inventaire(objet.prototype, qtt)
            
            vendus += qtt
            a_prototype = objet.prototype
            if vendus >= nombre:
                break
        
        if vendus == 0:
            return
        
        personnage << "Vous vendez {} pour {}.".format(a_prototype.get_nom(vendus),
                transaction.aff_argent(argent))
        personnage.salle.envoyer("{{}} vend {}.".format(a_prototype.get_nom(
                vendus)), personnage)
