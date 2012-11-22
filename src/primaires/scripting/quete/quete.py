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


"""Fichier contenant la classe Quete détailéle plus bas."""

import re
from datetime import datetime
from collections import OrderedDict

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.format.fonctions import oui_ou_non
from .etape import Etape

# Constantes
RE_QUETE_VALIDE = re.compile(r"^[a-z][a-z0-9_]*$")

class Quete(BaseObj):
    
    """Classe définissant une quête dans le scripting.
    
    Une quête est constituée d'une suite d'étapes.
    
    Chaque étape peut être :
        une étape simple de scripting (Etape)
        une autre quête (Quete)
        un embranchement (Embranchement)
    
    L'étape simple est une étape menant à une suite d'instructions.
    Une sous-quête possède les mêmes propriétés que celles définies ici.
    Un embranchement permet de matérialiser un choix dans la quête.
    
    """
    
    enregistrer = True
    def __init__(self, cle, auteur, parent=None, niveau=(1, )):
        """Constructeur de la quête."""
        BaseObj.__init__(self)
        self.type = "quete"
        self.cle = cle
        self.niveau = niveau
        self.auteur = auteur
        self.parent = parent
        self.date_creation = datetime.now()
        self.titre = "une quelconque quête"
        self.description = Description(parent=self)
        self.ordonnee = True
        self.__etapes = []
        self._construire()
    
    def __getnewargs__(self):
        return ("", None)
    
    def __repr__(self):
        return "<quête {}>".format(repr(self.titre))
    
    def __str__(self):
        ret = self.cle + ", " + \
                (self.auteur and "par " + self.auteur.nom or "auteur inconnu")
        
        # Statistiques
        nb_joueurs = importeur.scripting.cb_joueurs()
        nb_quete = importeur.scripting.cb_joueurs_quete(self.cle)
        pc = 0
        if nb_joueurs > 0:
            pc = int(nb_quete / nb_joueurs * 100)
        ret += " - {} / {} ({}%)".format(nb_quete, nb_joueurs, pc)
        return ret
    
    def __getitem__(self, niveau):
        """Retourne l'étape."""
        for etape in self.__etapes:
            if etape.str_niveau == niveau:
                return etape
        
        raise KeyError(niveau)
    
    @property
    def etapes(self):
        """Constitue un dictionnaire des niveaux."""
        return self.get_dictionnaire_etapes()
    
    @property
    def str_niveau(self):
        return ".".join([str(n) for n in self.niveau])
    
    @property
    def sous_niveau(self):
        if self.parent:
            return self.niveau + (len(self.__etapes) + 1, )
        else:
            return (len(self.__etapes) + 1, )
    
    @property
    def aff_ordonnee(self):
        return oui_ou_non(self.ordonnee)
    
    def get_dictionnaire_etapes(self, etapes_seulement=False):
        """Retourne un dictionnaire ordonné des étapes."""
        niveaux = OrderedDict()
        if not etapes_seulement:
            niveaux[self.str_niveau] = self
        
        for etape in self.__etapes:
            if etape.type == "quete":
                niveaux.update(etape.get_dictionnaire_etapes(etapes_seulement))
            else:
                niveaux[etape.str_niveau] = etape
        
        return niveaux
    
    def ajouter_etape(self, titre):
        """Ajoute l'étape à la quête."""
        etape = Etape(self)
        etape.titre = titre
        etape.niveau = self.sous_niveau
        self.__etapes.append(etape)
    
    def ajouter_sous_quete(self, titre):
        """Ajoute une sous-quête à la quête."""
        etape = Quete(self.cle, self.auteur, self)
        etape.titre = titre
        etape.niveau = self.sous_niveau
        self.__etapes.append(etape)
    
    def supprimer_etape(self, num):
        indice = len(self.niveau) - 1
        a_effacer = None
        for (strniveau,etape) in self.get_dictionnaire_etapes().items():
            niveau = list(etape.niveau)
            if niveau[indice] > num:
                niveau[indice] -= 1
                etape.niveau = tuple(niveau)
            elif etape.niveau[indice] != num:
                a_effacer = strniveau
        del self.get_dictionnaire_etapes()[a_effacer]
    
    def afficher_etapes(self, quete=None):
        """Affiche les étapes qui peuvent être aussi des sous-quêtes."""
        res = ""
        if self.parent and quete is not self:
            res += " " + "  " * len(self.niveau) + "|bc|" + \
                    self.str_niveau
            res += "|ff| - " + self.titre
            
            # Statistiques
            nb_quete = importeur.scripting.cb_joueurs_quete(self.cle)
            nb_etape = importeur.scripting.cb_joueurs_etape(self.cle,
                    self.niveau)
            pc = 0
            if nb_quete > 0:
                pc = int(nb_etape / nb_quete * 100)
            res += " - {} / {} ({}%)\n".format(
                    nb_etape, nb_quete, pc)
        
        for etape in self.__etapes:
            res += etape.afficher_etapes(quete)
            res += "\n"
        
        return res.rstrip("\n")
    
    def supprimer_etape(self, niveau):
        """Supprime l'étape."""
        numero = None
        for i, etape in enumerate(self.__etapes):
            if etape.str_niveau == niveau:
                numero = i
                break
        
        etape = self.__etapes[numero]
        niveau = etape.niveau
        etape.detruire()
        del self.__etapes[numero]
        for etape in self.__etapes[numero:]:
            t_niveau = etape.niveau
            etape.mettre_a_jour_niveau(niveau)
            niveau = t_niveau
    
    def mettre_a_jour_niveau(self, niveau):
        """Méthode mettant à jour le niveau de la quête."""
        self.niveau = niveau
        
        # On calcul le niveau des sous-étapes
        for etape in self.__etapes:
            t_niveau = niveau + (etape.niveau[-1], )
            etape.mettre_a_jour_niveau(t_niveau)
    
    def detruire(self):
        """Destruction de l'objet."""
        for etape in self.__etapes:
            etape.detruire()
        
        BaseObj.detruire(self)
