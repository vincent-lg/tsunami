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
        var_perso = evt_concentration.ajouter_variable("personnage",
                "Personnage")
        var_perso.aide = "le personnage qui concentre le sort"
        var_maitrise = evt_concentration.ajouter_variable("maitrise", "int")
        var_maitrise.aide = "la maîtrise que le personnage a de ce sort"
        var_cible = evt_concentration.ajouter_variable("cible", "Personnage")
        var_cible.aide = "la cible du sort (en l'occurence, le lanceur)"
        
        # Evénement échec
        evt_echec = self.creer_evenement("echec")
        evt_echec.aide_courte = "quelqu'un échoue à lancer le sort"
        evt_echec.aide_longue = \
            "Cet évènement est appelé lorsqu'un personnage tente de lancer " \
            "le sort, mais échoue. Par exemple : un personnage concentre " \
            "boule de feu, perd le contrôle et se fait flamber lui-même."
        
        # Configuration des variables de l'évènement échec
        var_perso = evt_echec.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage qui lance le sort"
        var_maitrise = evt_echec.ajouter_variable("maitrise", "int")
        var_maitrise.aide = "la maîtrise que le personnage a de ce sort"
        var_cible = evt_echec.ajouter_variable("cible", "Personnage")
        var_cible.aide = "la cible du sort (en l'occurence, le lanceur)"
        
        # Evénement lancement
        evt_lancement = self.creer_evenement("lancement")
        evt_lancement.aide_courte = "quelqu'un lance le sort"
        evt_lancement.aide_longue = \
            "Cet évènement est appelé lorsqu'un personnage lance le sort, "\
            "après l'avoir concentré. Par exemple : un personnage lance le " \
            "sort de boule de feu, la boule prend forme entre ses mains et " \
            "s'en échappe avec un grésillement."
        
        # Configuration des variables de l'évènement lancement
        var_perso = evt_lancement.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage qui lance le sort"
        var_maitrise = evt_lancement.ajouter_variable("maitrise", "int")
        var_maitrise.aide = "la maîtrise que le personnage a de ce sort"
        var_cible = evt_lancement.ajouter_variable("cible", "Personnage")
        var_cible.aide = "la cible du sort (en l'occurence, le lanceur)"
        
        # Evénement effet
        evt_effet = self.creer_evenement("effet")
        evt_effet.aide_courte = "le sort atteint sa cible"
        evt_effet.aide_longue = \
            "Cet évènement est appelé lorsque le sort atteint finalement " \
            "sa cible. Par exemple : une boule de feu atteint un bot " \
            "quelconque en explosant avec un grand bruit."
        
        # Configuration des variables de l'évènement effet
        var_perso = evt_effet.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage qui lance le sort"
        var_maitrise = evt_effet.ajouter_variable("maitrise", "int")
        var_maitrise.aide = "la maîtrise que le personnage a de ce sort"
        var_cible = evt_effet.ajouter_variable("cible", "Personnage")
        var_cible.aide = "la cible du sort"
        var_salle = evt_effet.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle où le sort prend effet"
        
        # Evénement part
        evt_part = self.creer_evenement("part")
        evt_part.aide_courte = "le sort quitte la salle"
        evt_part.aide_longue = \
            "Cet évènement est appelé lorsque le sort quitte la salle " \
            "courante pour se rendre dans une salle distante. Bien " \
            "entendu, cet évènement n'est appelé que si la cible est dans une " \
            "salle différente du lanceur. Si la cible est distante " \
            "de plusieurs salles, l'évènement sera appelé à chaque " \
            "fois que le sort quitte une salle pour aller dans une " \
            "autre."
        
        # Configuration des variables de l'évènement part
        var_perso = evt_part.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage qui lance le sort"
        var_maitrise = evt_part.ajouter_variable("maitrise", "int")
        var_maitrise.aide = "la maîtrise que le personnage a de ce sort"
        var_cible = evt_part.ajouter_variable("cible", "Personnage")
        var_cible.aide = "la cible du sort"
        var_salle = evt_part.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle courante du sort"
        var_destination = evt_part.ajouter_variable("destination", "Salle")
        var_destination.aide = "la salle de destination du sort"
        var_direction = evt_part.ajouter_variable("direction", "str")
        var_direction.aide = "la direction empruntée par le sort"
        
        # Evénement part
        evt_arrive = self.creer_evenement("arrive")
        evt_arrive.aide_courte = "le sort arrive dans une salle"
        evt_arrive.aide_longue = \
            "Cet évènement est appelé lorsque le sort arrive dans " \
            "une nouvelle salle en se déplaçant. De ce fait, il " \
            "n'est appelé que si la cible du sort (si présente) n'est " \
            "pas dans la même salle que le lanceur."
        
        # Configuration des variables de l'évènement arrive
        var_perso = evt_arrive.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage qui lance le sort"
        var_maitrise = evt_arrive.ajouter_variable("maitrise", "int")
        var_maitrise.aide = "la maîtrise que le personnage a de ce sort"
        var_cible = evt_arrive.ajouter_variable("cible", "Personnage")
        var_cible.aide = "la cible du sort"
        var_salle = evt_arrive.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle d'arrivée du sort"
        var_origine = evt_arrive.ajouter_variable("origine", "Salle")
        var_origine.aide = "la salle d'origine du sort"
        
        # Evénement dissipe
        evt_dissipe = self.creer_evenement("dissipe")
        evt_dissipe.aide_courte = "le sort se dissipe"
        evt_dissipe.aide_longue = \
            "Cet évènement est appelé lorsque le sort se dissipe, " \
            "souvent parce que le lanceur n'a pas fufisamment de mana " \
            "ou parce que la cible visée est trop éloignée."
        
        # Configuration des variables de l'évènement dissipe
        var_perso = evt_dissipe.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage qui lance le sort"
        var_maitrise = evt_dissipe.ajouter_variable("maitrise", "int")
        var_maitrise.aide = "la maîtrise que le personnage a de ce sort"
