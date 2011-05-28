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


"""Fichier contenant le type Indefini."""

from primaires.interpreteur.editeur.uniligne import Uniligne
from .base import BaseType

class Indefini(BaseType):
    
    """Type d'objet: indéfini.
    
    """
    
    nom_type = "indéfini"
    
    def __init__(self, cle=""):
        """Constructeur du type indéfini"""
        BaseType.__init__(self, cle)
        self.test = "un test"
        self.etendre_editeur("t", "test", Uniligne, self, "test")
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes.
        On récupère un dictionnaire représentant la présentation avec en
        clé les raccourcis et en valeur les enveloppes.
        
        Cela peut permettre de travailler sur les enveloppes ajoutées par
        'etendre_editeur'.
        
        """
        env = enveloppes["t"] # on récupère 'test'
        env.prompt = "Entrez une chaîne : "
        env.apercu = "{objet.test}"
        env.aide_courte = \
            "Entrez |tit|une chaîne|ff| ou |cmd|/|ff| pour revenir."
