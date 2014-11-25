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


"""Fichier contenant la classe EdtSalle, détaillée plus bas.

"""

from primaires.interpreteur.editeur.choix import Choix
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.salle.editeurs.redit.edt_details import EdtDetails
from primaires.interpreteur.editeur.selection import Selection
from secondaires.navigation.cale import CONTENEURS
from secondaires.navigation.equipage.postes.hierarchie import ORDRE
from secondaires.navigation.salle import NOMS_SORTIES

class EdtSalle(Presentation):

    """Classe définissant l'éditeur de salle de navire."""

    def __init__(self, personnage, salle, attribut=""):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, salle, "", False)
        self.ajouter_option("bab", self.opt_ajouter_babord)
        self.ajouter_option("tri", self.opt_ajouter_tribord)
        self.ajouter_option("ava", self.opt_ajouter_avant)
        self.ajouter_option("arr", self.opt_ajouter_arriere)
        self.ajouter_option("hau", self.opt_ajouter_haut)
        self.ajouter_option("bas", self.opt_ajouter_bas)
        self.ajouter_option("elt", self.opt_ajouter_supprimer_element)
        self.ajouter_option("s", self.opt_renommer_sortie)
        self.ajouter_option("p", self.opt_changer_porte)
        if personnage and salle:
            self.construire(salle)

    def __getnewargs__(self):
        return (None, None)

    def opt_ajouter_babord(self, arguments):
        """Ajoute une salle à bâbord.

        Syntaxe :
            /bab <mnémonic>

        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "ouest")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()

    def opt_ajouter_tribord(self, arguments):
        """Ajoute une salle à tribord.

        Syntaxe :
            /tri <mnémonic>

        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "est")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()

    def opt_ajouter_avant(self, arguments):
        """Ajoute une salle à l'avant.

        Syntaxe :
            /ava <mnémonic>

        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "nord")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()

    def opt_ajouter_arriere(self, arguments):
        """Ajoute une salle à l'arrière.

        Syntaxe :
            /arr <mnémonic>

        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "sud")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()

    def opt_ajouter_bas(self, arguments):
        """Ajoute une salle vers le bas.

        Syntaxe :
            /bas <mnémonic>

        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "bas")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()

    def opt_ajouter_haut(self, arguments):
        """Ajoute une salle vers le haut.

        Syntaxe :
            /hau <mnémonic>

        """
        salle = self.objet
        try:
            salle.modele.lier_salle(salle, arguments, "haut")
        except ValueError as err:
            self.pere << "|err|{}|ff|.".format(str(err).capitalize())
        else:
            self.actualiser()

    def opt_renommer_sortie(self, arguments):
        """Renomme une sortie dans la salle.

        Syntaxe :
            /s <direction> <nouveau nom>

        """
        salle = self.objet
        arguments = arguments.split(" ")
        direction = arguments[0].lower()
        nom = " ".join(arguments[1:])
        if not nom:
            self.pere << "|err|Syntaxe invalide. Entrez la direction, " \
                    "un espace et le nouveau nom de la sortie.|ff|"
            return

        try:
            sortie = salle.sorties.get_sortie_par_nom(direction)
        except KeyError:
            self.pere << "|err|Sortie {} introuvable.|ff|".format(
                    direction)
            return

        # Essaye de découper le nom
        if nom.count("'") == 1:
            article, nom = nom.split("'")
            article += "'"
        elif nom.count(" ") == 1:
            article, nom = nom.split(" ")
        else:
            self.pere << "|err|Syntaxe invalide. Vous devez préciser " \
                    "l'article et le nom (comme |ent|la cale|err|).|ff|"
            return

        try:
            salle.sorties.get_sortie_par_nom(nom.lower())
        except KeyError:
            pass
        else:
            self.pere << "|err|La sortie {} existe déjà.|ff|".format(nom)
            return

        sortie.nom = nom.lower()
        sortie.article = article.lower()
        self.actualiser()

    def construire(self, salle):
        """Construction de l'éditeur"""
        # Titre
        titre = self.ajouter_choix("titre", "t", Uniligne, salle, "titre")
        titre.parent = self
        titre.prompt = "Titre de la salle : "
        titre.apercu = "{objet.titre}"
        titre.aide_courte = \
            "Entrez le |ent|titre|ff| de la salle ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nTitre actuel : |bc|{objet.titre}|ff|"

        # Titre court
        court = self.ajouter_choix("titre court", "co", Uniligne, salle,
                "titre_court")
        court.parent = self
        court.prompt = "Titre court de la salle : "
        court.apercu = "{objet.titre_court}"
        court.aide_courte = \
            "Entrez le |ent|titre court|ff| de la salle ou |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nTitre court actuel : " \
            "|bc|{objet.titre_court}|ff|"

        # Description
        description = self.ajouter_choix("description", "d", Description, \
                salle)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description de la salle {}".format(salle).ljust(76) + \
            "|ff||\n" + self.opts.separateur

        # Détails
        details = self.ajouter_choix("details", "e", EdtDetails, salle,
                "details")
        details.parent = self
        details.aide_courte = \
            "Entrez le nom d'un |cmd|détail existant|ff| pour l'éditer ou " \
            "un |cmd|nouveau détail|ff|\n" \
            "pour le créer ; |ent|/|ff| pour revenir à la fenêtre parente.\n" \
            "Options :\n" \
            " - |ent|/s <détail existant> / <synonyme 1> (/ <synonyme 2> / " \
            "...)|ff| : permet\n" \
            "   de modifier les synonymes du détail passée en paramètre. " \
            "Pour chaque\n" \
            "   synonyme donné à l'option, s'il existe, il sera supprimé ; " \
            "sinon, il sera\n" \
            "   ajouté à la liste.\n" \
            " - |ent|/d <détail existant>|ff| : supprime le détail " \
            "indiqué\n\n"

        # Intérieur / extérieur
        inter = self.ajouter_choix("intérieur", "i", Flag, salle, "interieur")
        inter.parent = self

        # Noyable
        noyable = self.ajouter_choix("noyable", "n", Flag, salle, "noyable")
        noyable.parent = self

        # Poste
        poste = self.ajouter_choix("salle réservée au grade", "rad",
                Choix, salle, "poste", ORDRE)
        poste.parent = self
        poste.apercu = "{objet.poste}"
        poste.aide_courte = \
            "Entrez un |ent|grade|ff| pour réserver cette salle " \
            "\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nSi aucun grade n'est précisé, la salle est " \
            "ouverte à tous.\nNotez également qu'une salle réservée " \
            "doit avoir une porte.\n\n" \
            "Grades possibles : " + ", ".join(ORDRE) + "\n" \
            "Grade actuel : |bc|{objet.poste}|ff|"

        # Sabord minimum
        sabord_min = self.ajouter_choix("sabord", "b", Entier, salle,
                "sabord_min", -180, 180)
        sabord_min.parent = self
        sabord_min.prompt = "Sabord de la salle : "
        sabord_min.apercu = "{objet.sabord_min}°"
        sabord_min.aide_courte = \
            "Entrez le |ent|sabord|ff| de la salle ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nVous devez préciser le sabord " \
            "en degrés. Ceci est utile si la salle\ncomporte un canon " \
            "car il faut savoir dans quelle direction le canon doit\n" \
            "tirer. Le sabord est le centre (sélectionné par défaut) " \
            "du canon.\nVous devez préciser un nombre de degrés. Par " \
            "exemple, si la salle\na un sabord de 0°, cela signifie " \
            "que le canon tire droit devant. Si\nle sabord est de 90°, " \
            "cela signifie que le canon tire sur tribord\n(droit à " \
            "l'est si le navire face le nord, par exemple). L'angle " \
            "peut\nêtre négatif pour indiquer une direction bâbord " \
            ": -90° signifie que\nle canon tirera sur 90° bâbord. Notez " \
            "que si vous renseignez le sabord,\nvous devez aussi " \
            "renseigner la largeur du sabord qui indique de combien de\n" \
            "degrés le canon peut pivoter dans un sens ou dans l'autre.\n\n" \
            "Sabord actuel : |bc|{objet.sabord_min}°|ff|"

        # Sabord maximum
        sabord_max = self.ajouter_choix("largeur du sabord", "l", Entier,
                salle, "sabord_max", 0, 180)
        sabord_max.parent = self
        sabord_max.prompt = "Largeur du sabord de la salle : "
        sabord_max.apercu = "{objet.sabord_max}°"
        sabord_max.aide_courte = \
            "Entrez la |ent|largeur du sabord|ff| ou |cmd|/|ff| pour revenir " \
            "à la fenêtre parente.\n\nVous devez préciser la largeur " \
            "du sabord en degrés. Cette donnée indique\nde combien " \
            "de degrés le canon peut pivoter dans un sens ou dans l'autre\n" \
            "autour du sabord. Par exemple, si le sabord est de 0° " \
            "et que la largeur\ndu sabor est de 5°, le canon peut " \
            "pivoter de -5° (5° bâbord) jusqu'à\n5° (sur tribord). " \
            "Vous pouvez aussi faire un sabord qui s'ouvre sur\n-45° " \
            "(45° bâbord) avec une largeur de sabor de 10°, " \
            "c'est-à-dire que\nle canon pourra pivoter de 55° bâbord " \
            "à 35° bâbord.\n\nLargeur du sabord actuel : " \
            "|bc|{objet.sabord_max}°|ff|"

        # Cales
        cales = self.ajouter_choix("types de cale", "ca", Selection,
                salle, "cales", CONTENEURS)
        cales.parent = self
        cales.apercu = "{objet.str_cales}"
        cales.aide_courte = \
            "Entrez un |ent|nom de contenu|ff| pour la cale dans " \
            "cette salle\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nSi vous voulez supprimer un nom de contenu, " \
            "entrez son nom à nouveau.\n\nTypes possibles : " + ", ".join(
            CONTENEURS) + "\n\nTypes actuels : |bc|{objet.str_cales}|ff|"

    def opt_ajouter_supprimer_element(self, arguments):
        """Ajoute ou supprime un élément.

        Syntaxe :
            /elt <clé_élément>

        """
        salle = self.objet
        cle = arguments.strip()
        cles = tuple(e.nom_type for e in salle.mod_elements)
        types = tuple(e.nom_type for e in salle.elements)
        if cle in cles:
            salle.retirer_element(cle)
            self.actualiser()
        else:
            if cle not in type(self).importeur.navigation.elements:
                self.pere << "|err|Cet élément est introuvable.|ff|"
                return

            elt = type(self).importeur.navigation.elements[cle]
            if elt.nom_type in types:
                self.pere << "|err|Un élément de ce type est déjà présent " \
                        "dans cette salle.|ff|"
                return

            salle.ajouter_element(elt)
            self.actualiser()

    def opt_changer_porte(self, arguments):
        """Change le flag de la porte.

        Soit place une porte sur la sortie, soit la retire.

        Syntasxe :
            /p <direction>

        """
        salle = self.objet
        direction = arguments.lower()
        try:
            sortie = salle.sorties.get_sortie_par_nom(direction)
        except KeyError:
            self.pere << "|err|Sortie {} introuvable.|ff|".format(
                    direction)
            return

        if sortie.porte:
            sortie.supprimer_porte()
        else:
            sortie.ajouter_porte()

        self.actualiser()

    def accueil(self):
        """Message d'accueil de l'éditeur."""
        salle = self.objet
        msg = Presentation.accueil(self)
        msg += "\n"
        # Sorties
        msg += " Sorties :"
        for dir, nom in NOMS_SORTIES.items():
            sortie = salle.sorties[dir]
            if sortie:
                msg += "\n   {} vers {}".format(sortie.nom.capitalize(),
                        sortie.salle_dest.mnemonic)
                if sortie.porte:
                    msg += " (|att|fermée d'une porte|ff|)"
            else:
                msg += "\n   {}".format(nom.capitalize())

        msg += "\n"
        # Éléments
        msg += "\n Éléments de navire : " + ", ".join(
                e.cle for e in salle.mod_elements)
        if not salle.mod_elements:
            msg += "aucun"

        return msg
