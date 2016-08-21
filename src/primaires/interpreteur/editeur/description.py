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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur 'Description'."""

from primaires.format.description import Description as Desc
from primaires.format.fonctions import *
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from . import Editeur
from primaires.interpreteur.options import *

class Description(Editeur):

    """Contexte-éditeur description.

    Ce contexte sert à éditer des descriptions.

    """

    nom = "editeur:base:description"

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        attribut = attribut or "description"
        Editeur.__init__(self, pere, objet, attribut)
        self.opts.echp_sp_cars = False
        self.nom_attribut = attribut
        contenu = ""
        if objet:
            contenu = getattr(self.objet, self.nom_attribut)
            if contenu is None:
                setattr(self.objet, self.nom_attribut, "")
            else:
                contenu = str(contenu)

        self.description_complete = Desc(parent=objet, scriptable=False)
        if contenu:
            for paragraphe in contenu.split("\n"):
                self.description_complete.ajouter_paragraphe(
                        paragraphe.replace("|nl|", " "))

        self.ajouter_option("?", self.opt_aide)
        self.ajouter_option("j", self.opt_ajouter_paragraphe)
        self.ajouter_option("a", self.opt_inserer_paragraphe)
        self.ajouter_option("d", self.opt_supprimer)
        self.ajouter_option("r", self.opt_remplacer)
        self.ajouter_option("e", self.opt_editer_evt)
        self.ajouter_option("t", self.opt_tabulations)
        self.ajouter_option("de", self.opt_supprimer_evt)
        self.ajouter_option("re", self.opt_renommer_evt)
        self.ajouter_option("o", self.opt_editer_options)

    @property
    def description(self):
        """Retourne la description, attribut de self.objet"""
        attribut = getattr(self.objet, self.nom_attribut)
        if isinstance(attribut, str):
            return self.description_complete

        return attribut

    def get_prompt(self):
        """Retourne le prompt."""
        description = self.description
        personnage = self.pere.joueur
        options = importeur.interpreteur.options
        if not options.a_option(personnage, OPT_AUTONL) and not \
                description.saut_de_ligne:
            return "-? "
        else:
            return "-> "

    @staticmethod
    def afficher_apercu(apercu, objet, valeur):
        if valeur is None:
            return ""

        if isinstance(valeur, str):
            description = Desc(parent=objet, scriptable=False)

            for paragraphe in valeur.split("\n"):
                description.ajouter_paragraphe(
                        paragraphe.replace("|nl|", " "))

            valeur = description

        valeur = valeur.paragraphes_indentes
        return apercu.format(objet=objet, valeur=valeur)

    def mettre_a_jour(self):
        """Met à jour l'attribut si nécessaire."""
        attribut = getattr(self.objet, self.nom_attribut)
        if isinstance(attribut, str):
            contenu = self.description_complete.affichage_simple("|nl|")
            setattr(self.objet, self.nom_attribut, contenu)

    def accueil(self):
        """Retourne l'aide"""
        description = self.description

        # Message d'aide
        msg = self.aide_courte.format(objet = self.objet) + "\n"
        msg += "Entrez une |cmd|phrase|ff| à ajouter à la description " \
                "ou |ent|/|ff| pour revenir à la\nfenêtre mère.\n" \
                "Symboles :\n" \
                " - |ent||tab||ff| : symbolise une tabulation\n" \
                "Options :\n" \
                " - |ent|/?|ff| pour obtenir la liste complète " \
                "des options disponibles\n" \
                " - |ent|/d <numéro>/*|ff| : supprime un paragraphe ou " \
                "toute la description\n" \
                " - |ent|/r <texte 1> / <texte 2>|ff| : remplace " \
                "|cmd|texte 1|ff| par |cmd|texte 2|ff|\n" \
                "Pour ajouter un paragraphe, entrez-le tout simplement.\n\n" \
                "Description existante :\n"

        if len(description.paragraphes) > 0:
            no_ligne = 1
            for paragraphe in description.paragraphes:
                paragraphe = description.wrap_paragraphe(paragraphe,
                        aff_sp_cars=True)
                paragraphe = paragraphe.replace("\n", "\n   ")
                msg += "\n{: 2} {}".format(no_ligne, paragraphe)
                no_ligne += 1
        else:
            msg += "\n Aucune description."

        return msg

    def opt_aide(self, arguments):
        """Affiche la liste des options.

        Syntaxe :
          /?

        """
        msg = \
            "Liste des options disponibles :\n" \
            " - |ent|/d *|ff| pour supprimer toute la description\n" \
            " - |ent|/d <numéro du paragraphe>|ff| pour supprimer un " \
            "paragraphe\n" \
            " - |ent|/a <numéro du paragraphe> <texte>|ff| pour ajouter " \
            "du texte\n   à la fin du paragraphe spécifié\n" \
            " - |ent|/j <numéro du paragraphe> <texte>|ff| pour insérer " \
            "le\n   paragraphe avant celui spécifié\n" \
            " - |/r <texte 1> / <texte 2>|ff| pour remplacer " \
            "|ent|texte 1|ff| par |ent|texte 2|ff|\n" \
            " - |ent|/t|ff| pour ajouter ou retirer les tabulations"

        if self.description.scriptable:
            msg += \
                "\nScripting de description :\n" \
                " - |ent|/e (description dynamique)|ff| pour éditer un " \
                "élément de\n   description dynamique. Sans arguments, " \
                "affiche les descriptions dynamiques\n   existantes\n" \
                " - |ent|/de <description dynamique>|ff| supprime la " \
                "description dynamique\n" \
                " - |ent|/re <ancien nom> <nouveau nom>|ff| renomme la " \
                "description dynamique"

        self.pere << msg

    def opt_ajouter_paragraphe(self, arguments):
        """Ajoute un paragraphe.

        Syntaxe :
          /j <numéro> <texte>

        """
        description = self.description
        paragraphes = description.paragraphes
        arguments = arguments.split(" ")
        if len(arguments) < 2:
            self.pere << "|err|Syntaxe invalide :|ent|/a <numéro du " \
                    "paragraphe> <texte à insérer>|ff|"
            return

        numero = arguments[0]
        texte = " ".join(arguments[1:])

        # Conversion du numéro de paragraphe
        try:
            numero = int(numero)
            assert 1 <= numero <= len(paragraphes)
        except (ValueError, AssertionError):
            self.pere << "|err|Le numéro précisé est invalide.|ff|"
            return

        description.paragraphes.insert(numero - 1, texte)
        self.mettre_a_jour()
        self.actualiser()

    def opt_inserer_paragraphe(self, arguments):
        """Insère du texte à la fin d'un paragraphe.

        Syntaxe :
          /a <numéro> <texte>

        """
        description = self.description
        paragraphes = description.paragraphes
        arguments = arguments.split(" ")
        if len(arguments) < 2:
            self.pere << "|err|Syntaxe invalide :|ent|/a <numéro du " \
                    "paragraphe> <texte à insérer>|ff|"
            return

        numero = arguments[0]
        texte = " ".join(arguments[1:])

        # Conversion du numéro de paragraphe
        try:
            numero = int(numero)
            assert 1 <= numero <= len(paragraphes)
        except (ValueError, AssertionError):
            self.pere << "|err|Le numéro précisé est invalide.|ff|"
            return

        paragraphe = paragraphes[numero - 1]
        if not paragraphe.endswith(" "):
            paragraphe += " "
        paragraphe += texte
        description.paragraphes[numero - 1] = paragraphe
        self.mettre_a_jour()
        self.actualiser()

    def opt_supprimer(self, arguments):
        """Fonction appelé quand on souhaite supprimer un morceau de la
        description
        Les arguments peuvent être :
        *   le signe '*' pour supprimer toute la description
        *   un nombre pour supprimer le paragraphe n°<nombre>

        """
        description = self.description
        if arguments == "*": # on supprime toute la description
            description.vider()
            self.mettre_a_jour()
            self.actualiser()
        else:
            # Ce doit être un nombre
            try:
                no = int(arguments) - 1
                assert no >= 0 and no < len(description.paragraphes)
            except ValueError:
                self.pere << "|err|Numéro de ligne invalide.|ff|"
            except AssertionError:
                self.pere << "|err|Numéro de ligne inexistant.|ff|"
            else:
                description.supprimer_paragraphe(no)
                self.mettre_a_jour()
                self.actualiser()

    def opt_remplacer(self, arguments):
        """Fonction appelé pour remplacer du texte dans la description.

        La syntaxe de remplacement est :
        <texte 1> / <texte à remplacer>

        """
        description = self.description

        # On commence par split au niveau du pipe
        try:
            recherche, remplacer_par = arguments.split(" / ")
        except ValueError:
            self.pere << "|err|Syntaxe invalide.|ff|"
        else:
            description.remplacer(recherche, remplacer_par)
            self.mettre_a_jour()
            self.actualiser()

    def opt_tabulations(self, arguments):
        """Ajoute ou retire les tabulations d'une description.

        Syntaxe :
            /t

        """
        description = self.description

        # On parcourt tous les paragraphes
        for i, paragraphe in enumerate(description.paragraphes):
            if paragraphe.startswith("|tab|"):
                paragraphe = paragraphe[5:]
            else:
                paragraphe = "|tab|" + paragraphe
            description.paragraphes[i] = paragraphe

        self.mettre_a_jour()
        self.actualiser()

    def opt_editer_evt(self, arguments):
        """Edite ou affiche les éléments de la description."""
        description = self.description
        if not description.scriptable:
            self.pere << "|err|Option inconnue.|ff|"
            return

        evenements = description.script["regarde"].evenements
        evt = supprimer_accents(arguments).strip()
        if not evt:
            msg = \
                "Ci-dessous se trouve la liste des éléments observables " \
                "dans cette description :\n"
            for nom in sorted(evenements.keys()):
                msg += "\n  {}".format(nom)
            if not evenements:
                msg += "\n  |att|Aucun|ff|"
            self.pere << msg
        else:
            if evt in evenements.keys():
                evenement = evenements[evt]
            else:
                evenement = description.script["regarde"].creer_evenement(evt)
                description.script.init()
                evenement.creer_sinon()
            enveloppe = EnveloppeObjet(EdtInstructions, evenement.sinon)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere.joueur)

            self.migrer_contexte(contexte)

    def opt_supprimer_evt(self, arguments):
        """Supprime un évènement de la description dynamique.

        Syntaxe :
          /de <nom>

        """
        description = self.description
        if not description.scriptable:
            self.pere << "|err|Option inconnue.|ff|"
            return

        regarde = description.script["regarde"]
        evt = supprimer_accents(arguments).strip()
        if evt in regarde.evenements:
            regarde.supprimer_evenement(evt)
            self.actualiser()
        else:
            self.pere << "|err|Évènement inconnu : {}.|ff|".format(
                    repr(evt))

    def opt_renommer_evt(self, arguments):
        """Renomme un évènement de la description dynamique.

        Syntaxe :
          /de <nom> <nouveau nom>

        """
        description = self.description
        if not description.scriptable:
            self.pere << "|err|Option inconnue.|ff|"
            return

        regarde = description.script["regarde"]
        try:
            ancien, nouveau = arguments.split(" ")
        except ValueError:
            self.pere << "|err|Entrez l'ancien nom, un espace et le " \
                    "nouveau nom de variable.|ff|"
            return

        ancien = supprimer_accents(ancien).strip()
        if ancien in regarde.evenements:
            regarde.renommer_evenement(ancien, nouveau)
            self.actualiser()
        else:
            self.pere << "|err|Évènement inconnu : {}.|ff|".format(
                    repr(ancien))

    def opt_editer_options(self, arguments):
        """Fonction appelé pour consulter et éditer ses options.

        La syntaxe est :
            /o pour consulter ses options
            /o nom pour modifier ses options

        """
        arguments = arguments.strip()
        personnage = self.pere.joueur
        if arguments:
            options = importeur.interpreteur.options
            try:
                nombre = options.get_nombre_option(arguments)
            except ValueError:
                self.pere << "|err|Ce nom d'option est inconnu.|ff|"
            else:
                options.changer_option(personnage, nombre)
                self.pere << "Vos options ont bien été modifiées."
        else:
            # Affichage des options
            options = importeur.interpreteur.options.afficher_options(
                    personnage)
            self.pere << "Vos options actuelles :\n\n  " + "\n  ".join(
                    options)

    def interpreter(self, msg):
        """Interprétation du contexte"""
        description = self.description
        personnage = self.pere.joueur
        options = importeur.interpreteur.options
        if not options.a_option(personnage, OPT_AUTONL):
            if msg and not description.saut_de_ligne:
                if description.paragraphes:
                    paragraphe = description.paragraphes[-1]
                    msg = paragraphe + " " + msg
                    description.supprimer_paragraphe(-1)
            elif not msg:
                description.saut_de_ligne = True
                self.mettre_a_jour()
                self.actualiser()
                return
        elif options.a_option(personnage, OPT_AUTOTAB) and msg:
            msg = "|tab|" + msg
        description.ajouter_paragraphe(msg)
        description.saut_de_ligne = False
        self.mettre_a_jour()
        self.actualiser()

from primaires.scripting.editeurs.edt_instructions import EdtInstructions
