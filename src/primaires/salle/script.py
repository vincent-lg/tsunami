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


"""Fichier contenant la classe ScriptSalle détaillée plus bas."""

from primaires.scripting.script import Script

class ScriptSalle(Script):

    """Script et évènements propre aux salles.

    C'est dans cette classe que sont construits les évènements du scripting
    des salles. Il est ainsi plus facile à modifier si vous souhaitez
    rajouter un évènement.

    """

    def init(self):
        """Initialisation du script"""
        # Evénement entre
        evt_entre = self.creer_evenement("entre")
        evt_entre_avt = evt_entre.creer_evenement("avant")
        evt_entre_apr = evt_entre.creer_evenement("après")
        evt_entre.aide_courte = "un personnage entre dans la salle"
        evt_entre_avt.aide_courte = "avant d'entrer"
        evt_entre_apr.aide_courte = "après être entré"
        evt_entre.aide_longue = \
            "Cet évènement est appelé quand un personnage, joueur ou PNJ, " \
            "entre dans la salle, quelque soit sa salle de provenance et " \
            "son moyen de déplacement. Il faut cependant retirer le " \
            "déplacement par |cmd|goto|ff| qui ne déclenche pas cet évènement."
        evt_entre_avt.aide_longue = \
            "Cet évènement est appelé avant que le personnage n'entre, " \
            "c'est-à-dire avant que les différents messages ne soient " \
            "envoyés pour informer de son arrivée. On ne peut retenir " \
            "le joueur dans sa salle de départ depuis cet évènement " \
            "car le déplacement s'est déjà fait."
        evt_entre_apr.aide_longue = \
            "Cet évènement est appelé après que le personnage soit entré " \
            "dans la salle et après que lui et les autres personnages " \
            "présents en aient été informés."

        # Configuration des variables de l'évènement entre
        var_depuis = evt_entre.ajouter_variable("depuis", "str")
        var_depuis.aide = "la direction d'où vient le personnage"
        var_salle = evt_entre.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle actuelle"
        var_perso = evt_entre.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage se déplaçant"

        # Evénement sort
        evt_sort = self.creer_evenement("sort")
        evt_sort_avant = evt_sort.creer_evenement("avant")
        evt_sort_apres = evt_sort.creer_evenement("après")
        evt_sort.aide_courte = "un personnage sort de la salle"
        evt_sort_avant.aide_courte = "avant le départ de la salle"
        evt_sort_apres.aide_courte = "après le départ de la salle"
        evt_sort.aide_longue = \
            "Cet évènement est appelé quand un personnage quitte une " \
            "salle via un déplacement standard (en entrant un nom de " \
            "sortie). Le déplacement par |cmd|goto|ff| n'appelle " \
            "pas cet évènement."
        evt_sort_avant.aide_longue = \
            "Cet évènement est appelé avant que le joueur ne quitte une " \
            "salle dans son déplacement. Les autres personnages présents " \
            "n'ont pas encore reçu les messages informant de son " \
            "déplacement."
        evt_sort_apres.aide_longue = \
            "Cet évènement est appelé après qu'un personnage soit sorti " \
            "d'une salle. Il n'est pas encore arrivé dans la salle cible " \
            "mais son déplacement est bel et bien en court. Les personnages " \
            "présents dans la salle de départ en ont déjà été informés."

        # Configuration des variables de l'événement.
        var_vers = evt_sort.ajouter_variable("vers", "str")
        var_vers.aide = "la direction où va le personnage"
        var_salle = evt_sort.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle actuelle"
        var_destination = evt_sort.ajouter_variable("destination", "Salle")
        var_destination.aide = "la salle de destination"
        var_perso = evt_sort.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage se déplaçant"

        # Evénement dit
        evt_dire = self.creer_evenement("dit")
        evt_dire.aide_courte = "un personnage dit quelque chose dans la salle"
        evt_dire.aide_longue = \
            "Cet évènement est appelé quand un personnage dit quelque " \
            "chose dans la salle. Ce qu'il dit se trouve dans la " \
            "variable |ent|message|ff|."

        # Configuration des variables de l'événement.
        var_message = evt_dire.ajouter_variable("message", "str")
        var_message.aide = "le message prononcé"
        var_salle = evt_dire.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle actuelle"
        var_perso = evt_dire.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage qui parle"

        # Evénement connecte
        evt_connecte = self.creer_evenement("connecte")
        evt_connecte.aide_courte = "un joueur se connecte dans la salle"
        evt_connecte.aide_longue = \
            "Cet évènement est appelé quand un joueur se connecte dans la " \
            "salle. Notez que, bien que le terme \"personnage\" soit utilisé " \
            "pour des raisons principalement techniques, les PNJ ne se " \
            "connectent jamais. Cet évènement ne concerne donc que les " \
            "joueurs."

        # Configuration des variables de l'événement.
        var_salle = evt_connecte.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle actuelle"
        var_perso = evt_connecte.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage qui se connecte"

        # Evénement tick
        evt_tick = self.creer_evenement("tick")
        evt_tick.aide_courte = "la salle se tick"
        evt_tick.aide_longue = \
            "Cet évènement est appelé quand la salle se tick (toutes les " \
            "minutes)."

        # Configuration des variables de l'événement.
        var_salle = evt_tick.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle actuelle"

        # Évènement changer
        evt_changer = self.creer_evenement("changer")
        evt_changer.aide_courte = "le temps (minute heure jour...) change"
        evt_changer.aide_longue = \
            "Cet évènement est appelé quand le temps se modifie. Des " \
            "sous-évènements spécifiques sont utilisés toutes les " \
            "minutes, les heures, les jours, les mois ou les années. " \
            "Notez que, pour utiliser cet évènement, vous devez créer " \
            "des tests pré-conditonnels (si vous écrivez des lignes " \
            "d'instructions dans le test 'sinon', elles ne seront jamais " \
            "exécutées)."
        evt_changer_minute = evt_changer.creer_evenement("minute")
        evt_changer_minute.aide_courte = "au changement de minute"
        evt_changer_minute.aide_longue = \
            "Cet évènement est appelé au changement de minute. Utilisez " \
            "une ou plusieurs des variables proposées pour vérifier " \
            "l'heure. Par exemple, entrez le test " \
            "|cmd|\"${heure}:${minute}\" = \"18:25\"|ff| pour lancer un " \
            "test à 18:25 précise. Notez que vous pouvez aussi utiliser " \
            "la notation plus longue |cmd|heure = 18 et minute = 25|ff|. " \
            "Dans tous les cas, ne mettez pas d'instructions dans le " \
            "test 'sinon', elles seront ignorées : créez toujours un " \
            "ou plusieurs tests."
        evt_changer_heure = evt_changer.creer_evenement("heure")
        evt_changer_heure.aide_courte = "au changement d'heure"
        evt_changer_heure.aide_longue = \
            "Cet évènement est appelé au changement d'heure. Utilisez " \
            "une ou plusieurs des variables proposées pour vérifier " \
            "l'heure. Par exemple, entrez le test " \
            "|cmd|heure = 18|ff| pour lancer un test tous les jours à " \
            "18:00. Dans tous les cas, ne mettez pas d'instructions dans le " \
            "test 'sinon', elles seront ignorées : créez toujours un " \
            "ou plusieurs tests."
        evt_changer_jour = evt_changer.creer_evenement("jour")
        evt_changer_jour.aide_courte = "au changement de jour"
        evt_changer_jour.aide_longue = \
            "Cet évènement est appelé au changement de jour. Utilisez " \
            "une ou plusieurs des variables proposées pour vérifier " \
            "la date. Par exemple, entrez le test " \
            "|cmd|\"${jour}-${mois}\" = \"15-3\"|ff| pour lancer un " \
            "test le 15ème jour du 3ème mois. Notez que vous pouvez aussi " \
            "utiliser la notation plus longue |cmd|jour = 15 et mois = " \
            "3|ff|. Dans tous les cas, ne mettez pas d'instructions dans le " \
            "test 'sinon', elles seront ignorées : créez toujours un " \
            "ou plusieurs tests."
        evt_changer_mois = evt_changer.creer_evenement("mois")
        evt_changer_mois.aide_courte = "au changement de mois"
        evt_changer_mois.aide_longue = \
            "Cet évènement est appelé au changement de mois. Utilisez " \
            "une ou plusieurs des variables proposées pour vérifier " \
            "le mois. Par exemple, entrez le test " \
            "|cmd|mois = 8|ff| pour lancer un test tous les ans au " \
            "début du 8ème mois. Dans tous les cas, ne mettez pas " \
            "d'instructions dans le test 'sinon', elles seront ignorées : " \
            "créez toujours un ou plusieurs tests."
        evt_changer_annee = evt_changer.creer_evenement("année")
        evt_changer_annee.aide_courte = "au changement d'années"
        evt_changer_annee.aide_longue = \
            "Cet évènement est appelé au changement d'année."

        # Configuration des variables de l'événement.
        var_salle = evt_changer.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle actuelle"
        var_minute = evt_changer.ajouter_variable("minute", "Fraction")
        var_minute.aide = "le nombre de minutes (entre 0 et 59)"
        var_heure = evt_changer.ajouter_variable("heure", "Fraction")
        var_heure.aide = "le nombre d'heures (entre 0 et 23)"
        var_jour = evt_changer.ajouter_variable("jour", "Fraction")
        var_jour.aide = "le nombre de jours (entre 1 et 30)"
        var_mois = evt_changer.ajouter_variable("mois", "Fraction")
        var_mois.aide = "le nombre de mois (entre 1 et 12)"
        var_annee = evt_changer.ajouter_variable("annee", "Fraction")
        var_annee.aide = "le nombre d'années"

        # Evénement recherche
        evt_recherche = self.creer_evenement("recherche")
        evt_recherche.aide_courte = "un personnage cherche dans la salle"
        evt_recherche.aide_longue = \
            "Cet évènement est appelé quand un personnage utilise la " \
            "commande chercher/lookfor dans la salle. Le texte recherché " \
            "est placé dans la variable 'texte'. Utilisez de préférence " \
            "la fonction 'expression' pour tester le contenu du texte. " \
            "D'autre part, mettez bien les différents traitements dans " \
            "des tests séparés : en effet, si le test sinon est executé, " \
            "le système considère que le texte n'a pas été trouvé et " \
            "envoie une réponse conforme au personnage. Si au contraire " \
            "vous faites des tests du type 'expression(texte, " \
            "\"forêt|arbres\")' par exemple, le système considérera que " \
            "le test appelé transmet le message de réussite ou d'échec au " \
            "personnage."

        # Configuration des variables de l'événement.
        var_texte = evt_recherche.ajouter_variable("texte", "str")
        var_texte.aide = "le texte recherché"
        var_salle = evt_recherche.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle actuelle"
        var_perso = evt_recherche.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage qui fait la recherche"

        # Événement effacer_memoire
        evt_effacer_memoire = self.creer_evenement("effacer_memoire")
        evt_effacer_memoire.aide_courte = "une mémoire est effacée"
        evt_effacer_memoire.aide_longue = \
            "Cet évènement est appelé quand une mémoire " \
            "enregistrée dans l'objet est effacée par le système. " \
            "C'est très utile pour exécuter une action particulière " \
            "quand une mémoire expire."

        # Configuration des variables de l'évènement effacer_memoire
        var_salle = evt_effacer_memoire.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle-même"
        var_nom = evt_effacer_memoire.ajouter_variable("nom", "str")
        var_nom.aide = "le nom de la mémoire à effacer"
        var_valeur = evt_effacer_memoire.ajouter_variable("valeur", "Object")
        var_valeur.aide = "la valeur de la mémoire qu'on va effacer"
