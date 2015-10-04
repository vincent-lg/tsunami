# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Ce fichier contient la classe Rapport, détaillée plus bas."""

from datetime import datetime
from textwrap import wrap

from abstraits.obase import BaseObj
from primaires.format.date import get_date
from primaires.format.description import Description
from primaires.format.fonctions import echapper_accolades
from secondaires.rapport.commentaire import Commentaire
from .constantes import *

class Rapport(BaseObj):

    """Classe définissant un rapport de bug ou une suggestion.

    Un rapport définit une demande, de correction, d'amélioration ou
    une simple suggestion. La distinction se fait dans l'attribut
    self.type qui contient le type de la demande tel que défini dans
    les constantes.

    """

    enregistrer = True
    id_actuel = 1
    _nom = "rapport"
    _version = 1

    def __init__(self, titre, createur=None):
        """Constructeur d'un rapport."""
        BaseObj.__init__(self)
        self.ouvert = True
        self.id = type(self).id_actuel
        type(self).id_actuel += 1
        self.titre = titre
        self.avancement = 0
        self.description = Description(parent=self, scriptable=False)
        self.date = datetime.now()
        self.createur = createur
        self.assigne_a = None
        self.salle = createur.salle if createur else None
        self._type = "bug"
        self.public = False # Rapport non public de base.
        self._priorite = "normale"
        self._categorie = ""
        self.str_statut = "nouveau"

        # Copie
        self.source = None
        self.commentaires = []
        self._construire()

    def __getnewargs__(self):
        return ("", None)

    def __repr__(self):
        return "<rapport {} #{} ({}%)>".format(
                self.type, self.id, self.avancement)

    @property
    def nonassigne(self):
        """Retourne True si le rapport n'est pas assigné."""
        return self.assigne_a is None

    @property
    def aff_assigne_a(self):
        return self.assigne_a and self.assigne_a.nom or "personne"

    @property
    def aff_createur(self):
        return self.createur and self.createur.nom or "inconnu"

    @property
    def int_priorite(self):
        """Retourne la priorité sous la forme d'un entier."""
        return PRIORITES.index(self._priorite)

    @property
    def aff_titre(self):
        """Retourne le titre échappé."""
        return echapper_accolades(self.titre)

    def _get_type(self):
        return self._type
    def _set_type(self, type):
        if type not in TYPES:
            raise ValueError("type {} inconnu".format(type))
        self._type = type
    type = property(_get_type, _set_type)

    def _get_priorite(self):
        return self._priorite
    def _set_priorite(self, priorite):
        if priorite not in PRIORITES:
            raise ValueError("priorité {} inconnue".format(priorite))
        self._priorite = priorite
    priorite = property(_get_priorite, _set_priorite)

    def _get_statut(self):
        return self.str_statut
    def _set_statut(self, statut):
        if statut not in STATUTS:
            raise ValueError("statut {} inconnu".format(statut))
        self.str_statut = statut
        self.appliquer_statut()
    statut = property(_get_statut, _set_statut)

    def _get_categorie(self):
        return self._categorie
    def _set_categorie(self, categorie):
        if categorie not in CATEGORIES:
            raise ValueError("catégorie {} inconnue".format(categorie))
        self._categorie = categorie
    categorie = property(_get_categorie, _set_categorie)

    def copier(self, autre):
        """Copie les attributs d'un autre rapport."""
        self.source = autre
        self.ouvert = autre.ouvert
        self.titre = autre.titre
        self.avancement = autre.avancement
        self.description = autre.description
        self.date = autre.date
        self.createur = autre.createur
        self.assigne_a = autre.assigne_a
        self.salle = autre.salle
        self._type = autre.type
        self._priorite = autre.priorite
        self._categorie = autre.categorie
        self.str_statut = autre.str_statut

    def verifier(self):
        """Vérifie que createur et assigne_a sont toujours présents."""
        if self.createur and not self.createur.e_existe:
            self.createur = None
        if self.salle and not self.salle.e_existe:
            self.salle = None
        if self.assigne_a and not self.assigne_a.e_existe:
            self.assigne_a = None

    def appliquer_statut(self):
        """Applique le statut selon des règles définies.

        Par exemple, il est bon que le statut fermé ferme effectivement
        le rapport en changeant son avancement par exemple.

        """
        statut = self.str_statut
        attrs = ATTRS_STATUTS.get(statut)
        if attrs is None:
            return

        for nom, valeur in attrs:
            setattr(self, nom, valeur)

    def est_complete(self):
        """Return True si le rapport est complété, False sinon.

        On considère qu'un rapport est complété si tous les attributs
        en clé du dictionnaire COMPLETE sont vrais pour self.

        """
        for attr in COMPLETE.keys():
            if not getattr(self, attr):
                return False

        return True

    def get_champs_a_completer(self):
        """Retourne les champs à compléter."""
        champs = []
        for attr, nom in COMPLETE.items():
            if not getattr(self, attr):
                champs.append(nom)

        return champs

    def get_description_pour(self, personnage):
        """Retourne la description textuelle pour le personnage."""
        createur = self.createur.nom if self.createur else "personne"
        ret = "Rapport #" + str(self.id) + " : " + echapper_accolades(self.titre)
        ret += "\nCatégorie : " + self.type + " (" + \
                self.categorie + ")"
        ret += "\nStatut : " + self.statut + ", avancement : " + \
                str(self.avancement) + "%"
        ret += "\nCe rapport est classé en priorité " + \
                self.priorite + "."
        ret += "\nDétail :\n"
        ret += echapper_accolades(str(self.description))
        ret += "\nRapport envoyé par " + createur + " " +\
                get_date(self.date.timetuple()) + "\n"
        if personnage.est_immortel():
            ret += "Depuis " + str(self.salle) + " "
        ret += "Assigné à " + self.aff_assigne_a + "."

        # Comemntaires
        if self.commentaires:
            ret += "\n\nCommentaires du rapport:"
            for i, commentaire in enumerate(self.commentaires):
                auteur = commentaire.auteur and commentaire.auteur.nom or \
                        "inconnu"
                ret += "\n {:> 2} - par {}, {}".format(i + 1, auteur,
                        get_date(commentaire.date.timetuple()))
                ret += "\n      " + ("\n      ").join(wrap(
                        echapper_accolades(commentaire.texte), 70))

        return ret

    def commenter(self, auteur, texte):
        """Commente un rapport."""
        commentaire = Commentaire(self, auteur, texte)
        self.commentaires.append(commentaire)
        return commentaire
