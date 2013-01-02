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
from primaires.format.fonctions import *

# Statuts de l'attitude
FONCTIONNELLE = 1
SANS_CIBLE = 2
CIBLE_OBLIGATOIRE = 3
INACHEVEE = 4

# Ce dictionnaire lie un statut à une chaîne
STATUTS = {
    FONCTIONNELLE : "|vr|fonctionnelle|ff|",
    SANS_CIBLE : "|jn|sans cible|ff|",
    CIBLE_OBLIGATOIRE : "|jn|cible obligatoire|ff|",
    INACHEVEE : "|rg|inachevée|ff|"
}

class Attitude(BaseObj):

    """Cette classe contient une attitude jouable dans l'univers.
    
    """
    
    def __init__(self, cle, parent=None):
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
        if acteur.est_mort():
            acteur << "|err|Vous êtes comme inconscient.|ff|"
            return
        
        statut = self.statut
        if statut == INACHEVEE:
            acteur << "|err|Cette attitude n'est pas achevée.|ff|"
            return
        
        def formater(str, acteur="", cible=""):
            str = str.replace("_b_acteur_b_", "{acteur}")
            str = str.replace("_b_cible_b_", "{cible}")
            return str
        
        try:
            nom_cible = arguments.split(" ")[1]
        except IndexError:
            # Le joueur n'a pas donné de cible
            if statut == CIBLE_OBLIGATOIRE:
                acteur << "|err|Vous devez préciser une cible.|ff|"
                return
            for personnage in acteur.salle.personnages:
                if acteur.est_masculin():
                    if personnage is acteur:
                        personnage << self.independant["aim"]
                    else:
                        personnage.envoyer(formater(self.independant["oim"]),
                                acteur=acteur)
                else:
                    if personnage is acteur:
                        personnage << self.independant["aif"]
                    else:
                        personnage.envoyer(formater(self.independant["oif"]),
                                acteur=acteur)
        else:
            # Le joueur a précisé une cible
            if statut == SANS_CIBLE:
                acteur << "|err|Cette attitude n'accepte pas de cible.|ff|"
                return
            cible = None
            for personnage in acteur.salle.personnages:
                nom_perso = personnage.get_nom_pour(acteur)
                if acteur.peut_voir(personnage) and contient(nom_perso,
                        nom_cible):
                    cible = personnage
            if cible is None:
                acteur << "|err|Vous ne voyez pas cette personne ici.|ff|"
                return
            for personnage in acteur.salle.personnages:
                if acteur.est_masculin():
                    if personnage is acteur:
                        personnage.envoyer(formater(self.dependant["adm"]),
                                cible=cible)
                    elif personnage is cible:
                        personnage.envoyer(formater(self.dependant["idm"]),
                                acteur=acteur)
                    else:
                        personnage.envoyer(formater(self.dependant["odm"]),
                                acteur=acteur, cible=cible)
                else:
                    if personnage is acteur:
                        personnage.envoyer(formater(self.dependant["adf"]),
                                cible=cible)
                    elif personnage is cible:
                        personnage.envoyer(formater(self.dependant["idf"]),
                                acteur=acteur)
                    else:
                        personnage.envoyer(formater(self.dependant["odf"]),
                                acteur=acteur, cible=cible)
