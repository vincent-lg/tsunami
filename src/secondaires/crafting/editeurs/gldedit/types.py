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


"""Module contenant l'éditeur de types d'objet de guilde."""

from primaires.interpreteur.editeur.aes import AES

class EdtTypes(AES):

    """Classe définissant l'éditeur de types."""

    def __init__(self, pere, objet=None, attribut=None, *args):
        """Constructeur de l'éditeur."""
        AES.__init__(self, pere, objet, attribut, *args)
        self.ajouter_option("i", self.opt_info)

    def opt_info(self, arguments):
        """Donne des informatiosn sur le type indiqué.

        Syntaxe :
            /i <nom du type>

        """
        nom_type = arguments.strip()
        try:
            o_type = importeur.objet.get_type(nom_type)
        except KeyError:
            self.pere << "|err|Type {} inconnu.|ff|".format(repr(nom_type))
            return

        msg = "Information sur le type d'objet {} :".format(o_type.nom_type)
        parent = o_type.__bases__ and o_type.__bases__[0] or None
        if parent:
            msg += "\n  Type parent : {}".format(parent.nom_type)
        else:
            msg += "\n  Type premier (sans parent)"

        if o_type.types:
            msg += "\n  Types enfants définis :"
            for sous_type in o_type.types.values():
                msg += "\n    " + sous_type.nom_type
                if sous_type.types:
                    msg += " ({} types enfants)".format(
                            len(sous_type.types))
        else:
            msg += "\n  Aucun type enfant."

        self.pere << msg
