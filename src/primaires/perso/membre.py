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


"""Fichier contenant la classe Membre, détaillée plus bas.
Dans ce contexte, un membre est une partie du corps, comme un bras ou une
jambe.

"""

from abstraits.obase import BaseObj
from primaires.format.fonctions import supprimer_accents

# Flags
AUCUN_FLAG = 0
AFFICHABLE = 1
PEUT_TENIR = 2

FLAGS = {
    "affichable": AFFICHABLE,
    "peut tenir": PEUT_TENIR,
}

STATUTS = ("entier", "brisé")

class Membre(BaseObj):

    """Classe définissant un membre, une partie du corps d'un personnage.

    Chaque personnage possède un squelette, qui peut être propre à sa race
    ou à une personnalisation propre. Certains PNJ, par exemple, auront
    des squelettes hors de la définition de toute race;

    """

    _nom = "membre"
    _version = 1
    def __init__(self, nom, modele=None, parent=None):
        """Constructeur d'un membre"""
        BaseObj.__init__(self)
        self.nom = nom
        self.article = "le"
        self.flags = AFFICHABLE
        self.statut = "entier"
        self.groupe = ""
        self.probabilite_atteint = 0
        self.supporte = 3
        self.equipe = []
        self.tenu = None # l'objet tenu
        self.parent = parent
        self._construire()
        if nom:
            self.recalculer_article()

        # Copie du modèle si existe
        if modele:
            self.nom = modele.nom
            self.article = modele.article
            self.flags = modele.flags
            self.groupe = modele.groupe
            self.probabilite_atteint = modele.probabilite_atteint
            self.supporte = modele.supporte

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        return "membre({})".format(self.nom)

    def __str__(self):
        return self.nom

    @property
    def nom_complet(self):
        """Retourne le nom complet avec article."""
        article = self.article
        nom = self.nom
        if article.endswith("'"):
            return article + nom
        else:
            return article + " " + nom

    def _get_statut(self):
        return self._statut_m
    def _set_statut(self, statut):
        if statut not in STATUTS:
            raise ValueError("Le statut {} n'existe pas pour " \
                    "un membre".format(statut))

        self._statut_m = statut

    statut = property(_get_statut, _set_statut)

    def peut_tenir(self):
        """Retourne True si le membre peut tenir."""
        if self.equipe:
            return self.flags & PEUT_TENIR != 0 \
                    and all(o.peut_tenir for o in self.equipe)
        else:
            return self.flags & PEUT_TENIR != 0

    def affichable(self):
        """Retourne True si le membre est affichable"""
        return self.flags & AFFICHABLE != 0

    def peut_equiper(self, objet=None):
        """Si l'objet est précisé :
            retourne True si l'objet peut être équipé par ce membre
        sinon
            retourne True si l'emplacement est libre

        """
        # On cherche à savoir si l'emplacement est libre
        # Un emplacement est considéré comme libre si aucun objet n'est tenu
        # ni équipé
        equipable = False
        if self.tenu is None:
            equipable = True

        if objet is None:
            return equipable
        else:
            epaisseurs = sum(o.epaisseur for o in self.equipe)
            emplacement = self.groupe or self.nom
            sur = self.equipe and self.equipe[-1] or None
            peut_equiper = True
            if sur:
                peut_equiper = False
                for t in objet.empilable_sur:
                    if sur.est_de_type(t):
                        peut_equiper = True
                        break

                for t in sur.empilable_sous:
                    if objet.est_de_type(t):
                        peut_equiper = True
                        break

            return peut_equiper and equipable and objet.emplacement == \
                    emplacement and epaisseurs + objet.epaisseur <= \
                    self.supporte and epaisseurs + 1 in objet.positions

    def equiper(self, objet):
        """Equipe l'objet."""
        self.equipe.append(objet)
        if self.parent:
            objet.contenu = self.parent.equipement.equipes

    def tester(self, nom_flag):
        """Teste le flag nom_flag."""
        flag = FLAGS[nom_flag]
        return self.flags & flag

    def recalculer_article(self):
        """Recalcule l'article."""
        feminins = ("tete", "main", "patte")
        article = "le"
        nom = supprimer_accents(self.nom).lower()
        for debut in feminins:
            if nom.startswith(debut):
                article = "la"
                break

        if nom.startswith("aeiouyh"):
            article = "l'"

        self.article = article

class Groupe(BaseObj):

    """Classe définissant le groupe d'un membre.

    Un groupe permet de regrouper plusieurs membres et cela sert autant
    pour l'emplacement de l'équipement (une botte se porte aux pieds
    c'est-à-dire au pied gauche ou au pied droit dans un squelette classique)
    que pour regrouper de façon indissociable des membres (on ne peut
    équiper un objet sur la jambe gauche uniquement, on l'équipe
    sur les deux jambes à la fois).

    Attributs :
        nom -- le nom du groupe
        dissociable -- spécifie si les membres du groupe sont dissociables
            Par exemple, les membres du groupes 'jambes' ne le sont pas.

    """

    def __init__(self, nom):
        """Constructeur du groupe."""
        self.nom = nom
        self.dissociable = True

