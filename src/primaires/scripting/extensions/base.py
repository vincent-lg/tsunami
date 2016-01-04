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


"""Fichier contenant la classe Extension, détaillée plus bas."""

from abstraits.obase import *
from primaires.format.description import Description

class Extension(BaseObj):

    """Classe abstraite définissant une extension d'éditeur personnalisé.

    Chaque type d'extension (chaîne, nombre, presentation, etc)
    possède sa propre classe. Elle définit les paramètres et la
    façon dont l'éditeur doit être créée.

    Propriété à redéfinir :
        @property
        def editeur(self):
            '''Retourne le type d'éditeur, comme Uniligne pour chaîne.'''

        @property
        def arguments(self):
            '''Retourne la liste des arguments attendus par l'éditeur.'''

    """

    extension = "abstraite"

    def __init__(self, structure, nom):
        """Constructeur d'un éditeur personnalisé."""
        BaseObj.__init__(self)
        self.structure = structure
        self.nom = nom
        self.titre = nom
        self.description = Description(parent=self, scriptable=False)
        self.apercu = "$valeur"
        self._construire()

    def __getnewargs__(self):
        return (None, "inconnu")

    def __repr__(self):
        return "<Extension d'éditeur {}>".format(repr(type(self).extension))


    @property
    def cle_type(self):
        return self.nom + " / " + type(self).extension

    @property
    def editeur(self):
        """Retourne le type d'éditeur."""
        raise NotImplementedError

    @property
    def arguments(self):
        """Retourne les arguments de l'éditeur."""
        raise NotImplementedError

    def creer(self, parent, structure):
        """Crée l'éditeur sur le modèle du parent."""
        enveloppe = parent.ajouter_choix(self.titre, None, self.editeur,
                structure, self.nom, *self.arguments)
        enveloppe.parent = parent
        enveloppe.apercu = self.apercu.replace("$valeur", "{valeur}")
        enveloppe.aide_courte = str(self.description).replace("{",
                "{{").replace("}", "}}").replace("$valeur", "{valeur}")
        return enveloppe

    def etendre_editeur(self, presentation):
        """Étend l'éditeur en fonction de l'extension."""
        pass
