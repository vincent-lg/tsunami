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


"""Fichier contenant l'action appliquer."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Applique une structure sur l'univers."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.appliquer_personnage, "Personnage", "Structure")
        cls.ajouter_types(cls.appliquer_salle, "Salle", "Structure")
        cls.ajouter_types(cls.appliquer_objet, "Objet", "Structure")

    @staticmethod
    def appliquer_salle(salle, structure):
        """Applique la structure spécifiée sur la salle.

        Cette action est utile pour apporter des modifications à une
        salle grâce aux structures. Voir les exemples plus bas pour une
        démonstration de leur utilité.

        Paramètres à entrer :

          * salle : la salle que l'on veut modifier ;
          * structure : la structure à appliquer sur la salle.

        La structure peut contenir toutes les informations d'une
        salle (son titre, sa description, ses sorties, ses flags...). Si
        la structure n'est pas si complète, seules les informations
        précisées sont utilisées. Cette action peut générer des
        alertes si la structure n'est pas du bon format, ou bien dans
        certains autres cas particuliers. Par exemple, si vous souhaitez
        modifier le terrain d'une salle mais précdisez un terrain
        invalide, une alerte sera créée pour en rendre compte.

        Exemples d'utilisation :

          # Récupère la structure de la salle
          structure = structure(salle)
          # Met la salle en illuminée
          ecrire structure "illuminee" 1
          # Applique les modifications
          appliquer salle structure

        """
        salle.appliquer_structure(structure)

    @staticmethod
    def appliquer_personnage(personnage, structure):
        """Applique la structure spécifiée sur le personnage.

        Cette action est utile pour apporter des modifications à un
        personnage grâce aux structures. Voir les exemples plus bas
        pour une démonstration de leur utilité.

        Paramètres à entrer :

          * personnage : le personnage que l'on veut modifier ;
          * structure : la structure à appliquer sur le personnage.

        La structure peut contenir toutes les informations d'un
        personnage joueur on PNJ (son nom, sa race, son niveau, ...). Si
        la structure n'est pas si complète, seules les informations
        précisées sont utilisées. Cette action peut générer des
        alertes si la structure n'est pas du bon format, ou bien dans
        certains autres cas particuliers. Par exemple, si vous souhaitez
        modifier le nom d'un joueur, mais que ce nom est déjà utilisé,
        une alerte sera générée.

        Exemples d'utilisation :

          # Récupère la structure du personnage
          structure = structure(personnage)
          # Désactive le flag PK du personnage
          ecrire structure "pk" 0
          # Applique les modifications
          appliquer personnage structure

        """
        personnage.appliquer_structure(structure)

    @staticmethod
    def appliquer_objet(objet, structure):
        """Applique la structure spécifiée sur l'objet.

        Cette action est utile pour apporter des modifications à un
        objet grâce aux structures. Voir les exemples plus bas pour une
        démonstration de leur utilité.

        Paramètres à entrer :

          * objet : l'objet que l'on veut modifier ;
          * structure : la structure à appliquer sur l'objet.

        La structure peut contenir toutes les informations d'un
        objet (ses noms, sa description, ses flags...). Si
        la structure n'est pas si complète, seules les informations
        précisées sont utilisées. Cette action peut générer des
        alertes si la structure n'est pas du bon format, ou bien dans
        certains autres cas particuliers.

        Exemples d'utilisation :

          # Récupère la structure de l'objet
          structure = structure(objet)
          # Met l'objet en invisible
          ecrire structure "visible" 0
          # Applique les modifications
          appliquer objet structure

        """
        objet.appliquer_structure(structure)
