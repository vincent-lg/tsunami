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


"""Package contenant la commande 'remplir'."""

from primaires.interpreteur.commande.commande import Commande

class CmdRemplir(Commande):
    
    """Commande 'remplir'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "remplir", "fill")
        self.nom_categorie = "objets"
        self.schema = "<plat:nom_objet> avec/with (<nombre>) <nom_objet>"
        self.aide_courte = "remplit un plat de nourriture"
        self.aide_longue = \
                "Cette commande permet de manipuler des plats (assiette, " \
                "bol voire poêlon, marmite) en y mettant des objets de type " \
                "nourriture. Un repas pris de cette manière sera meilleur " \
                "et plus nourrissant."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple.iter_objets_qtt(" \
                "True), )"
        nom_objet.proprietes["quantite"] = "True"
        nom_objet.proprietes["conteneur"] = "True"
        plat = self.noeud.get_masque("plat")
        plat.prioritaire = True
        plat.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire, " \
                "personnage.salle.objets_sol)"
        plat.proprietes["types"] = "('conteneur de nourriture', " \
                "'conteneur de potion')"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("poser")
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre
        objets = list(dic_masques["nom_objet"].objets_qtt_conteneurs)[:nombre]
        dans = dic_masques["plat"].objet
        
        pose = 0
        poids_total = dans.poids
        for objet, qtt, conteneur in objets:
            if not objet.peut_prendre:
                personnage << "Vous ne pouvez pas prendre {} avec vos " \
                        "mains...".format(objet.get_nom())
                return
            
            if not objet.est_de_type("nourriture"):
                personnage << "|err|Ceci n'est pas de la nourriture.|ff|"
                return
            
            poids_total += objet.poids
            if poids_total > dans.poids_max:
                if pose == 0:
                    personnage << "Vous ne pouvez rien y poser de plus."
                    return
                else:
                    break
            
            pose += 1
            if qtt > nombre:
                qtt = nombre
            
            conteneur.retirer(objet, qtt)
            dans.nourriture.append(objet)
        
        if pose < qtt:
            pose = qtt
        
        personnage << "Vous déposez {} dans {}.".format(
                objet.get_nom(pose), dans.nom_singulier)
        personnage.salle.envoyer("{{}} dépose {} dans {}.".format(
                objet.get_nom(pose), dans.nom_singulier), personnage)
