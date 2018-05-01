# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant l'action equiper."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Fait équiper un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.equiper_prototype, "Personnage", "str")
        cls.ajouter_types(cls.equiper_objet, "Personnage", "Objet")

    @staticmethod
    def equiper_prototype(personnage, cle_prototype):
        """Fait équiper un objet à un personnage.

        Paramètres à préciser :

          * personnage : le personnage qui doit s'équiper
          * cle_prototype : la clé du prototype d'objet à équiper

        Exemple d'utilisation :

          equiper personnage "sabre_bois"

        Le personnage n'a pas besoin d'avoir l'objet indiqué dans
        son inventaire : il sera dans tous les cas créé. En outre,
        cette action ne vérifie pas que le joueur peut s'équiper
        à cet emplacement (utilisez la fonction 'peut_equiper' pour
        vérifier cela).

        """
        if not cle_prototype in importeur.objet.prototypes:
            raise ErreurExecution("prototype d'objet {} introuvable".format(
                    repr(cle_prototype)))

        prototype = importeur.objet.prototypes[cle_prototype]
        objet = importeur.objet.creer_objet(prototype)
        for membre in personnage.equipement.membres:
            if membre.peut_equiper(objet):
                membre.equiper(objet)
                return

        raise ErreurExecution("le personnage {} ne peut équiper {}".format(
                repr(personnage), repr(objet.cle)))

    @staticmethod
    def equiper_objet(personnage, objet):
        """Force un personnage à équiper l'objet précisé.

        Cette syntaxe de l'action se rapproche davantage de la commande
        **porter/wear**. Elle demande à un personnage d'équiper un
        objet qu'il possède (dans ses mains, ou dans un sac qu'il équipe).

        Paramètres à préciser :

          * personnage : le personnage que l'on souhaite équiper
          * objet : l'objet que l'on souhaite équiper.

        Cette action est susceptible de faire des erreurs, par exemple,
        si l'objet n'est pas possédé par le personnage ou si il ne
        peut être équipé par le personnage. Il est de bonne politique
        de tester avant d'équiper le personnage, sauf si on est dans
        une situation extrêmement limitée en aléatoire.

        Exemple d'utilisation :

          # On cherche à faire équiper un sabre de bois au personnage
          # Le personnage possède le sabre de bois dans son inventaire
          sabre = possede(personnage, "sabre_bois")
          si sabre:
              # On vérifié qu'il n'a rien dans la main gauche
              si !equipe(personnage, "*main gauche"):
                  equiper personnage sabre
              finsi
          finsi

        """
        if not any(o for o in personnage.equipement.inventaire if o is objet):
            raise ErreurExecution("{} ne possède visiblement pas {}".format(
                    personnage.nom_unique, objet.identifiant))
        # Si 'objet' est déjà équipé, ne fait rien
        if objet.contenu is personnage.equipement.equipes:
            return

        # Essaye d'équiper l'objet sur un membre
        for membre in personnage.equipement.membres:
            if membre.peut_equiper(objet):
                objet.contenu.retirer(objet)
                membre.equiper(objet)
                objet.script["porte"].executer(objet=objet,
                        personnage=personnage)
                return

        raise ErreurExecution("{} ne peut équiper {}, aucun emplacement " \
                "libre".format(personnage.nom_unique, objet.identifiant))
