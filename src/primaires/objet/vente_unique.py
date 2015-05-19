# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Ce fichier contient la classe VenteUnique, détaillée plus bas."""

from abstraits.obase import BaseObj

class VenteUnique(BaseObj):

    """Cette classe définit un service pour la vente unique d'objet.

    Par défaut, les magasins ne retiennent pas les objets, juste
    les prototypes d'objets. Pour certains objets uniques, c'est
    un problème. Ce service existe donc pour s'assurer que, dans
    certains cas (si le nom de l'objet diffère du nom du prototype),
    l'objet soit conservé intégralement.

    """

    type_achat = "unique"

    def __init__(self, objet):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.objet = objet
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<{}>".format(repr(self.objet))

    def __str__(self):
        return str(self.objet)

    @property
    def m_valeur(self):
        return self.objet.prix

    @property
    def nom_achat(self):
        """Retourne le nom à afficher dans le magasin."""
        if self.objet:
            return self.objet.nom_singulier

        return "inconnu"

    def get_nom(self, nombre=1):
        """Retourne le nom complet en fonction du nombre.

        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel

        """
        if self.objet:
            return self.objet.get_nom(nombre)

        return "inconnu"

    def acheter(self, quantite, magasin, transaction):
        """Achète les objets dans la quantité spécifiée."""
        salle = magasin.parent
        if self.objet:
            salle.objets_sol.ajouter(self.objet)

    def regarder(self, personnage):
        """Le personnage regarde le service (avant achat)."""
        return self.objet.regarder(personnage)
