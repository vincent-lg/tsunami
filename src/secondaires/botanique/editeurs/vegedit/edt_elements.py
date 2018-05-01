# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur EdtElements."""

from primaires.interpreteur.editeur import Editeur

class EdtElements(Editeur):
    
    """Contexte-éditeur d'édition des éléments de la période."""
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur."""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("d", self.opt_supprimer_element)
        self.ajouter_option("r", self.opt_renommer_element)
    
    def opt_supprimer_element(self, arguments):
        """Supprime un élément.
        
        Syntaxe : /d <nom de l'élément>
        
        """
        periode = self.objet
        nom = arguments
        if not nom:
            self.pere << "|err|Précisez le nom de l'élément à supprimer.|ff|"
            return
        
        try:
            periode.supprimer_element(nom)
        except ValueError:
            self.pere << "|err|Cet élément est introuvable.|ff|"
            return
        else:
            self.actualiser()
    
    def opt_renommer_element(self, arguments):
        """Renomme un élément.
        
        Syntaxe : /r <acien nom> / <nouveau nom>
        
        """
        periode = self.objet
        if not arguments:
            self.pere << "|err|Précisez <ancien nom> / <nouveau nom>|ff|"
            return
        
        try:
            ancien_nom, nouveau_nom = arguments.split(" / ")
        except ValueError:
            self.pere << "|err|Précisez <ancien nom> / <nouveau nom>|ff|"
            return
        
        try:
            elt = periode.get_element(ancien_nom)
        except ValueError:
            self.pere << "|err|Cet élément est introuvable.|ff|"
            return
        
        elt.nom = nouveau_nom.lower()
        self.actualiser()
    
    def accueil(self):
        """Message d'accueil du contexte."""
        periode = self.objet
        msg = "| |tit|" + "Edition des éléments de la période " \
                "{}".format(periode.nom).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Entrez le nom de l'élément (comme |ent|fruits|ff| " \
            "ou |ent|feuilles|ff|,\nau pluriel) suivi d'un espace, de " \
            "la clé de l'objet correspondant puis\nd'un autre espace et " \
            "de la quantité apparaissant par jour de la période. Si\nvous " \
            "précisez ici 5 pomme_rouge dans cette période, l'arbre " \
            "se\ncouvrira de plus ou moins 5 nouvelles pommes chaque jour." \
            "\n\nOptions :\n" \
            "  |ent|/r <ancien nom> / <nouveau nom>|ff| pour " \
            "renommer un élément\n" \
            "  |ent|/d <nom de l'élément|ff| pour supprimer un élément" \
            "\n\nExemples :\n  |ent|fruits pomme_rouge 5|ff|\n\n" \
            "Eléments définis :\n  "
        lignes = []
        for elt in sorted(periode.elements, key=lambda e: e.objet.cle):
            lignes.append("{:<20} {:<20} ({:>3})".format(
                    elt.nom, elt.objet.cle, elt.quantite))
        
        if not lignes:
            lignes.append("Aucun")
        
        msg += "\n  ".join(lignes)
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        periode = self.objet
        msg = msg.strip()
        if not msg:
            self.pere << "Entrez |ent|<type> <cle_objet> <quantité>|ff|."
            return
        
        try:
            type, cle, qtt = msg.split(" ")
        except ValueError:
            self.pere << "Entrez |ent|<type> <cle_objet> <quantité>|ff|."
            return
        
        try:
            qtt = int(qtt)
            assert qtt >= 0
        except (ValueError, AssertionError):
            self.pere << "|err|Quantité invalide.|ff|"
            return
        
        try:
            objet = importeur.objet.prototypes[cle]
        except KeyError:
            self.pere << "|err|Objet introuvable.|ff|"
            return
        
        try:
            periode.ajouter_element(type, objet, qtt)
        except ValueError as err:
            self.pere << "|err|" + str(err) + ".|ff|"
            return
        else:
            self.actualiser()
