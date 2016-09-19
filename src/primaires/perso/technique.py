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


"""Fichier contenant la classe Technique, détaillée plus bas."""

from primaires.format.description import Description
from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.parametre import Parametre
from primaires.perso.aptitude import Aptitude

class Technique(Aptitude):

    """Classe rprésentant une technique.

    Une technique est une aptitude active liée à une commande. Pour
    l'utiliser, le personnage doit donc entrer une commande spécifique.

    """

    nom_scripting = "la technique"

    def __init__(self, cle):
        Aptitude.__init__(self, cle)
        self.parent = None
        self.nom = "une technique"
        self.nom_francais = None
        self.nom_anglais = None
        self._utilisable = False
        self._nom_categorie = "divers"
        self._aide_courte = "à renseigner..."
        self.aide_longue = Description(parent=self, scriptable=False,
                callback="maj")
        self._schema = ""

    def __repr__(self):
        return "<Technique '{}'>".format(self.cle)

    @property
    def nom_complet(self):
        """Retourne le nom complet (<parent>:)<fr>/<an>."""
        parent = "{} ".format(self.parent) if self.parent else ""
        return parent + self.nom_francais

    @property
    def nom_francais_complet(self):
        """Retourne le nom français complet (parent:nom_francais)."""
        parent = "{} ".format(self.parent) if self.parent else ""
        return parent + self.nom_francais

    def _get_aide_courte(self):
        return self._aide_courte
    def _set_aide_courte(self, aide):
        if len(aide) > 70:
            aide = aide[:70]
        self._aide_courte = aide
        self.maj()
    aide_courte = property(_get_aide_courte, _set_aide_courte)

    def _get_nom_categorie(self):
        return self._nom_categorie
    def _set_nom_categorie(self, categorie):
        self._nom_categorie = categorie
        self.maj()
    nom_categorie = property(_get_nom_categorie, _set_nom_categorie)

    def _get_utilisable(self):
        return self._utilisable
    def _set_utilisable(self, utilisable):
        self._utilisable = utilisable
        if utilisable and self.commande is None:
            self.ajouter()
    utilisable = property(_get_utilisable, _set_utilisable)

    def _get_schema(self):
        return self._schema
    def _set_schema(self, schema):
        self._schema = schema
        if self.commande:
            self.commande.noeud.construire_arborescence(schema)
            self.maj_variables()
    schema = property(_get_schema, _set_schema)

    def ajouter_commande(self):
        """Ajoute la commande dans l'interpréteur.

        Si la commande a un parent, on va créer à la place son
        paramètre.

        """
        parent = None
        if self.parent:
            parent = importeur.interpreteur.trouver_commande(self.parent)
            commande = Parametre(self.nom_francais, self.nom_anglais)
        else:
            commande = Commande(self.nom_francais, self.nom_anglais)

        commande.schema = self.schema
        commande.groupe =  "pnj"
        commande.nom_categorie = self.nom_categorie
        commande.aide_courte = self.aide_courte
        commande.aide_longue = str(self.aide_longue)
        commande.peut_executer = self.peut_executer
        commande.interpreter = self.interpreter
        if parent:
            parent.ajouter_parametre(commande)
        else:
            importeur.interpreteur.ajouter_commande(commande)

        return commande

    def peut_executer(self, personnage):
        """Retourne True si le personnage peut ecuter la commande."""
        return True

    def interpreter(self, personnage, dic_masques):
        """Méthode outre-passant l'interprétation de la commande statique.

        Dans cette méthode peut être codé la technique. Si il s'agit
        d'une attitude scriptée (directement parente de Technique), son
        script sera appelé.

        """
        pass
