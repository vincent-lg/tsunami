# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant l'action changer_nom."""

from primaires.scripting.action import Action

class ClasseAction(Action):

    """Modifie le nom singulier et pluriel d'un PNJ.

    Cette action modifie le nom singulier et pluriel d'un PNJ. le nom
    singulier et pluriel par défaut (celui défini dans le prototype)
    est temporérement modifié. Utilisez l'action en ne précisant
    que le PNJ pour remettre le nom par défaut du prototype.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.remettre_nom, "PNJ")
        cls.ajouter_types(cls.changer_nom, "PNJ", "str", "str")

    @staticmethod
    def remettre_nom(pnj):
        """Remet le nom singulier et pluriel à leur valeur par défaut.

        Paramètres à préciser :

          * pnj : la variable contenant le PNJ.

        Les noms (singulier et pluriel) du prototype de PNJ seront
        remis à leur valeur précisée par défaut.

        """
        try:
            del pnj.nom_singulier
        except AttributeError:
            pass

        try:
            del pnj.nom_pluriel
        except AttributeError:
            pass

    @staticmethod
    def changer_nom(pnj, nom_singulier, nom_pluriel):
        """Change le nom singulier et pluriel d'un PNJ.

        Paramètres à préciser :

          * pnj : la variable contenant le PNJ
          * nom_singulier : le nouveau nom singulier
          * nom_pluriel : le nouveau nom pluriel.

        Exemple d'utilisation :

          changer_nom pnj "un gigantesque lézard" "gigantesques lézards"

        Le nom pluriel est nécessaire si plusieurs PNJ ont le même
        nom singulier. Si par exemple vous définissez plusieurs PNJ
        sur le même prototype et que vous modifiez le nom singulier
        de plusieurs, alors le nom pluriel personnalisé (si il existe)
        sera appliqué.

        Vous pouvez préciser une chaîne vide en nom pluriel mais
        ceci n'est pas conseillé. Faites-le si vous êtes absolument
        sûr qu'il n'y aura qu'un seul PNJ de ce prototype en jeu.

        """
        pnj.nom_singulier = nom_singulier
        if nom_pluriel:
            pnj.nom_pluriel = nom_pluriel
