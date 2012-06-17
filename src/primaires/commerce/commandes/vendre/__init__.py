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

class CmdVendre(Commande):
    
    """Commande 'vendre'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "vendre", "sell")
        self.nom_categorie = "objets"
        self.schema = "(<nombre>) <nom_objet>"
        self.aide_courte = "vend un objet"
        self.aide_longue = \
            "Cette commande permet de vendre des objets dans un magasin."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = "(personnage.equipement.tenus, )"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("poser")
        personnage << "|err|Cette commande n'est pas utilisable " \
                "pour l'instant.|ff|"
        return
        
        salle = personnage.salle
        if salle.magasin is None:
            personnage << "|err|Il n'y a pas de magasin ici.|ff|"
            return
        nb_obj = dic_masques["nombre"].nombre if \
            dic_masques["nombre"] is not None else 1
        liste_obj = dic_masques["nom_objet"].objets[:nb_obj]
        objet = dic_masques["nom_objet"].objet
        
        # Vérifications avant de valider la vente
        if (objet.prix / 2) * nb_obj > salle.magasin.caisse:
            personnage << "|err|Pas assez d'argent en caisse.|ff|"
            return
        
        # Tout est bon, on donne l'argent
        
        # Vente de l'objet
        for o in liste_obj:
            o[0].detruire()
        salle.magasin[objet.cle] += nb_obj
        personnage << "Vous vendez {}.".format(objet.get_nom(nb_obj))
