# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Package contenant la commande 'asseoir'."""

from primaires.interpreteur.commande.commande import Commande

class CmdAsseoir(Commande):
    
    """Commande 'asseoir'"""
    
    def __init__(self):
        """Constructeur de la commande."""
        Commande.__init__(self, "asseoir", "sit")
        self.schema = "(<element_observable>)"
        self.nom_categorie = "bouger"
        self.aide_courte = "permet de s'asseoir"
        self.aide_longue = \
            "Cette commande permet de s'asseoir. Sans paramètre, " \
            "vous vous assierez sur le sol. Vous pouvez également " \
            "préciser un nom d'élément observable dans la salle " \
            "(un détail de la description qui le supporte). " \
            "Le facteur de récupération de vos différentes statistiques " \
            "sera différent en fonction de l'élément choisi."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        masque = dic_masques["element_observable"]
        personnage.agir("asseoir")
        if masque:
            elt = masque.element
            if not hasattr(elt, "peut_asseoir") or not elt.peut_asseoir:
                personnage << "|err|Vous ne pouvez vous asseoir ici.|ff|"
                return
            
            nb = len([p for p in personnage.salle.personnages if \
                    p.occupe is elt])
            if nb >= elt.nb_places_assises:
                personnage << "|err|Toutes les places sont prises ici.|ff|"
                return
            
            personnage.cle_etat = "assis"
            personnage.position = "assis"
            personnage.occupe = elt
            personnage << "Vous vous asseyez {} {}.".format(
                    elt.connecteur, elt.titre)
            personnage.salle.envoyer("{{}} s'asseoit {} {}.".format(
                    elt.connecteur, elt.titre), personnage)
        else:
            personnage.cle_etat = "assis"
            personnage.position = "assis"
            personnage.occupe = None
            personnage << "Vous vous asseyez sur le sol."
            personnage.salle.envoyer("{} s'asseoit sur le sol.", personnage)

