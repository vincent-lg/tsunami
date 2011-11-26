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


"""Fichier contenant l'éditeur EdtCarte."""

from primaires.interpreteur.editeur import Editeur

class EdtCarte(Editeur):
    
    """Classe définissant l'éditeur edt_carte."""
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.niveau = 0
        self.ajouter_option("m", self.opt_ajouter_milieu)
        self.ajouter_option("d", self.opt_supprimer_salle)
    
    def opt_ajouter_milieu(self, arguments):
        """Ajoute d'une salle au milieu du navire."""
        modele = self.objet
        if "0.0.0" in modele.salles:
            self.pere << "|err|Une salle au milieu du navire est déjà " \
                    "définie.|ff|"
        else:
            modele.ajouter_salle(0, 0, 0, "1")
            self.actualiser()
    
    def opt_supprimer_salle(self, arguments):
        """Supprime une salle.
        
        Syntaxe :
            /d mnémonic
        
        """
        if modele.get_salle(arguments) is None:
            self.pere << "|err|Le mnémonic {} est introuvable.|ff|".format(
                    arguments)
        else:
            modele.supprimer_salle(arguments)
            self.actualiser()
    
    def accueil(self):
        """Affichage de la carte du navire."""
        modele = self.objet
        coordonnees = modele.coordonnees_salles
        msg = " |tit| Carte du modèle de navire {}|ff|\n\n".format(modele.cle)
        if coordonnees:
            # On cherche la coordonnée d'extrême ouest / est
            ouest_est = [c[0] for c in coordonnees]
            sud_nord = [c[1] for c in coordonnees]
            bas_haut = [c[2] for c in coordonnees]
            ouest = min(ouest_est)
            est = max(ouest_est)
            sud = min(sud_nord)
            nord = max(sud_nord)
            bas = min(bas_haut)
            haut = max(bas_haut)
            niveau = self.niveau
            for i in range(ouest, est + 1):
                for j in range(sud, nord - 1, -1):
                    t_coords = (i, j, niveau)
                    salle = modele.salles.get(t_coords)
                    if salle:
                        msg += salle.mnemonic.rjust(3)
                    else:
                        msg += "   "
                msg += "\n"
            msg = msg[:-1]
        else:
            msg += "|att|Aucune salle n'est définie pour l'instant.|ff|"
        
        return msg
