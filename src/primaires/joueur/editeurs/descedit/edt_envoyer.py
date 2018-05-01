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


"""Fichier contenant le contexte éditeur EdtEnvoyer."""

from primaires.interpreteur.editeur import Editeur

class EdtEnvoyer(Editeur):

    """Classe définissant le contexte éditeur 'envoyer'.

    Ce contexte permet d'envoyer une description de joueur en validation si
    le joueur n'est pas immortel. Sinon, la description est automatiquement
    validée.

    """

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)

    def entrer(self):
        joueur = self.objet
        if joueur.est_immortel():
            joueur.description_a_valider.paragraphes[:] = \
                    joueur.description.paragraphes
            self.pere.envoyer("Cette description a été automatiquement " \
                    "validée.")
        else:
            joueur.description_modifiee = True
            self.pere.envoyer("La description a bien été envoyée en " \
                    "validation.")
        self.fermer()
