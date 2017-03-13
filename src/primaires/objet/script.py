# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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

        # Evénement porte
        evt_porte = self.creer_evenement("porte")
        evt_porte.aide_courte = "un personnage équipe l'objet"
        evt_porte.aide_longue = \
            "Cet évènement est appelé quand un personnage porte " \
            "(c'est-à-dire équipe) l'objet."

        # Configuration des variables de l'évènement porte
        var_perso = evt_porte.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage équipant l'objet"
        var_objet = evt_porte.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet équipé"

        # Evénement retire
        evt_retire = self.creer_evenement("retire")
        evt_retire.aide_courte = "un personnage retire l'objet"
        evt_retire.aide_longue = \
            "Cet évènement est appelé quand un personnage retire " \
            "(c'est-à-dire déséquipe) l'objet."

        # Configuration des variables de l'évènement retire
        var_perso = evt_retire.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage déséquipant l'objet"
        var_objet = evt_retire.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet déséquipé"

        # Evénement effacer_memoire
        evt_effacer_memoire = self.creer_evenement("effacer_memoire")
        evt_effacer_memoire.aide_courte = "une mémoire est effacée"
        evt_effacer_memoire.aide_longue = \
            "Cet évènement est appelé quand une mémoire " \
            "enregistrée dans l'objet est effacée par le système. " \
            "C'est très utile pour exécuter une action particulière " \
            "quand une mémoire expire."

        # Configuration des variables de l'évènement effacer_memoire
        var_objet = evt_effacer_memoire.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet-même"
        var_nom = evt_effacer_memoire.ajouter_variable("nom", "str")
        var_nom.aide = "le nom de la mémoire à effacer"
        var_valeur = evt_effacer_memoire.ajouter_variable("valeur", "Object")
        var_valeur.aide = "la valeur de la mémoire qu'on va effacer"

        # Événement créé
        evt_cree = self.creer_evenement("créé")
        evt_cree.aide_courte = "l'objet est créé"
        evt_cree.aide_longue = \
            "Cet évènement est appelé quand l'objet est créé, pas " \
            "nécessairement quelque part. Il faut donc éviter de se " \
            "fier au contexte de l'objet (est-il posé au sol, par " \
            "exemple) car l'objet n'a pas encore de contexte à ce " \
            "stade. Il existe mais pas nécessairement quelque part. " \
            "Il a pu être créé par la fonction scripting 'creer_objet' " \
            "par exemple, et dans ce cas il sera manipulé avant " \
            "d'apparaître quelque part. Cet évènement est toutefois " \
            "utile pour créer des mémoires spécifiques, avoir des " \
            "objets qui se détériorent progressivement, par exemple."

        # Configuration des variables de l'évènement créé
        var_objet = evt_cree.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet nouvellement créé"


# Événement lève
        evt_leve = self.creer_evenement("lève")
        evt_leve.aide_courte = "un personnage se lève de sur l'objet"
        evt_leve.aide_longue = \
            "Cet évènement est appelé quand un personnage se lève " \
            "de sur l'objet. Sous-évènements disponibles : avant et après." \

        # Configuration des variables de l'évènement lève
        var_perso = evt_leve.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage se levant"
        var_salle = evt_leve.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se trouve le personnage"

# Événement lève.avant
        evt_leve_avant = evt_leve.creer_evenement("avant")
        evt_leve_avant.aide_courte = "un personnage veut se lever de sur l'objet"
        evt_leve_avant.aide_longue = \
            "Cet évènement est appelé quand un personnage cherche à se lever " \
            "de sur l'objet. Il se produit avant le " \
            "message comme quoi le personnage s'est levé. L'état " \
            "n'a pas encore été retiré."

        # Configuration des variables de l'évènement lève.avant
        var_perso = evt_leve_avant.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage souhaitant se lever"
        var_salle = evt_leve_avant.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se trouve le personnage"

