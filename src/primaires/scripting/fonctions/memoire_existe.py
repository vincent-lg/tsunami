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


"""Fichier contenant la fonction memoire_existe."""

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):
    
    """Teste si une mémoire de scripting est écrite."""
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.memoire_salle_existe, "Salle", "str")
        cls.ajouter_types(cls.memoire_perso_existe, "Personnage", "str")
        cls.ajouter_types(cls.memoire_objet_existe, "Objet", "str")
    
    @staticmethod
    def memoire_salle_existe(salle, cle):
        """Renvoie vrai si la mémoire de salle existe, faux sinon."""
        if salle in importeur.scripting.memoires:
            return cle in importeur.scripting.memoires[salle]
        else:
            return False
    
    @staticmethod
    def memoire_perso_existe(personnage, cle):
        """Renvoie vrai si la mémoire de personnage existe, faux sinon."""
        if personnage in importeur.scripting.memoires:
            return cle in importeur.scripting.memoires[personnage]
        else:
            return False
    
    @staticmethod
    def memoire_objet_existe(objet, cle):
        """Renvoie vrai si la mémoire d'objet existe, faux sinon."""
        if objet in importeur.scripting.memoires:
            return cle in importeur.scripting.memoires[objet]
        else:
            return False
