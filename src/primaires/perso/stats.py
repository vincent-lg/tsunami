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

from .stat import *
from abstraits.obase import BaseObj 

class Stats(BaseObj):
    
    """Cette classe définit un conteneur des stats (ou caractéristiques).
    Les stats sont construites dynamiquement dans la configuration du
    module Personnage et un conteneur de Stats, bases_stats, est créée dans
    le module Personnage. Tous les conteneurs de stats s'inspirent
    de ce modèle.
    
    """
    
    def __init__(self, config, parent=None):
        """Constructeur du conteneur.
        On s'inspire de la configuration pour créer la base des Stats.
        
        """
        BaseObj.__init__(self)
        self.__stats = []
        for ligne in config.stats:
            nom = ligne[0]
            stat = Stat(*ligne)
            setattr(self, "_{}".format(nom), stat)
            self.__stats.append(stat)
        print("La base crée est :", str(self))
    
    def __getinitargs__(self):
        return (None, )
    
    def __str__(self):
        ret = "  "
        for stat in self.__stats:
            ret += str(stat) + "\n  "
        
        return ret.rstrip(" \n")
    
    def __getattr__(self, nom_attr):
        """Si le 'nom_attr' n'est pas trouvé, on redigive vers la valeur
        courante de la stat. Par exemple, si on entre 'stats.force', on
        va chercher dans 'stats.;_force.courante'.
        
        """
        stat = getattr(self, "_{}".format(nom_attr))
        return stat.courante
    
    def enregistrer(self):
        """Enregistre le parent"""
        if self.parent:
            self.parent = parent
