# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant la méta-classe et la classe abstraite d'objectif."""

from abstraits.obase import BaseObj, MetaBaseObj

objectifs = {}

class MetaObjectif(MetaBaseObj):

    """Métaclasse des objectifs.

    Elle ajoute l'objectif dans le dictionnaire 'objectifs' si il possède
    une clé.

    """

    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        MetaBaseObj.__init__(cls, nom, bases, contenu)
        if cls.cle:
            objectifs[cls.cle] = cls

class Objectif(BaseObj, metaclass=MetaObjectif):

    """Définition abstraite d'un objectif.

    Cette classe doit être parente de tous les objectifs utilisés. Les
    méthodes et attributs donnés dans cette classe doivent pouvoir être
    utilisés sur tous les objectifs.

    Un objectif définit un but qu'un équipage doit attendre. Ils peuvent
    être de forme diverses, comme rejoindre un point précis, suivre un
    navire, le rattraper ou se mettre en formation sur lui. En fonction
    des objectifs actuels, un capitaine ou second (PNJ) donnera la suite
    d'ordres nécessaires à leur accomplissement.

    En réalité, un objectif décrit de façon aussi succinte et abstraite
    que possible un but à atteindre. L'objectif sera ensuite décomposé
    en contrôles (étape intermédiaire facultative), un contrôle étant
    un objectif intermédiaire clairement nommé. Par exemple, il existe
    un contrôle pour contrôler la vitesse : disons que le navire veut se
    former sur un navire B, il va créer deux contrôles, le premier pour
    obtenir la même vitesse que le navire B et le second pour contrôler
    la direction (la même que le navire B). Le contrôle de vitesse notamment
    est très délicat et le commandant en charge décidera du nombre de
    voiles ou de rames actives en fonction du besoin.

    """

    cle = None
    def __init__(self, equipage):
        BaseObj.__init__(self)
        self.equipage = equipage
