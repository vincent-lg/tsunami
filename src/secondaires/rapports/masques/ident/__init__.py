# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Fichier contenant le masque <ident_rapport>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class Ident(Masque):
    
    """Masque <ident_rapport>.
    On attend un identifiant de rapport.
    CLASSE ABSTRAITE
    """
    
    nom = "ident_rapport"
    
    def __init__(self):
        """Constructeur du masque"""
        Masque.__init__(self)
        self.identifiant = -1
        self.objet = None
    
    def valider(self, personnage, dic_masques, commande):
        """Validation du masque"""
        
        lstrip(commande)
        ident = liste_vers_chaine(commande)
        
        if not ident:
            raise ErreurValidation( \
                "Précisez un identifiant de rapport.")
        
        ident = ident.split(" ")[0]
        commande[:] = commande[len(ident):]
        ident=int(ident)
        
        try:
            objet = type(self).importeur.rapports[self.typeRapport][ident]
        except KeyError:
            raise ErreurValidation(
                "|err|L'identifiant '{}' n'est pas valide.|ff|".format(ident))
        
        self.objet = objet
        self.ident = objet.ident
        
        return True

class IdentBug(Ident):
    
    """Masque <ident_bug>.
    On attend un identifiant de rapport de bug.
    
    """
    
    nom = "ident_bug"
    
    def __init__(self):
        """Constructeur du masque"""
        self.typeRapport = "bug"
        self.nom_complet = "identifiant de bugs"
        Ident.__init__(self)

class IdentSuggestion(Ident):
    
    """Masque <ident_suggestion>.
    On attend un identifiant de suggestion.
    
    """
    
    nom = "ident_suggestion"
    
    def __init__(self):
        """Constructeur du masque"""
        self.typeRapport = "suggestion"
        self.nom_complet = "identifiant de suggestion"
        Ident.__init__(self)

