# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'retirer' de la commande 'cale'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmRetirer(Parametre):

    """Commande 'cale retirer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "retirer", "out")
        self.schema = "(<nombre>) <objet_cale>"
        self.aide_courte = "récupère des marchandises depuis la cale"
        self.aide_longue = \
            "Cette commande permet de récupérer des marchandises depuis " \
            "la cale. Vous devez pour cela vous trouvez dans une salle " \
            "du navire dans laquelle la cale est accessible (certains " \
            "types de marchandise peuvent avoir plusieurs emplacements " \
            "dans le navire). Vous devez préciser en paramètre optionnel " \
            "le nombre d'objets à récupérer et ensuite le nom ou " \
            "fragment du nom de l'objet à récupérer."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        if navire.accoste and not navire.a_le_droit(personnage):
            personnage << "|err|Vous n'avez pas le droit de retirer " \
                    "des objets de la cale.|ff|"
            return

        cale = navire.cale
        prototype = dic_masques["objet_cale"].prototype
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre

        cale.recuperer(personnage, prototype.cle, nombre)
