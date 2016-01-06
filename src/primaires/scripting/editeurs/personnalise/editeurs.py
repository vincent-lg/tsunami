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


"""Fichier contenant la classe EdtPresentation, détaillée plus bas."""

from primaires.interpreteur.editeur.aes import AES
from primaires.scripting.extensions import EXTENSIONS

aide = """
Entrez |cmd|/|ff| pour revenir à la fenêtre parente.
Utilisez les options :
 |ent|/a <clé_de_l_éditeur> / <type de donnée>|ff| pour ajouter un éditeur
 |ent|/s <cle_de_l_éditeur>|ff| pour supprimer l'éditeur
 |ent|<cle_de_l_editeur>|ff| pour éditer l'éditeur
 |ent|/h <cle_de_l_editeur>|ff| pour remonter l'éditeur dans la liste
 |ent|/b <cle_de_l_editeur>|ff| pour redescendre l'éditeur dans la liste

Types de données existants :{types}

Exemples :
 |cmd|/a titre / chaîne|ff|
 (Ajoute l'éditeur de clé 'titre' et de type 'chaîne')
 |cmd|titre|ff|
 (Édite l'éditeur 'titre')
 |cmd|/s titre|ff|
 (Supprime l'éditeur 'titre')

Éditeurs actuels :{{valeur}}
""".strip()

class EdtEditeurs(AES):

    """Classe définissant l'éditeur d'une quête.

    """

    def __init__(self, instance_connexion, editeur, attribut=None):
        """Constructeur de l'éditeur."""
        AES.__init__(self, instance_connexion, editeur, "editeurs",
                "personnalise", (("cle", "clé"), ("type", "chaîne")),
                "get_editeur", "ajouter_editeur", "supprimer_editeur",
                "cle_type")

    def __getnewargs__(self):
        return (None, None)

    def _get_aide_courte(self):
        types = ""
        for extension in sorted(list(EXTENSIONS.values()),
                key=lambda e: e.extension):
            types += "\n  |ent|{:<10}|ff| : {}".format(
                    extension.extension, extension.aide)

        return aide.format(types=types)
    def _set_aide_courte(self, aide):
        pass
    aide_courte = property(_get_aide_courte, _set_aide_courte)
