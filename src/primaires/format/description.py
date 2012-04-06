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


"""Fichier contenant la classe Description, détaillée plus bas."""

import re
from textwrap import wrap

from abstraits.obase import BaseObj
from .fonctions import *

# Constantes
TAILLE_LIGNE = 75

class Description(BaseObj):
    
    """Cette classe définit une description générique.
    Ce peut être une description de salle, d'objet, de balise, de
    véhicule...
    
    Elle propose plusieurs méthodes facilitant son déploiement dans un
    éditeur et sa mise en forme.
    
    """
    
    def __init__(self, description=None, parent=None, scriptable=True):
        """Constructeur"""
        BaseObj.__init__(self)
        self.paragraphes = [] # une liste des différents paragraphes
        self.saut_de_ligne = False
        self.parent = parent
        self.script = ScriptDescription(self)
        self.scriptable = scriptable
        if description:
            self.ajouter_paragraphe(description)
    
    def __getnewargs__(self):
        return ("", )
    
    def __str__(self):
        """Retourne la description sous la forme d'un texte 'str'"""
        res = []
        for paragraphe in self.paragraphes:
            paragraphe = self.wrap_paragraphe(paragraphe)
            paragraphe = paragraphe.replace("|nl|", "\n")
            res.append(paragraphe)
        return "\n".join(res)
    
    def __bool__(self):
        """Retourne True si la description n'est pas vide, False sinon."""
        return bool(str(self))
    
    def ajouter_paragraphe(self, paragraphe):
        """Ajoute un paragraphe.
        
        """
        self.paragraphes.append(paragraphe)
    
    def supprimer_paragraphe(self, no):
        """Supprime le paragraphe #no"""
        del self.paragraphes[no]
    
    def vider(self):
        """Supprime toute la description"""
        self.paragraphes[:] = []
    
    def remplacer(self, origine, par):
        """Remplace toutes les occurences de 'origine' par 'par'.
        Cette recherche & remplacement se fait dans tous les paragraphes.
        Le remplacement ne tient compte ni des majuscules, ni des accents.
        
        """
        origine = supprimer_accents(origine)
        diff = len(origine) - len(par)
        for i, paragraphe in enumerate(self.paragraphes):
            paragraphe = supprimer_accents(paragraphe).lower()
            # On cherche 'origine'
            no_car = paragraphe.find(origine)
            while no_car >= 0:
                self.paragraphes[i] = self.paragraphes[i][:no_car] + \
                        par + self.paragraphes[i][no_car + len(origine):]
                paragraphe = supprimer_accents(self.paragraphes[i]).lower()
                no_car = paragraphe.find(origine, no_car + len(par))
    
    def wrap_paragraphe(self, paragraphe, lien="\n", aff_sp_cars=False):
        """Wrap un paragraphe et le retourne"""
        if aff_sp_cars:
            paragraphe = echapper_sp_cars(paragraphe)
        else:
            paragraphe = paragraphe.replace("|tab|", "   ")
        return lien.join(wrap(paragraphe, TAILLE_LIGNE))
    
    @property
    def paragraphes_indentes(self):
        """Retourne les paragraphes avec une indentation du niveau spécifié"""
        indentation = "\n   "
        res = []
        for paragraphe in self.paragraphes:
            paragraphe = self.wrap_paragraphe(paragraphe, lien=indentation)
            paragraphe = paragraphe.replace("|nl|", "\n")
            res.append(paragraphe)
        
        if not res:
            res.append("Aucune description.")
        
        return indentation + indentation.join(res)
    
    def regarder(self, personnage, elt=None):
        """Le personnage regarde la description."""
        paragraphes = []
        elt = elt or self.parent
        for paragraphe in self.paragraphes:
            paragraphe = paragraphe.replace("|nl|", "\n").replace(
                    "|tab|", "   ")
            if self.scriptable:
                evts = re.findall(r"(\$[a-z0-9]+)([\n ,.]|$)", paragraphe)
                evts = [e[0] for e in evts]
                for nom_complet in evts:
                    nom = nom_complet[1:]
                    evt = self.script["regarde"][nom]
                    evt.executer(regarde=elt, personnage=personnage)
                    retour = evt.espaces.variables["retour"]
                    paragraphe = paragraphe.replace(nom_complet, retour)
            paragraphes.append("\n".join(wrap(paragraphe)))
        return "\n".join(paragraphes)

# On importe ici pour éviter les boucles
from primaires.scripting.script import Script

class ScriptDescription(Script):
    
    def init(self):
        """Initialisation du script."""
        evt = self.creer_evenement("regarde")
        var_regarde = evt.ajouter_variable("regarde", "BaseObj")
        var_personnage = evt.ajouter_variable("personnage", "Personnage")
        var_regarde.aide = "l'élément regardé"
        var_personnage.aide = "le personnage regardant"
