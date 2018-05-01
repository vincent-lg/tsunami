# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant la classe Association, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.format.fonctions import supprimer_accents

class Association(BaseObj):

    """Classe représentant une association entre un objet et des valeurs.

    Une association est créée pour chaque objet dans
    'importeur.crafting.configuration'.

    On peut écrire ou lire des données en utilisant la modification
    d'attribut (soit directement, soit avec getattr ou setattr).

    """

    def __init__(self):
        BaseObj.__init__(self)
        self.associations = {}
        self._construire()

    def __getnewargs__(self):
        return ()

    def __repr__(self):
        return "<Associations {}>".format(self.associations.keys())

    def __getattr__(self, nom):
        """Essaye de récupérer l'association indiquée.

        Le nom peut contenir majuscules ou accents. Ils seront
        supprimés. Si la valeur ne peut être trouvée, retourne
        None.

        """
        nom = supprimer_accents(nom).lower()
        if "_statut" not in self.__dict__ or not self.construit:
            return object.__getattr__(self, nom)
        else:
            return self.associations.get(nom)

    def __setattr__(self, nom, valeur):
        """Modifie l'association.

        Le nom peut contenir majuscules ou accents. Ils seront
        supprimés.

        """
        nom = supprimer_accents(nom).lower()
        if not self.construit:
            object.__setattr__(self, nom, valeur)
        else:
            self.associations[nom] = valeur
