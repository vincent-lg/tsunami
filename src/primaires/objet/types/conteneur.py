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


"""Fichier contenant le type Conteneur."""

from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.interpreteur.editeur.selection import Selection
from bases.objet.attribut import Attribut
from .base import BaseType
from primaires.objet.conteneur import ConteneurObjet

class Conteneur(BaseType):

    """Type d'objet: conteneur.

    Les conteneurs sont des objets pouvant en contenir d'autres.

    """

    nom_type = "conteneur"
    nettoyer = False

    empilable_sur = ["vêtement", "armure"]
    _attributs = {
        "conteneur": Attribut(
            lambda obj: ConteneurObjet(obj),
            ("", )),
    }

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.types_admis = ["*"]
        self.poids_max = 10
        self.meuble_support = False
        self.etendre_editeur("x", "poids max", Flottant, self, "poids_max")
        self.etendre_editeur("t", "types admis", Selection, self,
                "types_admis", type(self).importeur.objet.noms_types)
        self.etendre_editeur("m", "meuble support", Flag, self,
                "meuble_support")

    @property
    def str_types_admis(self):
        """Retourne une chaîne représentant les types admis actuels.

        Si la liste contient la chaîne *, tous les types sont possibles.
        Si la liste est vide, la chaîne l'est également.

        """
        if not self.types_admis:
            return "|err|aucun|ff|"
        elif "*" in self.types_admis:
            return "|rgc|tous|ff|"
        else:
            return "|cmd|" + "|ff|, |cmd|".join(sorted(
                    self.types_admis)) + "|ff|"

    @property
    def str_types(self):
        """Retourne une chaîne représentant les types actuels."""
        return ", ".join(type(self).importeur.objet.noms_types)

    def prefere_type(self, objet):
        """Retourne True si l'objet est l'un des types admis, False sinon.

        Comparé à la méthode accepte_type, celle-ci retourne True
        uniquement si le conteneur accepte seulement certains types,
        pas tous.

        """
        if self.types_admis == ['*']:
            return False

        for type in self.types_admis:
            if objet.est_de_type(type):
                return True

        return False

    def accepte_type(self, objet):
        """Retourne True si le conteneur accepte le type d'objet."""
        return self.types_admis == ["*"] or self.prefere_type(objet)

    def peut_contenir(self, objet, qtt=1):
        """Retourne True si le conteneur peut prendre l'objet."""
        poids = objet.poids * qtt
        contenu = self.poids - self.prototype.poids_unitaire
        poids_max = self.poids_max
        return contenu + poids <= poids_max

    def calculer_poids(self):
        """Retourne le poids de l'objet et celui des objets contenus."""
        poids = self.poids_unitaire
        for o, nb in self.conteneur.iter_nombres():
            poids += o.poids * nb

        return round(poids, 3)

    def contient(self, objet, quantite):
        """Retourne True si le conteneur contient l'objet, False sinon.

        Si l'objet est présente au moins dans la quantité indiquée,
        retourne True mais False si ce n'est pas le cas.
        Si on cherche un objet en quantité N et que l'objet est trouvé
        en quantité >= N, on retourne True sinon False.

        """
        for o, qtt in self.conteneur.iter_nombres():
            if objet is o:
                if qtt >= quantite:
                    return True
                return False

        return False

    def contient_recursif(self, objet):
        """ Retourne True si le conteneur ou un de ses enfants contient l'objet

        Aucun test de quantité ici contrairement à la méthode contient.

        """
        for o in self.conteneur:
            if o is objet:
                return True
            if o.est_de_type("conteneur") and o.contient_recursif(objet):
                return True

        return False

    def combien_dans(self, objet):
        """Retourne combien d'objet indiqué sont dans le conteneur."""
        for o, qtt in self.conteneur.iter_nombres():
            if objet is o:
                return qtt

        return 0

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        types_admis = enveloppes["t"]
        types_admis.apercu = "{objet.str_types_admis}"
        types_admis.aide_courte = \
            "Entrez les différents |ent|types admis|ff| de ce conteneur " \
            "ou |cmd|/|ff| pour revenir à la\n" \
            "fenêtre parente. Pour ajouter un |ent|type admis|ff|, entrez " \
            "son nom. Si il est déjà\n" \
            "dans la liste, il sera ajouté. Sinon, il sera retiré.\n" \
            "Entrez |cmd|*|ff| si vous voulez indiquer tous les types " \
            "possibles.\n\n" \
            "Types possibles : {objet.str_types}\n\n" \
            "Types admis actuels : {objet.str_types_admis}"

        poids_max = enveloppes["x"]
        poids_max.apercu = "{objet.poids_max} kg"
        poids_max.prompt = "Poids max du conteneur : "
        poids_max.aide_courte = \
            "Entrez le |ent|poids maximum|ff| du conteneur ou " \
            "|cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Poids maximum actuel : {objet.poids_max}"

    def objets_contenus(self, conteneur):
        """Retourne les objets contenus."""
        objets = []
        for objet in list(conteneur.conteneur._objets):
            objets.append(objet)
            objets.extend(objet.prototype.objets_contenus(objet))

        return objets

    def detruire_objet(self, conteneur):
        """Détruit l'objet passé en paramètre.

        On va détruire tout ce qu'il contient.

        """
        for objet in list(conteneur.conteneur._objets):
            if conteneur is not objet and objet.unique and objet.e_existe:
                importeur.objet.supprimer_objet(objet.identifiant)

    # Actions sur les objets
    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        msg = BaseType.regarder(self, personnage)
        if not getattr(self, "conteneur", False):
            return msg

        objets = []
        for o, nb in self.conteneur.get_objets_par_nom():
            objets.append(o.get_nom(nb))

        if objets:
            msg += "Vous voyez "
            if self.meuble_support:
                msg += "dessus :"
            else:
                msg += "à l'intérieur :"
            msg += "\n  " + "\n  ".join(objets)
        elif self.meuble_support:
            msg += "Vous ne voyez rien dessus."
        else:
            msg += "Vous ne voyez rien à l'intérieur."

        return msg
