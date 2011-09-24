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


"""Fichier contenant la classe Stats, détaillée plus bas."""

from abstraits.obase import BaseObj 
from .stat import *

class Stats(BaseObj):
    
    """Cette classe définit un conteneur des stats (ou caractéristiques).
    Les stats sont construites dynamiquement dans la configuration du
    module Personnage et un conteneur de Stats, bases_stats, est créée dans
    le module Personnage. Tous les conteneurs de stats s'inspirent
    de ce modèle.
    
    """
    
    def __init__(self, parent=None):
        """Constructeur du conteneur.
        On s'inspire de la configuration pour créer la base des Stats.
        
        """
        BaseObj.__init__(self)
        config = type(self).importeur.perso.cfg_stats
        self.parent = parent
        self.__stats = []
        for ligne in config.stats:
            nom = ligne[0]
            stat = Stat(*ligne, parent=self)
            setattr(self, "_{}".format(nom), stat)
            self.__stats.append(stat)
        
        self._construire()
    
    def __getnewargs__(self):
        return ()
    
    def __str__(self):
        ret = "  "
        for stat in self.__stats:
            ret += str(stat) + "\n  "
        
        return ret.rstrip(" \n")
    
    def __iter__(self):
        stats = [getattr(self, "_{}".format(stat.nom)) for stat in \
                self.__stats]
        return iter(tuple(stats))
    
    def __getattr__(self, nom_attr):
        """Si le 'nom_attr' n'est pas trouvé, on redirige vers la valeur
        courante de la stat. Par exemple, si on entre 'stats.force', on
        va chercher dans 'stats.;_force.courante'.
        
        """
        stat = object.__getattribute__(self, "_{}".format(nom_attr))
        return stat.courante
    
    def __setattr__(self, nom_attr, val_attr):
        nom_stat = "_{}".format(nom_attr)
        if hasattr(self, nom_stat):
            objet = getattr(self, nom_stat)
            if isinstance(objet, Stat):
                objet.courante = val_attr
                pass
        else:
            BaseObj.__setattr__(self, nom_attr, val_attr)
    
    def enregistrer(self):
        """Enregistre le parent"""
        if self.construit and self.parent:
            self.parent.enregistrer()
    
    def restaurer(self):
        """Restaure les stats.
        
        Toutes les stats ayant un maximum sont remis à ce maximum.
        
        """
        for stat in self:
            if stat.max:
                stat.courante = stat.max
