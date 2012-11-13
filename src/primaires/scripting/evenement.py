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


"""Fichier contenant la classe Evenement détaillée plus bas."""

from abstraits.obase import *
from primaires.format.fonctions import supprimer_accents
from .espaces import Espaces
from .test import Test
from .variable import Variable

class Evenement(BaseObj):
    
    """Classe contenant un évènement de scripting.
    
    Un évènement est appelé dans une certaine situation. Un cas classique,
    par exemple, est un script défini dans un PNJ. Un évènement pourrait
    être appelé quand le PNJ est attaqué.
    
    Les évènements peuvent contenir des sous-évènements.
    
    Au niveau de la structure, un évènement contient :
    -   un dictionnaire de variables qui doivent IMPERATIVEMENT être
        TOUTES RENSEIGNEES quand on l'appelle ;
    -   un dictionnaire pouvant contenir des sous-évènements ;
    -   une suite de tests ;
    -   plusieurs espaces de nom.
    
    En outre, l'évènement garde en mémoire le script dont il est issu,
    qu'il soit sous-évènement ou non.
    
    Un évènement est constitué de plusieurs conditions (ou tests). Ces
    conditions sont propres aux variables qui les définissent. Un exemple
    simple :
        Evènement donner du PNJ tavernier_picte
            1   objet = pot_biere et nombre > 1
    La condition ci-dessus est appelée si le joueur donne plus d'un pot de
    bière au tavernier. Cela permet de ranger plus facilement nos lignes
    de script en fonction de plusieurs variables.
    
    Les évènements n'ayant aucune variable définie n'ont pas cette
    distinction en conditions pour le bâtisseur. Du point de vue du code,
    ils ont une seule condition appelée automatiquement.
    
    Les espaces de nom sont présents dans l'attribut 'espaces'. Chaque
    attribut de cet objet 'Espaces' est un espace de nom différent.
    Chaque espace se manipule comme un dictionnaire.
    
    Le constructeur d'un évènement prend en paramètre :
        script -- le script qui possède l'évènement
        nom -- le nom de l'évènement
        parent -- si c'est un sous-évènement, l'évènement parent (optionnel)
    
    """
    
    def __init__(self, script, nom, parent=None):
        """Constructeur d'un évènement"""
        BaseObj.__init__(self)
        self.script = script
        self.nom = nom
        self.aide_courte = "non précisée"
        self.aide_longue = "non précisée"
        self.parent = parent
        self.variables = {}
        self.__evenements = {}
        self.__tests = []
        self.__sinon = None
        self.espaces = Espaces(self)
        self._construire()
    
    @property
    def nom_complet(self):
        """Retourne le nom complet de l'événement."""
        ret = self.nom
        parent = self.parent
        while parent is not None:
            ret = parent.nom + "." + ret
            parent = parent.parent
        return ret
        
    def __getnewargs__(self):
        return (None, "")
    
    def __getstate__(self):
        """Ne sauvegarde pas les variables en fichier."""
        dico_attr = self.__dict__.copy()
        del dico_attr["espaces"]
        return dico_attr
    
    def __getitem__(self, evenement):
        """Retourne l'évènement correspondant au nom passé en paramètre."""
        evenement = supprimer_accents(evenement).lower()
        return self.__evenements[evenement]
    
    @property
    def appelant(self):
        """Retourne l'appelant, c'est-à-dire le parent du script."""
        return self.script.parent
    
    @property
    def tests(self):
        """Retourne une liste déréférencée des tests."""
        return list(self.__tests)
    
    @property
    def sinon(self):
        """Retourne le test sinon."""
        return self.__sinon
    
    @property
    def evenements(self):
        """Retourne un dictionnaire déréférencé des évènements."""
        return self.__evenements.copy()
    
    def creer_sinon(self):
        """Création du test sinon si il n'existe pas."""
        if self.__sinon is None:
            self.__sinon = Test(self)
    
    def ajouter_test(self, chaine_test):
        """Ajoute un test à l'évènement."""
        test = Test(self, chaine_test)
        self.__tests.append(test)
        return len(self.__tests) - 1
    
    def supprimer_test(self, indice):
        """Retire le test à l'indice spécifié."""
        test = self.__tests[indice]
        test.detruire()
        del self.__tests[indice]
    
    def ajouter_variable(self, nom, type):
        """Ajoute une variable au dictionnaire des variables.
        
        On précise :
        nom -- le nom (ne doit pas être déjà utilisé)
        type -- le nom du type sous la forme d'une chaîne de caractère
        
        """
        if nom in self.variables:
            variable = self.variables[nom]
            variable.changer_type(type)
            for evt in self.__evenements.values():
                evt.substituer_variable(nom, variable)
            
            return variable
        
        variable = Variable(self, nom, type)
        self.variables[nom] = variable
        for evt in self.__evenements.values():
            evt.substituer_variable(nom, variable)
        
        return variable
    
    def substituer_variable(self, nom, variable):
        """Modifie la variable nom."""
        self.variables[nom] = variable
    
    def supprimer_variable(self, nom):
        """Supprime, si trouvé, la variable."""
        if nom in self.variables:
            del self.variables[nom]
        
        for evt in self.__evenements.values():
            evt.supprimer_variable(nom)
    
    def creer_evenement(self, evenement):
        """Crée et ajoute l'évènement dont le nom est précisé en paramètre.
        
        L'évènement doit être une chaîne de caractères non vide. Si
        l'évènement existe, le retourne. Sinon, retourne le créé.
        
        """
        if not evenement:
            raise ValueError("Un nom vide a été passé en paramètre de " \
                    "creer_evenement.")
        
        sa_evenement = supprimer_accents(evenement).lower()
        
        if sa_evenement in self.__evenements.keys():
            evt = self.evenements[sa_evenement]
            evt.nom = evenement
            evt.script = self.script
            evt.parent = self
            return evt
        
        nouv_evenement = Evenement(self.script, evenement, self)
        self.__evenements[sa_evenement] = nouv_evenement
        
        return nouv_evenement
    
    def supprimer_evenement(self, evenement):
        """Supprime l'évènement en le retirant de son parent."""
        evenement = supprimer_accents(evenement).lower()
        del self.__evenements[evenement]
    
    def executer(self, **variables):
        """Exécution de l'évènement."""
        self.espaces.variables.update(variables)
        var_manquantes = tuple(v for v in self.variables \
                if v not in self.espaces.variables)
        if var_manquantes:
            raise ValueError("Des variables manquent à l'appel ({}).".format(
                    ", ".join(var_manquantes)))
        
        # On cherche le bon test
        for test in self.__tests:
            if test.tester(self):
                test.executer_instructions(self)
                return
        
        if self.sinon and self.sinon.tester(self):
            self.sinon.executer_instructions(self)
