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

"""Ce fichier contient la classe Quete, détaillée plus bas."""

from abstraits.obase import *

class Quete(BaseObj):
    
    """Niveau dans une quête d'un personnage.
    
    Cet objet est destiné à enregistrer le niveau dans une quête d'un
    personnage.
    
    Le niveau est sous la forme d'un tuple de N éléments.
    Le premier élément représente le niveau dans la quête.
    Le second, si présent, représente le niveau dans la sous-quête.
    Ainsi de suite.
    
    Il est plus facile de se représenter ce tuple sous la forme d'une
    chaîne de caractères séparant chaque niveau par un point.
    Par exemple, "1.2" signifie le niveau 1 dans la quête et le niveau 2 dans
    la sous-quête 1. Il est facile de voir que :
        "1" < "1.2"
        "1.3" > "1.2"
        ...
    
    Pour se construire, la classe Quete prend :
        la clé de la quête (un identifiant)
        la valeur (plusieurs types sont admis, voir plus bas)
        le parent (optionnel)
    
    Le niveau de la quête peut être soit :
        un objet de type Quete copié
        un tuple
    
    Quant au parent, il ne sert qu'à symboliser le personnage qui possède
    la quête. Si l'objet est déréférencé, ce parent peut être None.
    
    """
    
    def __init__(self, cle_quete, niveau, parent=None):
        """Crée une nouvelle quête."""
        BaseObj.__init__(self)
        self.cle_quete = cle_quete
        self.parent = parent
        self.__verrou = False
        
        # Pour le niveau
        if isinstance(niveau, Quete):
            niveau = niveau.niveau
        elif isinstance(niveau, tuple):
            pass
        else:
            raise TypeError("le type {} ne peut servir pour caractériser " \
                    "un niveau de quête".format(type(niveau)))
        
        self.niveau = niveau
        self._construire()
    
    def __getnewargs__(self):
        return ("", (0, ))
    
    def __repr__(self):
        return tuple(self.niveau)
    
    def __str__(self):
        return ".".join([str(n) for n in self.niveau])
    
    # Méthodes de comparaison
    def __lt__(self, niveau):
        o_niveau = self.convertir_niveau(niveau)
        niveau, o_niveau = self.egaliser_niveaux(self.niveau, o_niveau)
        for n, m in zip(niveau, o_niveau):
            if n < m:
                return True
            elif n > m:
                break
        
        return False
    
    def __le__(self, niveau):
        o_niveau = self.convertir_niveau(niveau)
        niveau, o_niveau = self.egaliser_niveaux(self.niveau, o_niveau)
        for n, m in zip(niveau, o_niveau):
            if n > m:
                return False
        
        return True
    
    def __eq__(self, niveau):
        o_niveau = self.convertir_niveau(niveau)
        niveau, o_niveau = self.egaliser_niveaux(self.niveau, o_niveau)
        for n, m in zip(niveau, o_niveau):
            if n != m:
                return False
        
        return True
    
    def __ne__(self, niveau):
        o_niveau = self.convertir_niveau(niveau)
        niveau, o_niveau = self.egaliser_niveaux(self.niveau, o_niveau)
        for n, m in zip(niveau, o_niveau):
            if n == m:
                return False
        
        return True
    
    def __ge__(self, niveau):
        o_niveau = self.convertir_niveau(niveau)
        niveau, o_niveau = self.egaliser_niveaux(self.niveau, o_niveau)
        for n, m in zip(niveau, o_niveau):
            if n < m:
                return False
        
        return True
    
    def __gt__(self, niveau):
        o_niveau = self.convertir_niveau(niveau)
        niveau, o_niveau = self.egaliser_niveaux(self.niveau, o_niveau)
        for n, m in zip(niveau, o_niveau):
            if n > m:
                return True
            elif n < m:
                break
        
        return False
    
    def __add__(self, entier):
        """Ajoute un entier au niveau de la quête."""
        n_v = list(self.niveau)
        n_v[-1] += entier
        return Quete(self.cle_quete, tuple(n_v))
    
    @staticmethod
    def convertir_niveau(niveau):
        """Retourne le niveau convertit en tuple.
        
        Le niveau peut être :
            un objet Quête
            un tuple (on n'y touche pas)
            une chaîne de caractères
        
        """
        if isinstance(niveau, tuple):
            pass
        elif isinstance(niveau, Quete):
            niveau = niveau.niveau
        elif isinstance(niveau, int):
            niveau = tuple(nigveau)
        elif isinstance(niveau, str):
            try:
                niveau = tuple(int(v) for v in niveau.split("."))
            except ValueError:
                raise ValueError("impossible de convertir {} en niveau " \
                        "de quête".format(niveau))
        
        return niveau
    
    @staticmethod
    def egaliser_niveaux(n1, n2):
        """Egalise les tuple n1 et n2.
        
        Si n1 est plus long que n2, allonge n2 avec des 0.
        Même principe dans l'autre sens.
        Au final, n1 et n2 (retournés) doivent avoir la même taille.
        
        """
        if len(n1) > len(n2):
            n2 = n2 + (0, ) * (len(n1) - len(n2))
        elif len(n2) > len(n1):
            n1 = n1 + (0, ) * (len(n2) - len(n1))
        
        return n1, n2
    
    @property
    def verrouille(self):
        """Retourne True si la quête est verrouillé."""
        return self.__verrou
    
    def verrouiller(self):
        """Verrouille la quête."""
        self.__verrou = True
        if self.parent:
            self.parent.enregistrer()
    
    def deverouiller(self):
        """Déverouille la quête."""
        self.__verrou = False
        if self.parent:
            self.parent.enregistrer()
    
    def mettre_a_jour(self, niveau):
        """Met à jour le niveau de la quête.
        
        Le niveau doit être un tuple.
        
        """
        self.niveau = niveau
