# -*-coding:Utf-8 -*

# Copyright (c) 2013 CORTIER Benoît
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


"""Package contenant l'éditeur 'descedit'."""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from .edt_annuler import EdtAnnuler
from .edt_envoyer import EdtEnvoyer


class EdtDescedit(Presentation):

    """Classe définissant l'éditeur de description 'descedit'.

    """

    nom = "descedit"

    def __init__(self, personnage, joueur):
        """Constructeur de l'éditeur

        joueur représente ici le même objet que personnage.

        """
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, joueur, None, False)
        if personnage and joueur:
            self.construire(personnage, joueur)

    def __getnewargs__(self):
        return (None, None)

    def accueil(self):
        """Message d'accueil du contexte"""
        msg = "| |tit|Edition de sa description|ff|".ljust(87) + "|\n"
        msg += self.opts.separateur + "\n\n"
        msg += " " \
            "Une description qui doit se faire à la troisième personne du " \
            "singulier (il a les yeux clairs ou elle est de stature semblant " \
            "vigoureuse...). Pas de mention d'équipement, de vêtement ou " \
            "ornements. Rien que de l'objectif, des informations que l'on peut " \
            "obtenir au premier regard.\n"

        # Parcours des choix possibles
        for nom, objet in self.choix.items():
            raccourci = self.get_raccourci_depuis_nom(nom)
            # On constitue le nom final
            # Si le nom d'origine est 'description' et le raccourci est 'd',
            # le nom final doit être '[D]escription'
            pos = nom.find(raccourci)
            raccourci = ((pos == 0) and raccourci.capitalize()) or raccourci
            nom_maj = nom.capitalize()
            nom_m = nom_maj[:pos] + "[|cmd|" + raccourci + "|ff|]" + \
                    nom_maj[pos + len(raccourci):]
            msg += "\n " + nom_m
            enveloppe = self.choix[nom]
            apercu = enveloppe.get_apercu()
            if apercu:
                msg += " : " + apercu

        return msg

    def construire(self, personnage, joueur):
        """Construction de l'éditeur"""
        # Description
        # Si le personnage (l'utilisateur qui édite) est immortel, on travaille
        # directement sur l'attribut description, sinon on utilise
        # description_a_valider.
        if personnage is joueur and personnage.est_immortel():
            description = self.ajouter_choix("description", "d", \
                    Description, joueur, "description")
            description.apercu = "{objet.description.paragraphes_indentes}"
        else:
            description = self.ajouter_choix("description", "d", \
                    Description, joueur, "description_a_valider")

            description.apercu = \
                    "{objet.description_a_valider.paragraphes_indentes}"

        description.parent = self
        description.aide_courte = "Modifier sa description."

        # Envoyer
        envoyer = self.ajouter_choix(
                "envoyer la description en validation", "e",
                EdtEnvoyer, joueur)
        envoyer.parent = self

        # Annuler
        annuler = self.ajouter_choix(
                "annuler et revenir à l'ancienne description", "ann",
                EdtAnnuler, joueur)
        annuler.parent = self
