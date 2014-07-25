# -*-coding:Utf-8 -*

# Copyright (c) 2012 EILERS Christoff
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


"""Fichier contenant le type ConteneurPotion."""

from corps.aleatoire import *
from corps.fonctions import lisser
from primaires.interpreteur.editeur.choix import Choix
from primaires.perso.personnage import Personnage
from .base import BaseType

# Constante
LISTE_CONNECTEURS = [
        "de",
        "rempli{s} de",
        "remplie{s} de",
        "plein{s} de",
        "pleine{s} de",
]

class ConteneurPotion(BaseType):

    """Type d'objet: conteneur de potion.

    Les conteneurs de potion(s) sont des conteneurs spéciaux comme des verres, bouteilles, tonneaux...

    """

    nom_type = "conteneur de potion"

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.potion = None
        self.connecteur = "de"
        self.etendre_editeur("c", "connecteur", Choix, self,
                "connecteur", LISTE_CONNECTEURS)

        # Erreur de validation du type
        self.err_type = "Laissez ce liquide à sa place, non mais."

    @property
    def connecteurs(self):
        """Retourne la liste des suffixes possibles."""
        return ", ".join(LISTE_CONNECTEURS)

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes."""
        connecteur = enveloppes["c"]
        connecteur.apercu = "{objet.connecteur}"
        connecteur.aide_courte = \
            "Choisissez un |ent|connecteur|ff| ou entrez |cmd|/|ff| pour " \
            "revenir à la fenêtre parente.\nLe connecteur sera utilisé pour " \
            "afficher le contenu de cet objet, par exemple :\n" \
            "|grf|un tonneau|ff| |bc|plein de|ff| |grf|bière|ff|.\n\n" \
            "Choix possibles : {objet.connecteurs}\n\n" \
            "Connecteur actuel : {objet.connecteur}"

    # Actions sur les objets
    def get_nom(self, nombre=1, pluriels=True):
        """Retourne le nom complet en fonction du nombre.

        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel

        """
        ajout = ""
        if self.potion is not None:
            s = "s" if nombre > 1 else ""
            nom = self.potion.get_nom()
            ajout = lisser(" " + self.connecteur.format(s=s) + " " + nom)
        if nombre <= 0:
            raise ValueError("la fonction get_nom a été appelée " \
                    "avec un nombre négatif ou nul.")
        elif nombre == 1:
            return self.nom_singulier + ajout
        else:
            if self.noms_sup:
                noms_sup = list(self.noms_sup)
                noms_sup.reverse()
                for nom in noms_sup:
                    if nombre >= nom[0]:
                        return nom[1] + ajout
            return str(nombre) + " " + self.nom_pluriel + ajout

    def objets_contenus(self, conteneur):
        """Retourne les objets contenus."""
        objets = []
        if hasattr(conteneur, "potion") and conteneur.potion:
            objet = conteneur.potion
            objets.append(objet)
            if objet.unique:
                objets.extend(objet.prototype.objets_contenus(objet))

        return objets

    def detruire_objet(self, conteneur):
        """Détruit l'objet passé en paramètre.

        On va détruire tout ce qu'il contient.

        """
        if hasattr(conteneur, "potion") and conteneur.potion:
            objet = conteneur.potion
            if objet.unique and objet.e_existe:
                importeur.objet.essayer_supprimer_objet(objet)

    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        msg = BaseType.regarder(self, personnage)
        if getattr(self, "potion", False):
            msg += str(self.potion.description)

        return msg

    def veut_jeter(self, personnage, sur):
        """Le personnage veut jeter l'objet sur sur."""
        if not isinstance(sur, Personnage):
            return ""

        return "jeter_personnage"

    def jeter(self, personnage, elt):
        """Jète la nourriture sur un élément."""
        fact = varier(personnage.agilite, 20) / 100
        fact *= (1.6 - personnage.poids / personnage.poids_max)
        fact_adv = varier(elt.agilite, 20) / 100
        fact_adv *= (1.6 - elt.poids / elt.poids_max)
        reussite = fact >= fact_adv
        if reussite:
            personnage.envoyer("Vous lancez {} sur {{}}.".format(
                    self.get_nom()), elt)
            elt.envoyer("{{}} lance {} droit sur vous.".format(
                    self.get_nom()), personnage)
            personnage.salle.envoyer("{{}} envoie {} sur {{}}.".format(
                    self.get_nom()), personnage, elt)
        else:
            personnage.envoyer("Vous lancez {} mais manquez {{}}.".format(
                    self.get_nom()), elt)
            elt.envoyer("{{}} lance {} mais vous manque.".format(
                    self.get_nom()), personnage)
            personnage.salle.envoyer("{{}} envoie {} mais manque {{}}.".format(
                    self.get_nom()), personnage, elt)

        personnage.salle.objets_sol.ajouter(self)
        return reussite

    def jeter_personnage(self, personnage, cible):
        """Jète la nourriture sur un personnage."""
        personnage.salle.envoyer("{} tombe au sol et se renverse.".format(
                self.get_nom().capitalize()))
        self.potion = None
