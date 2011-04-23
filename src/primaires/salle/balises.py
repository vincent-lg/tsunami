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


"""Ce fichier contient la classe Balises, détaillée plus bas."""

from abstraits.obase import *
from .balise import Balise

class Balises(BaseObj):

    """Cette classe est une classe-enveloppe de Balise. Elle contient toutes
    les balises observables d'une salle, que l'on peut voir avec la commande
    look.
    
    Voir : ./balise.py
    
    """
    
    def __init__(self, parent=None):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.parent = parent
        self._balises = {}
        # On passe le statut en CONSTRUIT
        self._statut = CONSTRUIT
    
    def __getinitargs__(self):
        return ()
    
    def __getitem__(self, nom):
        """Retourne la balise 'nom'"""
        return self._balises[nom]
    
    def __setitem__(self, nom, balise):
        """Modifie la balise 'nom'"""
        self._balises[nom] = balise
        
        if self.construit and self.parent:
            self.parent.enregistrer()
    
    def __delitem__(self, nom):
        """Détruit la balise passée en paramètre"""
        del self._balises[nom]
    
    def iter(self):
        """Retourne un dictionnaire contenant les balises"""
        balises = {}
        for b_nom in self._balises.keys():
            balise = self[b_nom]
            balises[balise.nom] = balise
        
        return balises.items()
    
    def ajouter_balise(self, nom, *args, **kwargs):
        """Ajoute une balise à la liste.
        Les arguments spécifiés sont transmis au constructeur de Balise. Le nom
        correspondra au self.nom de la balise. Si une balise sous ce nom-là
        existe déjà, elle sera écrasée.
        
        """
        balise = Balise(nom, *args, parent=self.parent, **kwargs)
        self[nom] = balise
        
        return balise
    
    def get_balise(self, nom):
        """Renvoie la balise 'nom', si elle existe.
        A la différence de __getitem__(), cette fonction accepte en paramètre
        un des synonymes de la balise recherchée.
        
        """
        res = None
        for b_nom, balise in self._balises.items():
            if nom == b_nom or nom in balise.synonymes:
                res = balise
        return res
    
    def balise_existe(self, nom):
        """Renvoie True si la balise 'nom' existe"""
        try:
            return self.get_balise(nom) is not None
        except ValueError:
            return False
