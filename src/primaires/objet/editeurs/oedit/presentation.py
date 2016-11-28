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


"""Fichier contenant la classe EdtPresentation, détaillée plus bas.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.flags import Flags
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.interpreteur.editeur.entier import Entier
from primaires.objet.types.base import FLAGS
from primaires.scripting.editeurs.edt_script import EdtScript
from .edt_noms import EdtNoms
from .edt_emplacement import EdtEmplacement
from .supprimer import NSupprimer

class EdtPresentation(Presentation):

    """Classe définissant l'éditeur d'objet 'oedit'.

    """

    def __init__(self, personnage, prototype, attribut=""):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, prototype)
        if personnage and prototype:
            self.construire(prototype)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, prototype):
        """Construction de l'éditeur"""
        # Type (lecture seule)
        type = self.ajouter_choix("type", "type", Uniligne, prototype,
                "nom_type")
        type.parent = self
        type.apercu = "{valeur}"
        type.lecture_seule = True

        # Noms
        noms = self.ajouter_choix("noms", "n", EdtNoms, prototype)
        noms.parent = self
        noms.apercu = "{valeur}"

        # Description
        description = self.ajouter_choix("description", "d", Description,
                prototype, "description")
        description.parent = self
        description.apercu = "{valeur}"
        description.aide_courte = \
            "| |tit|" + "Description de l'objet {}".format(prototype).ljust(
            76) + "|ff||\n" + self.opts.separateur

        # Nettoyer
        nettoyer = self.ajouter_choix("à nettoyer", "net", Flag,
                prototype, "nettoyer")
        nettoyer.parent = self

        # Flags
        flags = self.ajouter_choix("flags", "fl", Flags, prototype, "flags",
                FLAGS)
        flags.parent = self
        flags.apercu = "{valeur}"
        flags.aide_courte = \
            "Flags d'objet de {} :".format(prototype.cle)

        # Emplacement
        emp = self.ajouter_choix("emplacement", "e", EdtEmplacement,
                prototype, "emplacement")
        emp.parent = self
        emp.apercu = "{objet.emplacement}"
        emp.prompt = "Entrez un emplacement (groupe ou membre) : "
        emp.aide_courte = \
            "Entrez l'emplacement de l'objet.\n" \
            "Cet emplacement peut être un nom de groupe (comme " \
            "|cmd|mains|ff|)\n" \
            "ou un nom de membre (comme |cmd|cou|ff|).\n\n" \
            "Vous pouvez également modifier l'épaisseur et les positions " \
            "de l'objet.\n" \
            "Les positions autorisées d'un objet indiquent à quelle " \
            "épaisseur il peut\n" \
            "être équipé. Par exemple, une chemise a généralement " \
            "une position de 1\n" \
            "(c'est-à-dire qu'on peut l'enfiler sans rien " \
            "au-dessous). Une armure a une\n" \
            "position plus importante (si elle est de 2, " \
            "par exemple, cela signifie qu'il\n" \
            "faut au moins un objet d'épaisseur 1 au-dessous, " \
            "pour pouvoir l'enfiler).\n" \
            "Généralement, un objet a plusieurs positions " \
            "(une armure peut être tout contre\n" \
            "la peau mais aussi recouvrir une ou deux " \
            "épaisseurs de vêtement.\n\n" \
            "Options disponibles :\n" \
            " |cmd|/e <épaisseur>|ff| pou changer l'épaisseur\n" \
            " |cmd|/p <position1, position2, ...>|ff| pour changer " \
            "les positions\n\n" \
            "Emplacement actuel : {objet.emplacement}\n" \
            "Epaisseur actuelle : {objet.epaisseur}"

        # Prix
        prix = self.ajouter_choix("prix", "p", Entier, prototype, "prix", 1)
        prix.parent = self
        prix.apercu = "{valeur}"
        prix.prompt = "Entrez un prix supérieur à 1 :"
        prix.aide_courte = \
            "Entrez la valeur de l'objet.\n\nValeur actuelle : {objet.prix}"

        # Poids
        poids = self.ajouter_choix("poids unitaire", "u", Flottant, prototype,
                "poids_unitaire")
        poids.parent = self
        poids.prompt = "Entrez le poids unitaire de l'objet : "
        poids.apercu = "{valeur} Kg"
        poids.aide_courte = \
            "Entrez le poids unitaire de l'objet.\n\nPoids actuel : " \
            "{objet.poids_unitaire}"

        # Protection contre le froid
        froid = self.ajouter_choix("protection contre le froid", "pr",
                Flottant, prototype, "protection_froid")
        froid.parent = self
        froid.prompt = "Entrez la protection au froid de l'objet : "
        froid.apercu = "{valeur}°"
        froid.aide_courte = \
            "Entrez la |ent|protection contre le froid|ff| de l'objet " \
            "ou |cmd|/|ff| pour revenir\nà la fenêtre parente.\n\n" \
            "Entrez la protection du froid en degrés. Vous pouvez " \
            "utiliser des nombres\nà virgule pour préciser |cmd|0,8|ff|° " \
            "par exemple.\n\nValeur actuelle : |bc|{valeur}|ff|"

        # Extensions
        for extension in prototype._extensions_editeur:
            rac, ligne, editeur, objet, attr, sup = extension
            env = self.ajouter_choix(ligne, rac, editeur, objet, attr, *sup)
            env.parent = self

        # Extensions de l'éditeur
        importeur.hook["editeur:etendre"].executer("objet", self, prototype)

        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                prototype.script)
        scripts.parent = self

        # Suppression
        suppression = self.ajouter_choix("supprimer", "sup", NSupprimer, \
                prototype)
        suppression.parent = self
        suppression.aide_courte = "Souhaitez-vous réellement supprimer " \
                "le prototype d'objet {} ?".format(prototype.cle)
        suppression.action = "objet.supprimer_prototype"
        suppression.confirme = "Le prototype d'objet {} a bien été " \
                "supprimé.".format(prototype.cle)

        # Travail sur les enveloppes
        # On appelle la méthode 'travailler_enveloppes' du prototype
        # Cette méthode peut travailler sur les enveloppes de la présentation
        # (écrire une aide courte, un aperçu...)
        enveloppes = {}
        for rac, nom in self.raccourcis.items():
            enveloppe = self.choix[nom]
            enveloppes[rac] = enveloppe

        prototype.travailler_enveloppes(enveloppes)

        if prototype.sans_prix:
            self.supprimer_choix("prix")
