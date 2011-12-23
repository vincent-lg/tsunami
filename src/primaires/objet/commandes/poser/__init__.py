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


"""Package contenant la commande 'poser'."""

from primaires.interpreteur.commande.commande import Commande

class CmdPoser(Commande):
    
    """Commande 'poser'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "poser", "drop")
        self.nom_categorie = "objets"
        self.schema = "(<nombre>) <nom_objet> " \
                "(dans/into <conteneur:nom_objet>)"
        self.aide_courte = "pose un objet"
        self.aide_longue = \
                "Cette commande permet de poser un ou plusieurs objets."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.tenus, )"
        conteneur = self.noeud.get_masque("conteneur")
        conteneur.prioritaire = True
        conteneur.proprietes["conteneurs"] = \
                "(personnage.equipement.tenus, personnage.salle.objets_sol)"
        conteneur.proprietes["type"] = "'conteneur'"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre
        objets = dic_masques["nom_objet"].objets[:nombre]
        dans = dic_masques["conteneur"]
        dans = dans and dans.objet or None
        
        pose = 0
        for objet, conteneur in objets:
            conteneur.retirer(objet)
            if dans:
                dans.conteneur.ajouter(objet)
            else:
                personnage.salle.objets_sol.ajouter(objet)
            pose += 1
        
        if dans:
            personnage << "Vous posez {} dans {}.".format(
                    objet.get_nom(pose), dans.nom_singulier)
            personnage.salle.envoyer("{{}} pose {} dans {}.".format(
                        objet.get_nom(pose), dans.nom_singulier), personnage)
        else:
            personnage << "Vous déposez {}.".format(objet.get_nom(pose))
            personnage.salle.envoyer("{{}} dépose {}.".format(
                        objet.get_nom(pose)), personnage)
