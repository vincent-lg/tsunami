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


"""Fichier contenant le type meuble."""

from textwrap import dedent

from bases.objet.attribut import Attribut
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.interpreteur.editeur.tableau import Tableau
from primaires.objet.conteneur import ConteneurObjet
from .base import BaseType

class Meuble(BaseType):

    """Type d'objet: meuble."""

    nom_type = "meuble"
    nettoyer = False

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.nb_places_assises = 1
        self.nb_places_allongees = 1
        self.poids_max = 10
        self.facteurs_repos = {
                "assis": 0,
                "allongé": 0,
        }

        self.messages = {
                "assis": "Vous vous assezez sur $meuble.",
                "allongé": "Vous vous allongez sur $meuble.",
                "oassis": "$personnage s'asseze sur $meuble.",
                "oallongé": "$personnage s'allonge sur $meuble.",
                "contenu": "Vous voyez à l'intérieur :",
                "vide": "Il n'y a rien à l'intérieur.",
                "pose": "Vous entreposez $objet dans $meuble.",
                "prend": "Vous prenez $objet depuis $meuble.",
                "opose": "$personnage entrepose $objet dans $meuble.",
                "oprend": "$personnage prend $objet depuis $meuble.",
        }

        # Extensions d'éditeur
        self.etendre_editeur("x", "poids max", Flottant, self, "poids_max")
        self.etendre_editeur("r", "facteurs de repos", Tableau, self,
                "facteurs_repos", (("Nom", ["assis", "allongé"]),
                ("Facteur", "flottant")))
        self.etendre_editeur("m", "messages", Tableau, self,
                "messages", (("Type", ["assis", "allongé",
                "contenu", "vide", "pose", "prend", "opose", "oprend"]),
                ("Message", "chaîne")))

        # Attributs propres à l'objet (non au prototype)
        self._attributs = {
            "conteneur": Attribut(
                lambda obj: ConteneurObjet(obj),
                ("", )),
        }

    @property
    def peut_asseoir(self):
        """Return si peut s'asseoir sur le meuble."""
        return self.facteurs_repos["assis"] > 0

    @property
    def peut_allonger(self):
        """Return si peut s'allonger sur le meuble."""
        return self.facteurs_repos["allongé"] > 0

    @property
    def facteur_asseoit(self):
        return self.facteurs_repos["assis"]

    @property
    def facteur_allonge(self):
        return self.facteurs_repos["allongé"]

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

    def combien_dans(self, objet):
        """Retourne combien d'objet indiqué sont dans le conteneur."""
        for o, qtt in self.conteneur.iter_nombres():
            if objet is o:
                return qtt

        return 0

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        poids_max = enveloppes["x"]
        poids_max.apercu = "{objet.poids_max} kg"
        poids_max.prompt = "Poids max du conteneur : "
        poids_max.aide_courte = \
            "Entrez le |ent|poids maximum|ff| du conteneur ou " \
            "|cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Poids maximum actuel : {objet.poids_max}"

        # Facteurs de repos
        repos = enveloppes["r"]
        repos.apercu = "{valeur}"
        repos.prompt = "Facteurs de repos : "
        repos.aide_courte = dedent("""
            Entrez |ent|/|ff| pour revenir à la fenêtre parente.

            Cet éditeur permet de configurer les facteurs de
            récupération quand on utilise ce meuble pour s'asseoir
            ou s'allonger. On ne peut, bien évidemment, pas s'assseoir
            ou s'allonger sur tous les meubles. Si le facteur précisé
            est de |ent|0|ff|, alors s'asseoir ou s'allonger est
            impossible sur ce meuble. Sinon, le facteur doit représenter
            la récupération de statistiques quand on se repose sur
            le meuble. Un facteur de |ent|1|ff| veut dire que le
            personnage récupère aussi vite que si il était debout.
            Un facteur de |ent|1.2|ff| signifie que le joueur récupère
            1,2 fois plus vite (au lieu de récupérer 10 points de
            vitalité par tick, par exemple, il en récupérerait 12).

            Pour remplacer un facteur, entrez son nom, un signe |ent|/|ff|
            après un espace et le nouveau facteur après un autre espace.
            Exemple : |cmd|assis / 1.15|ff|
            (La virgule est à remplacer par le point.)
            {valeur}
        """.strip("\n"))

        # Messages
        messages = enveloppes["m"]
        messages.apercu = "{valeur}"
        messages.prompt = "Messages d'affichage :"
        messages.aide_courte = dedent("""
            Entrez |ent|/|ff| pour revenir à la fenêtre parente.

            Cet éditeur permet de configurer les messages affichés
            dans certaines situations. Par exemple, le message "vide"
            est affiché quand le meuble regardé est vide. Les types
            des messages sont :
                assis : le joueur s'asseoit sur le meuble.
                allongé : le joueur s'allonge sur le meuble.
                oassis : le message que voient les autres quand on s'asseoit.
                oallonge : le message que voient les autres quand on s'allonge.
                contenu : le meuble regardé contient quelque chose.
                vide : le meuble regardé ne contient rien.
                pose : on pose un ou plusieurs objets sur le meuble.
                prend : on prend un ou plusieurs objets depuis le meuble.
                opose : le message envoyé aux autres joueurs présents
                        quand un joueur pose un objet sur le meuble.
                oprend : le message envoyé aux autres joueurs présents
                        quand un joueur prend un objet depuis le meuble.

            Dans chaque message, on peut utiliser le symbol $meuble
            qui sera remplacé par le nom du meuble. Les messages
            "pose" et "prend" supportent également le symbol $objet,
            qui sera remplacé par le nom de l'objet (ou des objets)
            manipulés). "opose" et "oprend" supportent $meuble et $objet,
            ainsi que $personnage remplacé par le nom du personnage
            manipulant le meuble.

            Pour remplacer un message, entrez son type, un signe |ent|/|ff|
            après un espace et le nouveau message après un autre espace.
            Exemple : |cmd|vide / Il n'y a rien de posé sur cette table.|ff|
            (N'oubliez pas les majuscules et signes de ponctuation.)
            {valeur}
        """.strip("\n"))

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
            contenu = self.messages["contenu"]
            contenu = contenu.replace("$meuble", self.get_nom(1))
            msg += contenu
            msg += "\n  " + "\n  ".join(objets)
        else:
            vide = self.messages["vide"]
            vide = vide.replace("$meuble", self.get_nom(1))
            msg += vide

        return msg
