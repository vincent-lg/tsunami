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


"""Package contenant la commande 'donner'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.objet.conteneur import SurPoids

class CmdDonner(Commande):
    
    """Commande 'donner'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "donner", "give")
        self.nom_categorie = "objets"
        self.schema = "(<nombre>) <nom_objet> " \
                "a/to <cible:personnage_present|nom_pnj>"
        self.aide_courte = "donne un objet"
        self.aide_longue = \
                ""
    
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
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre
        objets = list(dic_masques["nom_objet"].objets_qtt_conteneurs)[:nombre]
        if hasattr(dic_masques["cible"], "personnage"):
            cible = dic_masques["cible"].personnage
        else:
            cible = dic_masques["cible"].pnj
        
        donne = 0
        for objet, qtt, conteneur in objets:
            if not objet.peut_prendre:
                personnage << "Vous ne pouvez pas prendre {} avec vos " \
                        "mains...".format(objet.nom_singulier)
                return
            if qtt > nombre:
                qtt = nombre
            
            try:
                dans = cible.ramasser(objet, qtt=qtt)
            except SurPoids:
                personnage << "{} ne peut rien porter de plus.".format(
                        cible.get_nom_pour(personnage))
                return
            
            if dans is None:
                break
            conteneur.retirer(objet, qtt)
            donne += 1
        
        if donne == 0:
            personnage << "{} ne peut pas prendre cela.".format(
                    cible.get_nom_pour(personnage))
            return
        
        if donne < qtt:
            donne = qtt
        
        personnage << "Vous donnez {} à {}.".format(objet.get_nom(donne),
                cible.get_nom_pour(personnage))
        if not hasattr(cible, "prototype"):
            cible << "{} vous donne {}.".format(personnage.get_nom_pour(cible),
                    objet.get_nom(donne))
        personnage.salle.envoyer("{{}} donne {} à {{}}.".format(
                objet.get_nom(donne)), personnage, cible)
        
        # Appel de l'évènement 'donne' du PNJ
        if hasattr(cible, "prototype"):
            cible.script["donne"].executer(objet=objet, quantite=donne,
                    personnage=personnage, pnj=cible)
