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
# POSSIBILITY OF SUCH DAMAGE.

"""Fichier contenant la classe Autoquete, détaillée plus bas."""

from datetime import datetime

from abstraits.obase import BaseObj

class AutoQuete(BaseObj):
    
    """Classe-mère de TOUS les types d'autoquêtes définis.
    
    Cette classe est au sommet de la hiérarchie d'héritage.
    Elle est la seule parmi les types d'autoquêtes à ne pas
    définir de parent.
    
    Attributs définis :
        tps_attente -- temps (en jours IRL) avant de pouvoir refaire la quête
    
    """
    
    nom_type = "base"
    parent = None
    concrete = False
    _no = 1
    def __init__(self, cle):
        """Cosntructeur de l'auto-quête."""
        self.id = Base._no
        Base._no += 1
        self.cle = cle
        self.tps_attente = 1
        self._memoire = {}
        self._a_detruire = {}
    
    def __getnewargs__(self):
        return ("inconnue", )
    
    def __repr__(self):
        return "<autoquête {} (type={}>".format(self.id, self.nom_type)
    
    def __str__(self):
        return "autoquête {}".format(self.id)
    
    def ecrire_memoire(self, personnage, nom, valeur=1):
        """Écrit dans la mémoire de l'auto-quête.
        
        Paramètres à entrer :
            personnage -- le personnage concerné
            nom -- le nom de la mémoire
            valeur -- la valeur de la mémoire (1 par défaut)
        
        Si aucune autre mémoire n'existe pour ce personnage, la mémoire est
        prise comme point de départ de la quête et sera effacée au bout
        de self.tps_attente jours.
        
        """
        memoire = self._memoire.get(personnage, {})
        memoire[nom] = valeur
        self._memoire[personnage] = memoire
        
        if personnage not in self._a_detruire:
            self._a_detruire[personnage] = datetime.now()
    
    def est_complete(self, personnage):
        """L'autoquête est-elle complute ?"""
        return False
