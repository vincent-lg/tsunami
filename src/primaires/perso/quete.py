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
    
    """Niveaux dans une quête d'un personnage.
    
    Cet objet est destiné à enregistrer les niveaux dans une quête d'un
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
    
    Ayez bien conscience que l'objet Quete stock plusieurs niveaux,
    pas un seul. En fait, tous les niveaux validés par le joueur sont
    enregistrés dans cet objet.
    
    """
    
    def __init__(self, cle_quete, niveau, parent=None):
        """Crée une nouvelle quête."""
        BaseObj.__init__(self)
        self.cle_quete = cle_quete
        self.parent = parent
        self.__verrou = False
        
        # Pour le niveau
        if isinstance(niveau, Quete):
            niveaux = niveau.niveaux
        elif isinstance(niveau, tuple):
            niveaux = [niveau]
        else:
            raise TypeError("le type {} ne peut servir pour caractériser " \
                    "un niveau de quête".format(type(niveau)))
        
        self.__niveaux = niveaux
        self._construire()
    
    def __getnewargs__(self):
        return ("", (0, ))
    
    @property
    def verrouille(self):
        """Retourne True si la quête est verrouillé."""
        return self.__verrou
    
    @property
    def niveaux(self):
        return list(self.__niveaux)
    
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
        if niveau not in self.__niveaux:
            self.__niveaux.append(niveau)
            if self.parent:
                self.parent.enregistrer()
    
    @property
    def niveau_suivant(self):
        """Récupère le niveau le plus avancé et y ajoute 1.
        
        Par exemple, si le niveau le plus élevé est 1.2, retourne 1.3.
        
        """
        if not len(self.__niveaux):
            return (1, )
        
        niveau = max(self.__niveaux)
        if niveau == (0, ):
            return (1, )
        
        niveau = ".".join([str(n) for n in niveau])
        # On récupère la template
        quete = type(self).importeur.scripting.quetes[self.cle_quete]
        niveaux = quete.get_dictionnaire_etapes(True)
        etapes = list(niveaux.keys())
        pos = etapes.index(niveau)
        if pos == len(niveaux) - 1:
            return ()
        
        print("Retourne", niveaux[etapes[pos + 1]])
        return niveaux[etapes[pos + 1]].niveau
    
    def peut_faire(self, quete, niveau):
        """Retourne True si la quête peut être faite, False sinon.
        
        La quête passée en paramètre est le template de la quête.
        Le niveau est le niveau demandé.
        
        """
        if niveau in self.__niveaux:
            return False
        
        if quete is None:
            return True
        
        if niveau == (0, ):
            return True
        
        if quete.ordonnee:
            return niveau == self.niveau_suivant
        else:
            # Le niveau parent doit être validé
            # Note : le niveau parent de (2, 3) et (1, )
            # Celui de (1, 5, 2) est (1, 4)
            t_niveau = niveau[:-2] + (niveau[-2] - 1, )
            
            # On retire les 0 en fin de niveau
            f_niveau = []
            non_zero = False
            for n in reversed(t_niveau):
                if n <= 0:
                    if non_zero:
                        f_niveau.insert(0, n)
                else:
                    f_niveau.insert(0, n)
                    non_zero = True
            
            return tuple(f_niveau) in self.__niveaux
    
    def valider(self, quete, niveau):
        """Valide la quête passée en paramètre.
        
        Le niveau représente l'étape validée dans la quête.
        
        Si la quête est une sous-quête et que toutes ses étapes
        sont validées, valide l'étape parent.
        
        """
        if niveau not in self.__niveaux:
            self.__niveaux.append(niveau)
        
        print(quete, quete.parent, quete.niveau)
        if quete.parent and all(e.niveau in self.__niveaux for e in \
                quete.get_dictionnaire_etapes(True).values()):
            print("Valide")
            self.__niveaux.append(quete.niveau)
        
        if self.parent:
            self.parent.enregistrer()
