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


"""Fichier contenant la classe Script détaillée plus bas."""

from abstraits.obase import *
from primaires.format.fonctions import *
from .evenement import Evenement

class Script(BaseObj):
    
    """Classe contenant un script.
    
    Un script est un ensemble d'évènements. Chaque instance devant
    faire appel à un évènement doit contenir un attribut possédant un script
    l'identifiant comme l'auteur des évènements qu'il contient.
    
    Par exemple :
        class Personnage:
            def __init__(self):
                ...
                self.script = Script(self)
    
    Comme indiqué, chaque instance de script peut contenir un ou plusieurs
    évènements qu'il est nécessaire de définir précisément avant l'appel.
    Chaque évènement peut contenir plusieurs sous-évènements.
    Pour plus d'informations, voir la classe Evènement définie dans ce package.
    
    A noter que c'est l'évènement qui stock les instructions, pas le script lui-même.
    
    Pour se construire, un script prend en paramètre :
        parent -- l'objet qui appellera le script
    
    """
    
    def __init__(self, parent):
        """Constructeur d'un script"""
        BaseObj.__init__(self)
        self.parent = parent
        self.__evenements = {}
        self._construire()
    
    def __getnewargs__(self):
        return (None, )
    
    def __getitem__(self, evenement):
        """Retourne l'évènement correspondant.
        
        L'évènement doit être une chaîne de caractères.
        
        """
        evenement = supprimer_accents(evenement).lower()
        return self.__evenements[evenement]
    
    def __setstate__(self, dico_attr):
        """Quand on récupère l'objet depuis un fichier.
        
        On s'assure que, si des évènements vides ont été ajoutés dans
        le constructeur, ils soient toujours présents.
        
        """
        BaseObj.__setstate__(self, dico_attr)
        # On crée un nouveau script pour récupérer les évènements standards
        tmp_script = type(self)(self.parent)
        evts = tmp_script.evenements
        nv_evts = evts.copy()
        nv_evts.update(self.__evenements)
        self.__evenements.update(nv_evts)
        # On s'asure que tous les évènements pointent sur le bon script
        for evenement in self.__evenements.values():
            evenement.script = self
            evt = evts.get(evenement.nom)
            if evt:
                evenement.aide_courte = evt.aide_courte
                evenement.aide_longue = evt.aide_longue
                evenement.variables = evt.variables
    
    @property
    def evenements(self):
        return dict(self.__evenements)
    
    def creer_evenement(self, evenement):
        """Crée et ajoute l'évènement dont le nom est précisé en paramètre.
        
        L'évènement doit être une chaîne de caractères non vide.
        L'évènement ne doit pas déjà exister dans ce script.
        Cette méthode retourne l'évènement créé.
        
        """
        if not evenement:
            raise ValueError("un nom vide a été passé en paramètre de " \
                    "creer_evenement")
        
        evenement = supprimer_accents(evenement).lower()
        
        if evenement in self.__evenements.keys():
            raise ValueError("ce nom d'évènement est déjà présent dans ce " \
                    "script")
        
        nouv_evenement = Evenement(self, evenement)
        self.__evenements[evenement] = nouv_evenement
        
        return nouv_evenement
    
    def supprimer_evenement(self, evenement):
        """Supprime l'évènement en le retirant du script."""
        evenement = supprimer_accents(evenement).lower()
        del self.__evenements[evenement]
