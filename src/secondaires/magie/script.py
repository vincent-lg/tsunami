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


"""Fichier contenant la classe ScriptSort détaillée plus bas."""

from primaires.scripting.script import Script

class ScriptSort(Script):
    
    """Script et évènements propre aux sorts.
    
    C'est dans cette classe que sont construits les évènements du scripting
    de la magie. Il est ainsi plus facile à modifier si vous souhaitez
    rajouter un évènement.
    
    """
    
    def init(self):
        """Initialisation du script"""
        # Evénement concentration
        evt_concentration = self.creer_evenement("concentration")
        evt_concentration.aide_courte = "quelqu'un concentre le sort"
        evt_concentration.aide_longue = \
            "Cet évènement est appelé lorsqu'un personnage concentre le " \
            "sort, c'est-à-dire tente de le lancer. Par exemple : un " \
            "personnage concentre le sort de boule de feu, une aura rouge " \
            "l'entoure soudain."
        
        # Configuration des variables de l'évènement concentration
        var_perso = evt_concentration.ajouter_variable("lanceur", "Personnage")
        var_perso.aide = "le personnage qui concentre le sort"
        var_maitrise = evt_concentration.ajouter_variable("maitrise", "int")
        var_maitrise.aide = "la maîtrise que le personnage a de ce sort"
        
        # Evénement lancement
        evt_lancement = self.creer_evenement("lancement")
        evt_lancement.aide_courte = "quelqu'un lance le sort"
        evt_lancement.aide_longue = \
            "Cet évènement est appelé lorsqu'un personnage lance le sort, "\
            "après l'avoir concentré. Par exemple : un personnage lance le " \
            "sort de boule de feu, la boule prend forme entre ses mains et " \
            "s'en échappe avec un grésillement."
        
        # Configuration des variables de l'évènement lancement
        var_perso = evt_lancement.ajouter_variable("lanceur", "Personnage")
        var_perso.aide = "le personnage qui lance le sort"
        var_maitrise = evt_lancement.ajouter_variable("maitrise", "int")
        var_maitrise.aide = "la maîtrise que le personnage a de ce sort"
        
        # Evénement effet
        evt_effet = self.creer_evenement("effet")
        evt_effet.aide_courte = "le sort atteint sa cible"
        evt_effet.aide_longue = \
            "Cet évènement est appelé lorsque le sort atteint finalement " \
            "sa cible. Par exemple : une boule de feu atteint un bot " \
            "quelconque en explosant avec un grand bruit."
        
        # Configuration des variables de l'évènement effet
        var_perso = evt_effet.ajouter_variable("lanceur", "Personnage")
        var_perso.aide = "le personnage qui lance le sort"
        var_maitrise = evt_effet.ajouter_variable("maitrise", "int")
        var_maitrise.aide = "la maîtrise que le personnage a de ce sort"
