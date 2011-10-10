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


"""Fichier contenant la classe Combat, détaillée plus bas."""

class Combat:
    
    """Classe représentant un combat dans une salle.
    
    Un combat est constitué :
        combattants -- D'une liste de combattants
        combattus -- d'un dictionnaire combattant: combattu
    
    A chaque tour (appelle à la méthode tour), les combattants combattent
    selon des règles définies dans ce module. Voir la méthode 'tour'
    pour plus d'informations.
    
    """
    
    def __init__(self, salle):
        """Constructeur d'un combat."""
        self.salle = salle
        self.__combattants = []
        self.__combattus = {}
    
    @property
    def combattants(self):
        """Retourne une liste déréférencée des combattants."""
        return list(self.__combattants)
    
    @property
    def combattus(self):
        """Retourne un dictionnaire déréférencé des combattus."""
        return dict(self.__combattus)
    
    def ajouter_combattants(self, combattant, combattu):
        """Ajoute les combattants."""
        self.__combattants.append(combattant)
        self.__combattants.append(combattu)
        self.__combattus[combattant] = combattu
        self.__combattus[combattu] = combattant
    
    def verifier_combattants(self):
        """VVérifie que tous les combattants sont bien dans la salle."""
        for combattant in self.combattants:
            if combattant.salle != self.salle:
                self.__combattants.remove(combattant)
        
        for combattant, combattu in self.combattus.items():
            if combattant.salle != self.salle:
                del self.__combattus[combattant]
            elif combattu.salle != self.salle:
                self.__combattus[combattant] = None
        
        # Les combattants ne combattant personne essayent de trouver une
        # autre cible
        for combattant, combattus in self.combattus.items():
            if combattu is None:
                # On liste les cibles possibles du combattant
                # (ceux qui le combattent)
                cibles = [cbt for cbt, cbu in self.combattus.items() if \
                        cbu == combattant]
                if cibles:
                    cible = choice(cibles)
                    self.__combattus[combattant] = cible
    
    def tour(self, importeur):
        """Un tour de combat."""
        self.verifier_combattants()
        for combattant, combattu in self.combattus.items():
            print(combattant, "attaque", combattu)
        
        importeur.diffact.ajouter_action(
            "combat:{}".format(self.salle.ident), 3, self.tour, importeur)
