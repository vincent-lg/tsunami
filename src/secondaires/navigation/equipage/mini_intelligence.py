# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant la classe MiniIntelligence."""

from abstraits.obase import BaseObj
from .ordre import ordres

class MiniIntelligence(BaseObj):
    
    """Classe définissant la mini-intelligence d'un navire.
    
    Cette intelligence s'intercalle entre l'émission d'un ordre simple
    ou complexe et son exécution. Elle ne fait pas de calcul
    d'intelligence artificielle à proprement parlé. Elle est
    spécifiquement chargée de :
    *   Trouver le matelot le plus compétent pour l'ordre si nécessaire
    *   Vérifier que l'ordre s'est bien exécuté et le rerouter si besoin
    *   Décomposer un ordre complexe en ordres simplistes.
    
    Le dernier point mérite explications. Les ordres définis dans ordre
    sont dits "simples" car ils se limitent à UNE SEULE action effectuée
    par UN SEUL matelot dans un contexte précis. Si le capitaine demande
    à un matelot en cale d'aller hisser une voile, la mini intelligence
    va se charger d'émettre tous les ordres simples nécessaires :
    1.  D'abord, va vers le mât (plusieurs ordres deplacer)
    2.  Ensuite, hisse la voile (un ordre hisser_voile
    3.  Enfin, renvoie le matelot dans la cale (plusieurs ordres deplacer)
    
    """
    
    def __init__(self, navire):
        """Initialise l'intelligence liée à un navire."""
        BaseObj.__init__(self)
        self.navire = navire
    
    def __getnewargs__(self):
        return (None, )
    
    def __repr__(self):
        return "<MiniIntelligence pour {}>".format(self.navire)
    
    def emettre(self, ordre, matelot, priorite, *args):
        """Émet un ordre."""
        classe = ordres[ordre]
        ordre = classe(matelot, self.navire, *args)
        ordre.priorite = priorite
        matelot.ordonner(ordre)
