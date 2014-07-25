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


"""Fichier contenant le type ConteneurNourriture."""

from math import ceil

from corps.aleatoire import *
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.objet.editeurs.edt_statuts import EdtStatuts
from primaires.perso.personnage import Personnage
from bases.objet.attribut import Attribut
from .base import BaseType

class ConteneurNourriture(BaseType):

    """Type d'objet: conteneur de nourriture.

    Les conteneurs de nourriture sont des conteneurs spéciaux genre assiette,
    bol, écuelle...

    """

    nom_type = "conteneur de nourriture"
    nettoyer = False

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.statuts = [
            (5, "à moitié plein"),
            (10, "rempli"),
        ]
        self.poids_max = 0.5
        self.etendre_editeur("m", "poids maximum", Flottant, self, "poids_max")
        self.etendre_editeur("s", "statuts", EdtStatuts, self, "statuts")

        # Attributs propres à l'objet (non au prototype)
        self._attributs = {
            "nourriture": Attribut(list),
        }

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes."""
        poids_max = enveloppes["m"]
        poids_max.apercu = "{objet.poids_max}"
        poids_max.prompt = "Poids maximum : "
        poids_max.aide_courte = \
            "Entrez le |ent|poids maximum|ff| que peut contenir cet objet " \
            "ou |cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Poids maximum actuel : {objet.poids_max}"

        statuts = enveloppes["s"]
        statuts.aide_courte = \
            "Entrez un |ent|ratio|ff| et un |ent|message|ff| à ajouter aux " \
            "statuts actuels, ou un |ent|ratio\nexistant|ff| et un " \
            "|ent|nouveau message|ff| pour modifier celui " \
            "existant. Ce ratio, sur 10,\ncorrespond au remplissage du " \
            "conteneur jusqu'auquel le message sera affiché\n(exemple : " \
            "|vr|5|ff| |bc|à moitié plein|ff| signifie qu'on affiche " \
            "|grf|un bol à moitié plein|ff|).\n" \
            "Option :\n" \
            " - |ent|/d <ratio>|ff| : supprime le statut précisé\n"

    def calculer_poids(self):
        """Retourne le poids de l'objet et celui des objets contenus."""
        poids = self.poids_unitaire
        if hasattr(self, "nourriture"):
            for objet in self.nourriture:
                poids += objet.poids

        return round(poids, 3)

    # Actions sur les objets
    def get_nom(self, nombre=1, pluriels=True):
        """Retourne le nom complet en fonction du nombre.

        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel

        """
        ajout = "vide"
        if hasattr(self, "nourriture") and self.nourriture:
            poids_contenu = sum([o.poids_unitaire for o in self.nourriture])
            ratio = ceil(10 * poids_contenu / self.poids_max)
            for r, message in self.statuts:
                if ratio <= r:
                    ajout = message
                    break
        if nombre <= 0:
            raise ValueError("la fonction get_nom a été appelée " \
                    "avec un nombre négatif ou nul.")
        elif nombre == 1:
            return self.nom_singulier + " " + ajout
        else:
            if self.noms_sup:
                noms_sup = list(self.noms_sup)
                noms_sup.reverse()
                for nom in noms_sup:
                    if nombre >= nom[0]:
                        return nom[1]
            return str(nombre) + " " + self.nom_pluriel + " " + ajout

    def objets_contenus(self, conteneur):
        """Retourne les objets contenus."""
        objets = []
        for objet in conteneur.nourriture:
            objets.append(objet)
            if objet.unique:
                objets.append(objet)
                objets.extend(objet.prototype.objets_contenus(objet))

        return objets

    def detruire_objet(self, conteneur):
        """Détruit l'objet passé en paramètre.

        On va détruire tout ce qu'il contient.

        """
        for objet in list(conteneur.nourriture):
            if conteneur is not objet and objet.unique and objet.e_existe:
                importeur.objet.essayer_supprimer_objet(objet)

    def peut_vendre(self, vendeur):
        """Retourne True si peut vendre, False sinon."""
        if hasattr(self, "nourriture") and self.nourriture:
            vendeur << "|err|{} n'est pas vide.|ff|".format(self.get_nom())
            return False

        return True

    def peut_vendre(self, vendeur):
        """Retourne True si peut vendre, False sinon."""
        if hasattr(self, "potion") and self.potion:
            vendeur << "|err|{} n'est pas vide.|ff|".format(self.get_nom())
            return False

        return True

    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        msg = BaseType.regarder(self, personnage)
        if not getattr(self, "nourriture", False):
            return msg

        dico_qtt = {}
        for item in self.nourriture:
            if item.prototype not in dico_qtt:
                dico_qtt[item.prototype] = 1
            else:
                dico_qtt[item.prototype] += 1

        if self.nourriture:
            nourriture = [o.get_nom(nb) for o, nb in dico_qtt.items()]
            if len(nourriture) > 1:
                ajout = ", ".join(nourriture[:-1]) + " et " + nourriture[-1]
            else:
                ajout = nourriture[0]
            msg += "Ce récipient contient " + ajout + "."
        else:
            msg += "Ce récipient est vide."

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
        self.nourriture = []
