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


"""Fichier contenant la classe ParserMasque détaillée plus bas."""

from primaires.interpreteur.masque.noeud import NoeudMasque

class ParserMasque:
    
    """Parser de masque.
    Il se charge, grâce à une chaîne de caractère, de construire une
    arborescence de masques. Cette arborescence pourra être étendue par la
    suite. Cela permettra de modifier le comportement d'une commande
    existante en y ajoutant, par exemple, de nouveaux paramètres.
    
    Cette arborescence de masques servira de base à l'analyse de la commande.
    
    """
    
    def __init__(self, schema="", racine=NoeudMasque()):
        """Constructeur du parser.
        Il peut prendre en paramètre :
        schema -- le schéma sous la forme d'une chaîne 'str'
        racine -- la racine de l'arborescence, un noeud vide par défaut
        
        """
        self.racine = racine
        self.parser(self.racine, schema)
    
    def parser(self, noeud_courant, schema):
        """Parse le schéma passé en paramètre.
        Cette fonction est appelée récursivement. Elle doit partir de la
        racine avec le schéma complet et au fur et à mesure que le schéma est
        décodé, on ajoute de nouveaux fils à la racine, puis de nouveaux fils
        à ces nouveaux fils, ainsi de suite jusqu'à obtenir l'arborescence
        complète.
        
        """
        
    def extraire_partie(self, schema):
        """On 