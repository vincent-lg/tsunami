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
# LIABLE FOR ANY teleporterCT, INteleporterCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action effacer_memoire."""

import re
from fractions import Fraction

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

# Constantes
RE_TEMPS = re.compile(r"^[0-9]+[mhjs]$")

class ClasseAction(Action):

    """Efface ou programme l'effacement d'une mémoire de scripting."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.effacer_salle, "Salle", "str")
        cls.ajouter_types(cls.effacer_perso, "Personnage", "str")
        cls.ajouter_types(cls.effacer_objet, "Objet", "str")
        cls.ajouter_types(cls.effacer_salle, "Salle", "str", "Fraction")
        cls.ajouter_types(cls.effacer_perso, "Personnage", "str", "Fraction")
        cls.ajouter_types(cls.effacer_objet, "Objet", "str", "Fraction")
        cls.ajouter_types(cls.effacer_salle, "Salle", "str", "str")
        cls.ajouter_types(cls.effacer_perso, "Personnage", "str", "str")
        cls.ajouter_types(cls.effacer_objet, "Objet", "str", "str")

    @staticmethod
    def effacer_salle(salle, cle, temps=0):
        """Efface une mémoire de salle.

        Paramètres à préciser :

          * salle : la salle dont on veut supprimer la mémoire
          * cle : la clé de la mémoire à effacer
          * temps (optionnel) : permet de programmer la suppression.

        Si un temps est précisé, la mémoire n'est pas effacée tout de suite
        mais sa suppression est programmée. Il est ainsi possible d'avoir des
        mémoires temporaires, devant exister 5 minutes par exemple.

        Le temps peut être précisé :

          * Sous la forme d'un nombre (le nombre de minutes à attendre) ;
          * Sous la forme d'une chaîne (détail plus bas).

        La chaîne doit contenir un nombre suivi d'une lettre. Les lettres sont
        s pour un nombre de secondes, m pour un nombre de minutes, h
        pour les heures et j pour les jours.

        Par exemple :

          * "3s" signifie supprimer la mémoire dans 3 secondes ;
          * "12h" signifie "supprimer la mémoire dans 12 heures" ;
          * "5j" signifie "supprimer la mémoire dans 5 jours" ;
          * "38m" est équivalent à 38. (38 minutes)

        Exemples d'utilisation :

          # Supprime immédiatement la mémoire "createur" de la salle
          effacer_memoire salle "createur"
          # Supprime la mémoire dans 8 secondes
          effacer_memoire salle "createur" "8s"
          # Supprime la mémoire dans 30 minutes
          effacer_memoire salle "createur" 30
          # Équivaut à
          effacer_memoire salle "createur" "30m"

        """
        temps = temps_en_secondes(temps)
        if temps:
            try:
                importeur.scripting.memoires.programmer_destruction(
                        salle, cle, temps)
            except ValueError as err:
                raise ErreurExecution(str(err))
            return

        if salle in importeur.scripting.memoires:
            if cle in importeur.scripting.memoires[salle]:
                del importeur.scripting.memoires[salle][cle]
                importeur.scripting.memoires.nettoyer_memoire(salle, cle)
            else:
                raise ErreurExecution("la mémoire {}:{} n'existe pas".format(
                        salle, cle))
            if not importeur.scripting.memoires[salle]:
                del importeur.scripting.memoires[salle]
        else:
            raise ErreurExecution("pas de mémoire pour {}".format(salle))

    @staticmethod
    def effacer_perso(personnage, cle, temps=0):
        """Efface une mémoire de personnage.

        Paramètres à préciser :

          * personnage : le personnage dont on veut supprimer la mémoire
          * cle : la clé de la mémoire à effacer
          * temps (optionnel) : permet de programmer la suppression.

        Si un temps est précisé, la mémoire n'est pas effacée tout de suite
        mais sa suppression est programmée. Il est ainsi possible d'avoir des
        mémoires temporaires, devant exister 5 minutes par exemple.

        Le temps peut être précisé :

          * Sous la forme d'un nombre (le nombre de minutes à attendre) ;
          * Sous la forme d'une chaîne (détail plus bas).

        La chaîne doit contenir un nombre suivi d'une lettre. Les lettres sont
        s pour un nombre de secondes, m pour un nombre de minutes, h
        pour les heures et j pour les jours.

        Par exemple :

          * "3s" signifie supprimer la mémoire dans 3 secondes ;
          * "12h" signifie "supprimer la mémoire dans 12 heures" ;
          * "5j" signifie "supprimer la mémoire dans 5 jours" ;
          * "38m" est équivalent à 38. (38 minutes)

        Exemples d'utilisation :

          # Supprime immédiatement la mémoire "createur" du personnage
          effacer_memoire personnage "createur"
          # Supprime la mémoire dans 8 secondes
          effacer_memoire personnage "createur" "8s"
          # Supprime la mémoire dans 30 minutes
          effacer_memoire personnage "createur" 30
          # Équivaut à
          effacer_memoire personnage "createur" "30m"

        """
        personnage = hasattr(personnage, "prototype") and \
                personnage.prototype or personnage
        temps = temps_en_secondes(temps)
        if temps:
            try:
                importeur.scripting.memoires.programmer_destruction(
                        personnage, cle, temps)
            except ValueError as err:
                raise ErreurExecution(str(err))
            return

        if personnage in importeur.scripting.memoires:
            if cle in importeur.scripting.memoires[personnage]:
                del importeur.scripting.memoires[personnage][cle]
            else:
                raise ErreurExecution("la mémoire {}:{} n'existe pas".format(
                        personnage, cle))
            if not importeur.scripting.memoires[personnage]:
                del importeur.scripting.memoires[personnage]
                importeur.scripting.memoires.nettoyer_memoire(personnage,
                        cle)
        else:
            raise ErreurExecution("pas de mémoire pour {}".format(personnage))

    @staticmethod
    def effacer_objet(objet, cle, temps=0):
        """Efface une mémoire d'objet.

        Paramètres à préciser :

          * objet : l'objet dont on veut supprimer la mémoire
          * cle : la clé de la mémoire à effacer
          * temps (optionnel) : permet de programmer la suppression.

        Si un temps est précisé, la mémoire n'est pas effacée tout de suite
        mais sa suppression est programmée. Il est ainsi possible d'avoir des
        mémoires temporaires, devant exister 5 minutes par exemple.

        Le temps peut être précisé :

          * Sous la forme d'un nombre (le nombre de minutes à attendre) ;
          * Sous la forme d'une chaîne (détail plus bas).

        La chaîne doit contenir un nombre suivi d'une lettre. Les lettres sont
        s pour un nombre de secondes, m pour un nombre de minutes, h
        pour les heures et j pour les jours.

        Par exemple :

          * "3s" signifie supprimer la mémoire dans 3 secondes ;
          * "12h" signifie "supprimer la mémoire dans 12 heures" ;
          * "5j" signifie "supprimer la mémoire dans 5 jours" ;
          * "38m" est équivalent à 38. (38 minutes)

        Exemples d'utilisation :

          # Supprime immédiatement la mémoire "createur" de l'objet
          effacer_memoire objet "createur"
          # Supprime la mémoire dans 8 secondes
          effacer_memoire objet "createur" "8s"
          # Supprime la mémoire dans 30 minutes
          effacer_memoire objet "createur" 30
          # Équivaut à
          effacer_memoire objet "createur" "30m"

        """
        temps = temps_en_secondes(temps)
        if temps:
            try:
                importeur.scripting.memoires.programmer_destruction(
                        objet, cle, temps)
            except ValueError as err:
                raise ErreurExecution(str(err))
            return

        if objet in importeur.scripting.memoires:
            if cle in importeur.scripting.memoires[objet]:
                del importeur.scripting.memoires[objet][cle]
                importeur.scripting.memoires.nettoyer_memoire(objet, cle)
            else:
                raise ErreurExecution("la mémoire {}:{} n'existe pas".format(
                        objet, cle))
            if not importeur.scripting.memoires[objet]:
                del importeur.scripting.memoires[objet]
        else:
            raise ErreurExecution("pas de mémoire pour {}".format(objet))

def temps_en_secondes(temps):
    """Retourne le temps en secondes."""
    if isinstance(temps, (Fraction, int)):
        return int(temps) * 60
    elif isinstance(temps, str):
        if not RE_TEMPS.search(temps):
            raise ErreurExecution("syntaxe de temps invalide")

        mul = temps[-1]
        temps = temps[:-1]
        try:
            temps = int(temps)
        except ValueError:
            raise ErreurExecution("temps invalide")

        if mul == "h":
            temps *= 60 * 60
        elif mul == "j":
            temps *= 60 * 60 * 24
        elif mul == "m":
            temps *= 60

        return temps
    else:
        raise ValueError("type de temps invalide")
