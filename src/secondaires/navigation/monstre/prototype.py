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


"""Fichier contenant la classe PrototypeMonstreMarin, détaillée plus bas."""

from abstraits.obase import MetaBaseObj
from primaires.vehicule.vehicule import Vehicule

types_monstres = {}

class MetaMonstreMarin(MetaBaseObj):

    """Métaclasse des monstres marins."""

    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        MetaBaseObj.__init__(cls, nom, bases, contenu)
        if cls.cle:
            types_monstres[cls.cle] = cls


class PrototypeMonstreMarin(Vehicule, metaclass=MetaMonstreMarin):

    """Un prototype de monstre marin.

    Cette classe est la classe de base des monstres marins. Une
    forme de classe abstraite dont les différents types de monstre
    marin héritent. Par exemple, pour créer un type 'serpent de mer',
    il faut hériter cette classe (voir le package types). Si un
    monstre serpent de mer doit être créé dans l'univers, ce sera pour
    le système un objet de type SerpentMer héritée de PrototypeMonstreMarin.

    Cette classe défini ainsi des méthodes et attributs que l'on pourra
    retrouver dans tous les types de monstres marins, ainsi que quelques
    techniques pour faciliter la manipulation des monstres marins en
    général.

    """

    logger = type(importeur).man_logs.get_logger("monstres")
    cle = ""
    id_actuel = 1

    def __init__(self, *args):
        """Constructeur du monstre marin."""
        Vehicule.__init__(self)
        self.id = type(self).id_actuel
        type(self).id_actuel += 1
        self.args = args

    def __getnewargs__(self):
        return self.args

    def __repr__(self):
        return "<MonstreMarin {}>".format(repr(self.cle))
