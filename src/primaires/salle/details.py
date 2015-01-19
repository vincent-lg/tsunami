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


"""Ce fichier contient la classe Details, détaillée plus bas."""

from abstraits.obase import *
from .detail import Detail

class Details(BaseObj):

    """Cette classe est un conteneur de détails.

    Elle contient les détails observables d'une salle, que l'on peut voir
    avec la commande look.

    Voir : ./detail.py

    """

    def __init__(self, parent=None):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.parent = parent
        self._details = {}
        # On passe le statut en CONSTRUIT
        self._construire()

    def __getnewargs__(self):
        return ()

    def __iter__(self):
        return iter(self._details.values())
    def __getitem__(self, nom):
        """Retourne le détail 'nom'"""
        return self._details[nom]

    def __setitem__(self, nom, detail):
        """Modifie le détail 'nom'"""
        self._details[nom] = detail

    def __delitem__(self, nom):
        """Détruit le détail passée en paramètre"""
        del self._details[nom]

    def iter(self):
        """Retourne un dictionnaire contenant les details"""
        return dict(self._details).items()

    def ajouter_detail(self, nom, *args, **kwargs):
        """Ajoute un détail à la liste.
        Les arguments spécifiés sont transmis au constructeur de Detail.
        Le nom correspondra au self.nom du détail.
        Si un détail sous ce nom-là existe déjà, il sera écrasé.

        """
        detail = Detail(nom, *args, parent=self.parent, **kwargs)
        self[nom] = detail

        return detail

    def get_detail(self, nom, flottants=False):
        """Renvoie le détail 'nom', si elle existe.

        A la différence de __getitem__(), cette fonction accepte en paramètre
        un des synonymes du détail recherchée.

        """
        res = None
        details = self._details.copy()
        if self.parent and flottants:
            description = self.parent.description
            for paragraphe in description.paragraphes:
                p, flottantes = description.charger_descriptions_flottantes(
                        paragraphe)
                for flottante in flottantes:
                    for d in flottante.details:
                        if d.nom not in details:
                            details[d.nom] = d

        for d_nom, detail in details.items():
            if nom == d_nom or nom in detail.synonymes:
                res = detail

        return res

    def detail_existe(self, nom, flottants=False):
        """Renvoie True si le détail 'nom' existe"""
        return self.get_detail(nom, flottants) is not None
