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


"""Ce fichier contient la classe Attitude détaillée plus bas."""

from abstraits.obase import *

# Statuts de l'attitude
FONCTIONNELLE = 1
SANS_CIBLE = 2
CIBLE_OBLIGATOIRE = 3
INACHEVEE = 4

# Ce dictionnaire lie un statut à une chaîne
STATUTS = {
    FONCTIONNELLE : "fonctionnelle",
    SANS_CIBLE : "sans cible",
    CIBLE_OBLIGATOIRE : "cible obligatoire",
    INACHEVEE : "inachevée"
}

class Attitude(BaseObj):

    """Cette classe contient une attitude jouable dans l'univers.
    
    """
    
    def __init__(self, cle, parent):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.parent = parent
        self.cle = cle
        self.independant = {
            "aim" : "",
            "aif" : "",
            "oim" : "",
            "oif" : "",
        }
        self.dependant = {
            "adm" : "",
            "adf" : "",
            "idm" : "",
            "idf" : "",
            "odm" : "",
            "odf" : "",
        }
        # On passe le statut en CONSTRUIT
        self._statut = CONSTRUIT
    
    def __getnewargs__(self):
        return ("", None)
    
    def __setattr__(self, nom_attr, valeur):
        """Enregisre le parent si il est précisé"""
        construit = self.construit
        BaseObj.__setattr__(self, nom_attr, valeur)
        if construit and self.parent:
            self.parent.enregistrer()
    
    @property
    def statut(self):
        """Renvoie le statut de l'attitude"""
        # On teste les deux dicos
        indep_complet = True
        for indep in self.independant.values():
            if not indep or indep.isspace():
                indep_complet = False
                break
        dep_complet = True
        for dep in self.dependant.values():
            if not dep or dep.isspace():
                dep_complet = False
                break
        if indep_complet and dep_complet:
            ret = FONCTIONNELLE
        elif indep_complet and not dep_complet:
            ret = SANS_CIBLE
        elif not indep_complet and dep_complet:
            ret = CIBLE_OBLIGATOIRE
        elif not indep_complet and not dep_complet:
            ret = INACHEVEE
        return ret
    
    def jouer(self, acteur, arguments):
        """Joue le social pour acteur"""
        arguments = arguments.split(" ")
        statut = self.statut
        if statut == INACHEVEE:
            acteur << "|err|Cette attitude n'est pas achevée.|ff|"
            return
        try:
            cible = arguments[1]
        except IndexError:
            # Le joueur n'a pas donné de cible
            if statut == CIBLE_OBLIGATOIRE:
                acteur << "|err|Vous devez préciser une cible.|ff|"
                return
            for personnage in acteur.salle.personnages:
                if personnage is acteur:
                    personnage << self.independant["aim"]
                else:
                    personnage << self.independant["oim"].replace("|acteur|", acteur.nom)
        else:
            # Le joueur a précisé une cible
            if statut == SANS_CIBLE:
                acteur << "|err|Cette attitude n'accepte pas de cible.|ff|"
                return
            for personnage in acteur.salle.personnages:
                if personnage.nom == cible:
                    cible = personnage
            if type(cible) == str:
                acteur << "|err|Vous ne voyez pas cette personne ici.|ff|"
                return
            for personnage in acteur.salle.personnages:
                if personnage is acteur:
                    personnage << self.dependant["adm"]
                elif personnage is cible:
                    personnage << self.dependant["idm"]
                else:
                    personnage << self.dependant["odm"]
