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

class CmdPrendre(Commande):
    
    """Commande 'prendre'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "prendre", "get")
        self.schema = "(<nombre>) <nom_objet>"
        self.aide_courte = "ramasse un objet"
        self.aide_longue = \
                "Cette commande permet de ramasser un ou plusieurs objets."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre
        objets = dic_masques["nom_objet"].objets[:nombre]
        
        # On cherche les emplacements libres chez le personnage
        membres_libres = []
        for membre in personnage.equipement.membres:
            if membre.peut_tenir() and membre.tenu is None:
                membres_libres.append(membre)
        
        if not membres_libres:
            personnage << "Vous n'avez aucune main libre."
        else:
            pris = 0
            for objet, conteneur in objets:
                membre = membres_libres[0]
                membres_libres.pop(0)
                personnage.salle.objets_sol.retirer(objet)
                membre.tenu = objet
                pris += 1
                if not membres_libres:
                    break
            
            personnage << "Vous ramassez {}.".format(objet.get_nom(pris))
            personnage.salle.envoyer("{} ramasse {}.".format(personnage.nom,
                    objet.get_nom(pris)), (personnage, ))
