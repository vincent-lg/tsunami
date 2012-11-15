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


"""Fichier contenant la fonction zone."""

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):
    
    """Retourne les salles d'une zone."""
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.zone, "str")
        cls.ajouter_types(cls.zone_filtre, "str", "str")
    
    @staticmethod
    def zone(nom_zone):
        """Retourne toutes les salles d'une zone indiquée.
        
        Cette fonction retourne toutes les salles de la zone indiquée, sans
        aucun tri. Bien que le calcul ne soit pas gourmand en ressources,
        ne pas oublier que plusieurs centaines de salle peuvent être
        retournées.
        
        """
        nom_zone = nom_zone.lower()
        try:
            zone = importeur.salle.zones[nom_zone]
        except KeyError:
            raise ErreurExecution("zone {} inconnue".format(repr(nom_zone)))
        
        return list(zone.salles)
    
    @staticmethod
    def zone_filtre(nom_zone, mnemoniques):
        """Retourne les salles filtrées d'une zone.
        
        Le filtre opère sur les mnémoniques. Si on a par exeple les salles :
            zone:ch1, zone:ch2, zone:rt1, zone:rt2, zone:mag1
        L'appel à zone("zone", "ch") retournera :
            zone:ch1, zone:ch2
        
        On peut utiliser plusieurs débuts de mnémonique, séparés par un pipe
        (|).
        L'appel à zone("zone", "ch|mag") retournera :
            zone:ch1, zone:ch2, zone:mag1
        
        """
        nom_zone = nom_zone.lower()
        mnemonics = mnemoniques.split("_b_")
        mnemonics = [m.lower() for m in mnemonics]
        try:
            zone = importeur.salle.zones[nom_zone]
        except KeyError:
            raise ErreurExecution("zone {} inconnue".format(repr(nom_zone)))
        
        salles = list(zone.salles)
        r_salles = set()
        for m in mnemonics:
            t_salles = [s for s in salles if s.mnemonic.startswith(m)]
            for salle in t_salles:
                r_salles.add(salle)
        
        return list(r_salles)
