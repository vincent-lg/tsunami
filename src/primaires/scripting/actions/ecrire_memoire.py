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
# LIABLE FOR ANY teleporterCT, INteleporterCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action ecrire_memoire."""

from primaires.scripting.action import Action

class ClasseAction(Action):
    
    """Ecrit dans la mémoire du scripting.
        
    Une mémoire peut être spécifiée pour une salle, un personnage (joueur
    ou PNJ) ou un objet. La valeur de la mémoire peut être de n'importe quel
    type, sa clé doit être une chaîne.
    """
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ecrire_salle, "Salle", "str", "object")
        cls.ajouter_types(cls.ecrire_perso, "Personnage", "str", "object")
        cls.ajouter_types(cls.ecrire_objet, "Objet", "str", "object")
    
    @staticmethod
    def ecrire_salle(salle, cle, valeur):
        """Ecrit une mémoire de salle."""
        if salle in importeur.scripting.memoires:
            importeur.scripting.memoires[salle][cle] = valeur
        else:
            importeur.scripting.memoires[salle] = {cle: valeur}
    
    @staticmethod
    def ecrire_perso(personnage, cle, valeur):
        """Ecrit une mémoire de personnage (joueur ou PNJ)."""
        personnage = hasattr(personnage, "prototype") and \
                personnage.prototype or personnage
        if personnage in importeur.scripting.memoires:
            importeur.scripting.memoires[personnage][cle] = valeur
        else:
            importeur.scripting.memoires[personnage] = {cle: valeur}
    
    @staticmethod
    def ecrire_objet(objet, cle, valeur):
        """Ecrit une mémoire d'objet."""
        if objet in importeur.scripting.memoires:
            importeur.scripting.memoires[objet][cle] = valeur
        else:
            importeur.scripting.memoires[objet] = {cle: valeur}
