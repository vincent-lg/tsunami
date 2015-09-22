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

from bases.objet.attribut import Attribut
from corps.aleatoire import *
from corps.fonctions import lisser
from primaires.interpreteur.editeur.choix import Choix
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.entier import Entier
from .base import BaseType

# Constante
LISTE_CONNECTEURS = {
        "de": [
            "de {liquide} presque vide{s}",
            "de {liquide} à moitié plein{e}{s}",
            "plein{e}{s} de {liquide}",
        ],
        "rempli{s} de": [
            "presque vide{s} de {liquide}",
            "de {liquide} à moitié rempli{s}",
            "rempli{s} de {liquide}",
        ],
        "remplie{s} de": [
            "presque vide{s} de {liquide}",
            "de {liquide} à moitié remplie{s}",
            "remplie{s} de {liquide}",
        ],
        "plein{s} de": [
            "presque vide{s} de {liquide}",
            "de {liquide} à moitié plein{s}",
            "plein{s} de {liquide}",
        ],
        "pleine{s} de": [
            "presque vide{s} de {liquide}",
            "de {liquide} à moitié pleine{s}",
            "pleine{s} de {liquide}",
        ],
}

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
        self.masculin = True
        self.onces_max = 1
        
        # Extensions d'éditeur
        self.etendre_editeur("c", "connecteur", Choix, self,
                "connecteur", LISTE_CONNECTEURS)
        self.etendre_editeur("on", "nombre d'onces au maximum", Entier,
                self, "onces_max")
        self.etendre_editeur("ma", "genre masculin", Flag, self, "masculin")

        # Attributs
        self._attributs = {
            "onces": Attribut(lambda: self.onces_max),
        }
        
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
        
        contenu = enveloppes["on"]
        contenu.apercu = "{valeur}"
        contenu.prompt = "Nombre maximum d'onces que peut contenir l'objet : "
        contenu.aide_courte = \
            "Entrez le |ent|contenu|ff| en onces " \
            "du conteneur de potion\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Il suffit de savoir qu'une once peut être bue en une " \
            "longue gorgée\npour les joueurs. Remplacez donc once par " \
            "gorgée si c'est plus simple.\n\n" \
            "Onces maximum actuelles : {valeur}"

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
            connecteurs = LISTE_CONNECTEURS[self.connecteur]
            nb_max = self.onces_max
            nb = getattr(self, "onces", nb_max)
            rempli = nb / nb_max
            if rempli <= 0.2:
                connecteur = connecteurs[0]
            elif rempli <= 0.7:
                connecteur = connecteurs[1]
            else:
                connecteur = connecteurs[2]
                
            e = "e" if not self.masculin else ""
            ajout = lisser(" " + connecteur.format(s=s, e=e, liquide=nom))
            
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

    def est_plein(self):
        """Retourne True si le conteneur de potion est plein."""
        nb_max = self.onces_max
        return getattr(self, "onces", nb_max) == nb_max

    def est_vide(self):
        """Retourne True si le conteneur de potion est vide."""
        nb_max = self.onces_max
        return getattr(self, "onces", nb_max) == 0

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
        from primaires.perso.personnage import Personnage
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
