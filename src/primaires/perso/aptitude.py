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


"""Fichier contenant la classe Aptitude, détaillée plus bas."""

from abstraits.obase import *
from corps.fonctions import valider_cle

class Aptitude(BaseObj):

    """Classe rprésentant une aptitude.

    Une aptitude représente un savoir-faire d'un personnage, qui
    peut être inactive (elle influence indirectement ce que le personnage
    fait, comme la nyctalopie qui lui permet de voir la nuit), ou
    active (elle est verrouillée par commande). Dans ce dernier cas,
    au lieu de parler d'aptitude, on parle de technique, qui est donc
    une aptitude liée à une commande spécifique.

    Les aptitudes définies les contextes où elles sont actives : la
    nyctalopie, par exemple, influence directement la façon de voir
    du personnage. Une autre aptitude pourrait permettre à une race
    de détecter du métal pouvant être extrait ici.

    Les aptitudes ou techniques peuvent être créées dans le code ou
    bien scriptées, c'est pourquoi elles sont enregistrées en BaseObj.

    """

    def __init__(self, cle):
        valider_cle(cle)
        BaseObj.__init__(self)
        self.cle = cle
        self.nom = "une aptitude"
        self._construire()

    def __getnewargs__(self):
        return ("inconnue", )

    def __repr__(self):
        return "<Aptitude '{}'>".format(self.cle)

    def __str__(self):
        return self.cle
