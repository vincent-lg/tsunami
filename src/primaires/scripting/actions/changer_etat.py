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


"""Fichier contenant l'action changer_etat."""

from primaires.scripting.action import Action

class ClasseAction(Action):

    """Modifie l'état singulier et pluriel d'un PNJ.

    Cette action modifie l'état singulier et pluriel d'un PNJ. L'état
    singulier et pluriel par défaut (celui défini dans le prototype)
    est temporérement modifié. Utilisez l'action en ne précisant
    que le PNJ pour remettre l'état par défaut du prototype.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.remettre_etat, "PNJ")
        cls.ajouter_types(cls.changer_etat, "PNJ", "str", "str")

    @staticmethod
    def remettre_etat(pnj):
        """Remet l'état singulier et pluriel à leur valeur par défaut.

        Paramètres à préciser :

          * pnj : la variable contenant le PNJ.

        Les états (singulier et pluriel) du prototype de PNJ seront
        remis à leur valeur précisée par défaut.

        """
        try:
            del pnj.etat_singulier
        except AttributeError:
            pass

        try:
            del pnj.etat_pluriel
        except AttributeError:
            pass

    @staticmethod
    def changer_etat(pnj, etat_singulier, etat_pluriel):
        """Change l'état singulier et pluriel d'un PNJ.

        Paramètres à préciser :

          * pnj : la variable contenant le PNJ
          * etat_singulier : le nouvel état singulier
          * etat_pluriel : le nouvel état pluriel.

        Exemple d'utilisation :

          changer_etat pnj "est assis là" "sont assis là"

        L'état pluriel est nécessaire si plusieurs PNJ ont le même
        état singulier. Si par exemple vous définissez plusieurs PNJ
        sur le même prototype et que vous modifiez l'état singulier
        de plusieurs, alors l'état pluriel personnalisé (si il existe)
        sera appliqué.

        Vous pouvez préciser une chaîne vide en état pluriel mais
        ceci n'est pas conseillé. Faites-le si vous êtes absolument
        sûr qu'il n'y aura qu'un seul PNJ de ce prototype en jeu.

        """
        pnj.etat_singulier = etat_singulier
        if etat_pluriel:
            pnj.etat_pluriel = etat_pluriel
