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


"""Fichier contenant la classe Salle, détaillée plus bas."""

from abstraits.id import ObjetID
from .coordonnees import Coordonnees
from .sorties import Sorties

class Salle(ObjetID):
    
    """Classe représentant une salle de l'univers.
    Une salle est un élément détaillant la géographie locale d'une petite
    portion de l'univers. Bien que cela dépende des MUDs, les salles décrivent
    généralement un espace d'environ 5 M sur 5 M.
    
    Ces salles comportent une description détaillant les alentours proches.
    Cette description est envoyée à chaque fois qu'un personnage se déplace
    dans l'univers, pour lui donner une idée de son nouvel environnement.
    
    Note sur le positionnement des salles :
        Les salles peuvent être caractérisées par des coordonnées. Ces
        coordonnées sont en soit facultatives. Il est possible de créer un
        univers sans aucune coordonnées. Les coordonnées sont une facilité
        lors de la constitution de votre univers et permettent à certains
        modules, comme 'vehicule', de fonctionner. Si votre salle n'a pas de
        coordonnées, vous devrez créer chaque sortie "à la main".
        Les salles ne sont donc pas identifiées par leurs coordonnées, sauf
        dans certains cas, mais bien par leur zone et mnémonic. Ce couple
        caractérise de façon unique une salle dans l'univers.
        Exemple : une ssalle ayant pour zone 'picte' et pour mnémonic '1'
        sera accessible depuis la clé 'picte:1'. Aucune autre salle de
        l'univers ne pourra posséder cette clé 'picte:1'.
    
    """
    
    groupe = "salles"
    sous_rep = "salles"
    
    def __init__(self, zone, mnemonic, x=0, y=0, z=0, valide=True):
        """Constructeur de la salle"""
        ObjetID.__init__(self)
        self._zone = zone
        self._mnemonic = mnemonic
        self.coords = Coordonnees(x, y, z, valide, self)
        self.titre = ""
        self.description = ""
        self.sorties = Sorties()
    
    def __getinitargs__(self):
        return ("", "")
    
    def _get_zone(self):
        return self._zone
    def _set_zone(self, zone):
        ident = self.ident
        self._zone = zone
        type(self).importeur.salle.changer_ident(ident, self.ident)
    
    def _get_mnemonic(self):
        return self._mnemonic
    def _set_mnemonic(self, mnemonic):
        ident = self.ident
        self._mnemonic = mnemonic
        type(self).importeur.salle.changer_ident(ident, self.ident)
    
    zone = property(_get_zone, _set_zone)
    mnemonic = property(_get_mnemonic, _set_mnemonic)
    
    @property
    def ident(self):
        """Retourne l'identifiant, c'est-à-dire une chaîne 'zone:mnemonic'"""
        return "{}:{}".format(self._zone, self._mnemonic)
    
    def __repr__(self):
        """Affichage de la salle en mode debug"""
        res = "Salle ({}, {})".format(self.ident, self.coords)
        # sorties
        for nom, sortie in self.sorties.iter_couple():
            if sortie:
                res += "\n  {}: {}".format(nom, sortie.salle_dest.ident)
        
        return res
    
    def regarder(self, personnage):
        """Le personnage regarde la salle"""
        res = ""
        res += "|jn|" + self.titre + "|ff|\n"
        res += self.description + "\n"
        res += "Sorties : "
        res += self.afficher_sorties(personnage)
        return res
    
    def afficher_sorties(self, personnage):
        """Affiche les sorties de la salle"""
        res = ""
        for nom, sortie in self.sorties.iter_couple():
            nom_aff = self.sorties.get_nom_abrege(nom)
            if self.sorties.sortie_existe(nom):
                res += nom_aff
            else:
                res += " ".ljust(len(nom_aff))
            res += ", "
        res = res[:-2] + "."
        return res

# On ajoute le groupe à ObjetID
ObjetID.ajouter_groupe(Salle)
