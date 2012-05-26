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


"""Package contenant l'éditeur 'vegedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

"""

from primaires.interpreteur.editeur.presentation import Presentation
from .edt_cycles import EdtCycles
from .supprimer import NSupprimer

class EdtVegedit(Presentation):
    
    """Classe définissant l'éditeur de prototype de végétal 'vegedit'.
    
    """
    
    nom = "vegedit"
    
    def __init__(self, personnage, prototype):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, prototype)
        if personnage and prototype:
            self.construire(prototype)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, prototype):
        """Construction de l'éditeur"""
        # Cycles
        cycles = self.ajouter_choix("cycles", "c", EdtCycles,
                prototype)
        cycles.parent = self
        cycles.aide_courte = \
            "Entrez |ent|le nom|ff| d'un cycle pour l'éditer ou " \
            "|ent|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Options :\n" \
            "  |ent|/n <nouveau nom>|ff| : ajoute un cycle\n" \
            "  |ent|/d <nom>|ff| : supprime un cycle"
        
        # Supprimer
        sup = self.ajouter_choix("supprimer", "sup", NSupprimer,
                prototype)
        sup.parent = self
        sup.aide_courte = "Souhaitez-vous réellement supprimer " \
                "le prototype {} et ses plantes ?".format(prototype.cle)
