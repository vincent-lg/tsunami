# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Ce fichier définit la classe Cherchable, classe abstraite de base
pour les objets de recherche (voir plus bas).

"""

from abstraits.obase import BaseObj
from primaires.recherche.filtre import Filtre
from primaires.recherche.cherchables import MetaCherchable

INTERDITS = ["a", "aide"]

class Cherchable(BaseObj, metaclass=MetaCherchable):
    
    """Classe de base des objets de recherche.
    
    Cette classe modélise les items que l'on est susceptible de rechercher
    dans l'univers : objets, salles, personnages... Elle associe à chacun une
    liste de filtres de recherche correspondant à des options (syntaxe Unix).
    
    De fait, c'est plutôt une enveloppe de filtres et d'objets à traiter.
    Pour un exemple d'utilisation, voir primaires/objet/cherchables/objet.py.
    
    """
    
    nom_cherchable = ""
    
    def __init__(self):
        """Constructeur de la classe"""
        self.filtres = []
        
        # Initialisation du cherchable
        self.init()
    
    def init(self):
        """Méthode d'initialisation.
        
        C'est ici que l'on ajoute réellement les filtres, avec la méthode
        dédiée.
        
        """
        raise NotImplementedError
    
    @property
    def courtes(self):
        """Renvoie une chaîne des options courtes au bon format"""
        avec = []
        sans = ""
        for filtre in self.filtres:
            courte = filtre.opt_courte
            courte += ":" if filtre.type else ""
            if filtre.opt_longue:
                avec.append(courte)
            else:
                sans += courte
        avec = "".join(sorted(avec))
        print(avec + sans)
        return avec + sans
    
    @property
    def longues(self):
        """Renvoie une liste des options longues au bon format"""
        ret = []
        for filtre in self.filtres:
            if filtre.opt_longue:
                egal = "=" if filtre.type else ""
                ret.append(filtre.opt_longue + egal)
        print(sorted(ret))
        return sorted(ret)
    
    @property
    def items(self):
        """Renvoie la liste des objets traités"""
        raise NotImplementedError
    
    def ajouter_filtre(self, opt_courte, opt_longue, test, type=""):
        """Ajoute le filtre spécifié"""
        longues = [f.opt_longue for f in self.filtres]
        if opt_courte in self.courtes or opt_courte in INTERDITS:
            raise ValueError("l'option courte '{}' est indisponible".format(
                    opt_courte))
        if opt_longue in longues or opt_longue in INTERDITS:
            raise ValueError("l'option longue '{}' est indisponible".format(
                    opt_longue))
        if type and type not in ("int", "str", "bool"):
            raise ValueError("le type {} est invalide".format(type))
        self.filtres.append(Filtre(opt_courte, opt_longue, test, type))
    
    def tester(self, options, liste):
        """Teste une liste de couples (option, argument)"""
        if not options:
            return liste
        liste_ret = []
        # On regarde la première option
        o, a = options[0]
        # Pour chaque objet de la liste à traiter
        for item in liste:
            o_testee = False
            # On récupère le filtre adéquat
            for filtre in self.filtres:
                if o in ("-" + filtre.opt_courte, "--" + filtre.opt_longue):
                    # Si le filtre dit oui, on retient l'objet en question
                    if filtre.tester(item, a):
                        liste_ret.append(item)
                    o_testee = True
            if not o_testee:
                raise ValueError("l'option {} n'existe pas".format(o))
        del options[0]
        return self.tester(options, liste_ret)
    
    def afficher(self, objet):
        """Méthode d'affichage des objets traités"""
        raise NotImplementedError
