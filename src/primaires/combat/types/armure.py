# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant le type armure."""

from random import randint

from bases.objet.attribut import Attribut
from primaires.combat.types.editeurs.fourreau import EdtFourreau
from primaires.format.fonctions import oui_ou_non
from primaires.interpreteur.editeur.entier import Entier
from primaires.objet.types.base import BaseType

class Armure(BaseType):

    """Type d'objet: armure.

    Ce type est une classe-mère des armuers spécifiques (casque,
    cotte de mailles...).

    """

    nom_type = "armure"
    _nom = "prototype_armure"
    _version = 1

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.empilable_sur = ["vêtement"]
        self.encaissement_fixe = 5
        self.encaissement_variable = 0
        self.fourreau = False
        self.fourreau_visible = True
        self.poids_max_fourreau = 1
        self.types_fourreau = []
        self._attributs = {
            "au_fourreau": Attribut(None),
        }

        # Editeurs
        self.etendre_editeur("f", "encaissement fixe", Entier, self,
                "encaissement_fixe")
        self.etendre_editeur("v", "encaissement variable", Entier, self,
                "encaissement_variable")
        self.etendre_editeur("fo", "fourreau", EdtFourreau, self, "")

    @property
    def str_types_fourreau(self):
        """Retourne une chaîne représentant les types admis en fourreau."""
        if len(self.types_fourreau) == 0:
            return "aucun"
        else:
            return ", ".join(self.types_fourreau)

    @property
    def str_fourreau(self):
        """Retourne oui ou non."""
        return oui_ou_non(self.fourreau)

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        fixe = enveloppes["f"]
        fixe.apercu = "{objet.encaissement_fixe}"
        fixe.prompt = "Encaissement fixe de l'armure : "
        fixe.aide_courte = \
            "Entrez l'|ent|encaissement fixe|ff| de l'armure. Il " \
            "représente\nla quantité de dégâts fixes que l'armure peut " \
            "encaisser.\nÀ cet encaissement s'ajoute l'encaissement " \
            "variable. Si les\ndégâts dépassent l'encaissement de l'armure, " \
            "l'armure n'encaisse\nque ce qu'elle a été configurée pour " \
            "et le personnage derrière\nreçoit les dégâts compensés. Si " \
            "les dégâts sont inférieurs à\nl'enciassement de l'armure, " \
            "le personnage ne reçoit rien.\n\n" \
            "Encaissement fixe actuel : {objet.encaissement_fixe}"

        variable = enveloppes["v"]
        variable.apercu = "{objet.encaissement_variable}"
        variable.prompt = "Encaissement variable de l'armure : "
        variable.aide_courte = \
            "Entrez l'|ent|encaissement variable|ff| de l'armure. Il " \
            "représente\nla partie variable de l'encaissement global, " \
            "celui-ci étant\nl'encaissement fixe plus l'encaissement " \
            "variable déterminé aléatoirement,\nentre |ent|0|ff| et " \
            "l'encaissement variable configuré. Une armure\navec un " \
            "encaissement fixe de |ent|5|ff| et des dégâts variables de " \
            "|ent|2|ff|\naura un encaissement entre |ent|5|ff| et " \
            "|ent|7|ff|.\n\nEncaissement variable actuel : " \
            "{objet.encaissement_variable}"

        fourreau = enveloppes["fo"]
        fourreau.apercu = "{objet.str_fourreau}"

    def encaisser(self, personnage, arme, degats):
        """Retourne les dégâts en tenant compte de l'encaissement.

        La stat 'robustesse' du personnage est utilisée pour estimer
        à quel point l'armure protège le membre (pour la robustesse est
        élevée, plus la protection est importante).

        """
        if degats <= 1:
            return 0

        taux = 0.5 + personnage.stats.robustesse / 200
        encaissement = self.encaissement_fixe
        if self.encaissement_variable > 0:
            encaissement = randint(self.encaissement_fixe,
                    self.encaissement_fixe + self.encaissement_variable)

        encaissement = int(taux * encaissement)
        if encaissement > degats - 1:
            encaissement = degats - 1

        return encaissement

    def calculer_poids(self):
        """Retourne le poids de l'objet et celui des objets contenus."""
        poids = self.poids_unitaire
        if self.au_fourreau:
            poids += self.au_fourreau.poids

        return round(poids, 3)

    def objets_contenus(self, conteneur):
        """Retourne les objets contenus."""
        objets = []
        if conteneur.au_fourreau:
            objet = conteneur.au_fourreau
            objets.append(objet)
            objets.extend(objet.prototype.objets_contenus(objet))

        return objets

    def get_nom(self, nombre=1):
        """Retourne le nom complet en fonction du nombre.

        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel

        """
        ajout = ""
        if self.fourreau_visible and getattr(self, "au_fourreau", None):
            ajout = " {{" + self.au_fourreau.nom_singulier + "}}"

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
                        return nom[1]
            return str(nombre) + " " + self.nom_pluriel

    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        msg = BaseType.regarder(self, personnage)
        if self.au_fourreau:
            msg += "Au fourreau : " + self.au_fourreau.nom_singulier

        return msg
