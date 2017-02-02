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


"""Fichier contenant l'action donner_bonus."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution
from primaires.format.fonctions import supprimer_accents

class ClasseAction(Action):

    """Donne ou retire des bonus temporaires à un personnage.

    Cette action permet de donner ou retirer des bonus à un personnage
    dans un domaine précis (par exemple, augmenter son agilité pendant
    10 minutes).

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.donner_bonus, "Personnage", "str",
                "Fraction")
        cls.ajouter_types(cls.donner_bonus_perso, "Personnage", "str",
                "Fraction", "Fraction")
        cls.ajouter_types(cls.donner_bonus_salle, "Salle", "str",
                "Fraction", "Fraction")

    @staticmethod
    def donner_bonus(personnage, nom_stat, points):
        """Donne ou retire un bonus dans la stat indiquée.

        Les paramètres à préciser sont :

          * personnage : le personnage ciblé par le bonus
          * nom_stat : le nom de la stat (par exemple "force")
          * points : le nombre de points à ajouter ou retirer.

        NOTE IMPORTANTE : cette action modifie la partie variable
        de la stat du personnage. Concrètement, cela signifie que vous
        devez l'appeler deux fois : une fois pour donner le bonus, une
        fois pour le retirer. Retirer le bonus se fait en spécifiant un
        nombre négatif de points. Par exemple, si vous voulez faire
        une affection qui donne 10 points de force, vous devrez faire
        comme ceci :

            donner_bonus personnage "force" 10

        Et quand l'affection se détruit:

            donner_bonus personnage "force" -10

        Dans le cas contraire le bonus sera maintenu éternellement.

        """
        nom_stat = supprimer_accents(nom_stat)
        points = int(points)
        variable = personnage.stats[nom_stat].variable
        personnage.stats[nom_stat].variable = variable + points

    @staticmethod
    def donner_bonus_perso(personnage, adresse, secondes, valeur):
        """Donne un bonus temporaire au personnage indiqué.

        Cette action permet de créer un bonus temporaire pour le personnage
        indiqué. La durée en secondes du bonus (un nombre) et la valeur
        du bonus (un autre nombre) doivent être précisés. L'expiration
        est géré automatiquement.

        Paramètres à préciser :

          * personnage : le personnage à modifier /
          * adresse : l'adresse de la modification (une chaîne) ;
          * secondes : le nombre de secondes du bonus (un nombre) ;
          * valeur : la valeur du bonus/malus (un nombre).

        Cette action permet de créer des bonus/malus temporaires pour
        plusieurs choses. Il faut donc préciser la nature de la modification.

        Adresses supportées :

          "temperature" : la température du personnage
          "talent nom_du_talent" : un talent du personnage
          "stat nom_de_la_stat" : une statistique du personnage (il faut renseigner le nom entier de la statistique)

        Exemple d'utilisation :

          # Fait un bonus de 10° pour le personnage, durant 5 minutes
          donner_bonus personnage "temperature" 300 10

        """
        adresse = supprimer_accents(adresse).lower()
        if adresse == "temperature":
            secondes = int(secondes)
            valeur = round(float(valeur), 1)
            importeur.bonus.ajouter((personnage, "temperature"), valeur,
                    secondes)
        elif adresse.startswith("talent "):
            secondes = int(secondes)
            valeur = round(float(valeur), 1)
            debut, sep, adresse = adresse.partition(" ")
            cle = None
            talent = None
            for t_talent in importeur.perso.talents.values():
                if supprimer_accents(t_talent.nom) == adresse:
                    talent = t_talent
                    cle = talent.cle
                    break
            if talent is None:
                raise ErreurExecution("talent inconnu : {}".format(repr(adresse)))
            importeur.bonus.ajouter((personnage, "talent", cle), valeur, secondes)
        elif adresse.startswith("stat "):
            secondes = int(secondes)
            valeur = round(float(valeur), 1)
            debut, sep, adresse = adresse.partition(" ")
            importeur.bonus.ajouter((personnage, "stat", adresse), valeur, secondes)
        else:
            raise ErreurExecution("adresse '{}' introuvable.".format(
                    adresse))

    @staticmethod
    def donner_bonus_salle(salle, adresse, secondes, valeur):
        """Donne un bonus temporaire à la salle indiquée.

        Cette action permet de créer un bonus temporaire dans la salle
        indiqué. La durée en secondes du bonus (un nombre) et la valeur
        du bonus (un autre nombre) doivent être précisés. L'expiration
        est géré automatiquement.

        Paramètres à préciser :

          * salle : la salle à modifier ;
          * adresse : l'adresse de la modification (une chaîne) ;
          * secondes : le nombre de secondes du bonus (un nombre) ;
          * valeur : la valeur du bonus/malus (un nombre).

        Cette action permet de créer des bonus/malus temporaires pour
        plusieurs choses. Il faut donc préciser la nature de la modification.

        Adresses supportées :

          "temperature" : la température de la salle.

        Exemple d'utilisation :

          # Fait un bonus de 10° dans la salle, durant 5 minutes
          donner_bonus salle "temperature" 300 10

        """
        adresse = supprimer_accents(adresse).lower()
        if adresse == "temperature":
            secondes = int(secondes)
            valeur = round(float(valeur), 1)
            importeur.bonus.ajouter((salle, "temperature"), valeur, secondes)
        else:
            raise ErreurExecution("adresse '{}' introuvable.".format(
                    adresse))