# Événement lève.après
        evt_leve_apres = evt_leve.creer_evenement("après")
        evt_leve_apres.aide_courte = "un personnage se lève de sur l'objet"
        evt_leve_apres.aide_longue = \
            "Cet évènement est appelé quand un personnage se lève " \
            "de sur l'objet. Il se produit après le " \
            "message comme quoi le personnage s'est levé. L'état " \
            "a déjà été retiré."

        # Configuration des variables de l'évènement lève.après
        var_perso = evt_leve_apres.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage se levant"
        var_salle = evt_leve_apres.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se trouve le personnage"

# Événement asseoit
        evt_asseoit = self.creer_evenement("asseoit")
        evt_asseoit.aide_courte = "un personnage s'asseoit sur l'objet"
        evt_asseoit.aide_longue = \
            "Cet évènement est appelé quand un personnage s'asseoit " \
            "sur l'objet. Sous-évènements disponibles : avant et après." \

        # Configuration des variables de l'évènement asseoit
        var_perso = evt_asseoit.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage s'asseyant"
        var_salle = evt_asseoit.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se trouve le personnage"

# Événement asseoit.avant
        evt_asseoit_avant = evt_asseoit.creer_evenement("avant")
        evt_asseoit_avant.aide_courte = "un personnage veut s'asseoir sur l'objet"
        evt_asseoit_avant.aide_longue = \
            "Cet évènement est appelé quand un personnage cherche à s'asseoir " \
            "sur l'objet. Il se produit avant le " \
            "message comme quoi le personnage s'est assis. L'état " \
            "n'a pas encore été ajouté."

        # Configuration des variables de l'évènement asseoit.avant
        var_perso = evt_asseoit_avant.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage souhaitant s'asseoir"
        var_salle = evt_asseoit_avant.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se trouve le personnage"

# Événement asseoit.après
        evt_asseoit_apres = evt_asseoit.creer_evenement("après")
        evt_asseoit_apres.aide_courte = "un personnage s'asseoit sur l'objet"
        evt_asseoit_apres.aide_longue = \
            "Cet évènement est appelé quand un personnage s'asseoit " \
            "sur l'objet. Il se produit après le " \
            "message comme quoi le personnage s'est assis. L'état " \
            "a déjà été ajouté."

        # Configuration des variables de l'évènement asseoit.après
        var_perso = evt_asseoit_apres.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage se levant"
        var_salle = evt_asseoit_apres.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se trouve le personnage"


# Événement allonge
        evt_allonge = self.creer_evenement("allonge")
        evt_allonge.aide_courte = "un personnage s'allonge sur l'objet"
        evt_allonge.aide_longue = \
            "Cet évènement est appelé quand un personnage s'allonge " \
            "sur l'objet. Sous-évènements disponibles : avant et après." \

        # Configuration des variables de l'évènement allonge
        var_perso = evt_allonge.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage s'allongeant"
        var_salle = evt_allonge.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se trouve le personnage"

# Événement allonge.avant
        evt_allonge_avant = evt_allonge.creer_evenement("avant")
        evt_allonge_avant.aide_courte = "un personnage veut s'allonger sur l'objet"
        evt_allonge_avant.aide_longue = \
            "Cet évènement est appelé quand un personnage cherche à s'allonger " \
            "sur l'objet. Il se produit avant le " \
            "message comme quoi le personnage s'est allongé. L'état " \
            "n'a pas encore été ajouté."

        # Configuration des variables de l'évènement allonge.avant
        var_perso = evt_allonge_avant.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage souhaitant s'allonger"
        var_salle = evt_allonge_avant.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se trouve le personnage"

# Événement allonge.après
        evt_allonge_apres = evt_allonge.creer_evenement("après")
        evt_allonge_apres.aide_courte = "un personnage s'allonge sur l'objet"
        evt_allonge_apres.aide_longue = \
            "Cet évènement est appelé quand un personnage s'allonge " \
            "sur l'objet. Il se produit après le " \
            "message comme quoi le personnage s'est allongé. L'état " \
            "a déjà été ajouté."

        # Configuration des variables de l'évènement allonge.après
        var_perso = evt_allonge_apres.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage s'allongeant"
        var_salle = evt_allonge_apres.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se trouve le personnage"

