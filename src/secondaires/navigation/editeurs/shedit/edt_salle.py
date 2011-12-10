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


"""Fichier contenant la classe EdtSalle, détaillée plus bas.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.flag import Flag
from secondaires.navigation.salle import NOMS_SORTIES

class EdtSalle(Presentation):
    
    """Classe définissant l'éditeur de salle de navire."""
    
    def __init__(self, personnage, salle, attribut=""):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, salle, "", False)
        self.ajouter_option("bab", self.opt_ajouter_babord)
        self.ajouter_option("tri", self.opt_ajouter_tribord)
        self.ajouter_option("ava", self.opt_ajouter_avant)
        self.ajouter_option("arr", self.opt_ajouter_arriere)
        self.ajouter_option("hau", self.opt_ajouter_haut)
        self.ajouter_option("bas", self.opt_ajouter_bas)
        self.ajouter_option("elt", self.opt_ajouter_supprimer_element)
        if personnage and salle:
            self.construire(salle)
    
    def __getnewargs__(self):
        return (None, None)
    
    def opt_ajouter_babord(self, arguments):
        """Ajoute une salle à bâbord.
        
        Syntaxe :
            /bab <mnémonic>
        
        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "ouest")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()
    
    def opt_ajouter_tribord(self, arguments):
        """Ajoute une salle à tribord.
        
        Syntaxe :
            /tri <mnémonic>
        
        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "est")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()
    
    def opt_ajouter_avant(self, arguments):
        """Ajoute une salle à l'avant.
        
        Syntaxe :
            /ava <mnémonic>
        
        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "nord")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()
    
    def opt_ajouter_arriere(self, arguments):
        """Ajoute une salle à l'arrière.
        
        Syntaxe :
            /arr <mnémonic>
        
        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "sud")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()
    
    def opt_ajouter_bas(self, arguments):
        """Ajoute une salle vers le bas.
        
        Syntaxe :
            /bas <mnémonic>
        
        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "bas")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()
    
    def opt_ajouter_haut(self, arguments):
        """Ajoute une salle vers le haut.
        
        Syntaxe :
            /hau <mnémonic>
        
        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "haut")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()
    
    def construire(self, salle):
        """Construction de l'éditeur"""
        # Titre
        titre = self.ajouter_choix("titre", "t", Uniligne, salle, "titre")
        titre.parent = self
        titre.prompt = "Titre de la salle : "
        titre.apercu = "{objet.titre}"
        titre.aide_courte = \
            "Entrez le |ent|titre|ff| de la salle ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nTitre actuel : |bc|{objet.titre}|ff|"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, \
                salle)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description de la salle {}".format(salle).ljust(76) + \
            "|ff||\n" + self.opts.separateur
        
        # Intérieur / extérieur
        inter = self.ajouter_choix("intérieur", "i", Flag, salle, "interieur")
        inter.parent = self
    
    def opt_ajouter_supprimer_element(self, arguments):
        """Ajoute ou supprime un élément.
        
        Syntaxe :
            /elt <clé_élément>
        
        """
        salle = self.objet
        cle = arguments.strip()
        cles = tuple(e.cle for e in salle.elements)
        types = tuple(e.nom_type for e in salle.elements)
        if cle in cles:
            salle.retirer_element(cle)
            self.actualiser()
        else:
            if cle not in type(self).importeur.navigation.elements:
                self.pere << "|err|Cet élément est introuvable.|ff|"
                return
            
            elt = type(self).importeur.navigation.elements[cle]
            if elt.nom_type in types:
                self.pere << "|err|Un élément de ce type est déjà présent " \
                        "dans cette salle.|ff|"
                return
            
            salle.ajouter_element(elt)
            self.actualiser()
    
    def accueil(self):
        """Message d'accueil de l'éditeur."""
        salle = self.objet
        msg = Presentation.accueil(self)
        msg += "\n"
        # Sorties
        msg += " Sorties :"
        for dir, nom in NOMS_SORTIES.items():
            sortie = salle.sorties[dir]
            if sortie:
                msg += "\n   {} vers {}".format(sortie.nom.capitalize(),
                        sortie.salle_dest.mnemonic)
            else:
                msg += "\n   {}".format(nom.capitalize())
        
        msg += "\n"
        # Éléments
        msg += "\n Éléments de navire : " + ", ".join(
                e.cle for e in salle.elements)
        if not salle.elements:
            msg += "aucun"
        
        return msg
