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


"""Fichier contenant la classe ScriptObjet détaillée plus bas."""

from primaires.scripting.script import Script

class ScriptObjet(Script):

    """Script et évènements propre aux objets.

    C'est dans cette classe que sont construits les évènements du scripting
    des objets. Il est ainsi plus facile à modifier si vous souhaitez
    rajouter un évènement.

    """

    def init(self):
        """Initialisation du script"""
        # Evénement regarde
        evt_regarde = self.creer_evenement("regarde")
        evt_reg_avant = evt_regarde.creer_evenement("avant")
        evt_reg_apres = evt_regarde.creer_evenement("après")
        evt_regarde.aide_courte = "un personnage regarde l'objet"
        evt_reg_avant.aide_courte = "avant la description de l'objet"
        evt_reg_apres.aide_courte = "après la description de l'objet"
        evt_regarde.aide_longue = \
            "Cet évènement est appelé quand un personnage regarde l'objet."
        evt_reg_avant.aide_longue = \
            "Cet évènement est appelé avant que la description de l'objet " \
            "ne soit envoyée au personnage le regardant."
        evt_reg_apres.aide_longue = \
            "Cet évènement est appelé après que la description de l'objet " \
            "ait été envoyée au personnage le regardant."

        # Configuration des variables de l'évènement regarde
        var_perso = evt_regarde.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage regardant l'objet"
        var_objet = evt_regarde.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet regardé"

        # Evénement prend
        evt_prend = self.creer_evenement("prend")
        evt_prend.aide_courte = "un personnage prend l'objet"
        evt_prend.aide_longue = \
            "Cet évènement est appelé quand un personnage prend l'objet."

        # Configuration des variables de l'évènement prend
        var_perso = evt_prend.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage prenant l'objet"
        var_objet = evt_prend.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet ramassé"
        var_quantite = evt_prend.ajouter_variable("quantite", "Fraction")
        var_quantite.aide = "le nombre d'objets ramassés"

        # Evénement pose
        evt_pose = self.creer_evenement("pose")
        evt_pose.aide_courte = "un personnage pose l'objet"
        evt_pose.aide_longue = \
            "Cet évènement est appelé quand un personnage pose l'objet."

        # Configuration des variables de l'évènement pose
        var_perso = evt_pose.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage posant l'objet"
        var_objet = evt_pose.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet posé"
        var_quantite = evt_pose.ajouter_variable("quantite", "Fraction")
        var_quantite.aide = "le nombre d'objets posés"
