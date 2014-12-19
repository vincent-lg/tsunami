# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Package postes contenant les différents postes.

Chaque poste est dans un fichier distinct.

La définition d'un poste se fait dans la classe Poste, détaillée plus bas.
Ce fichier contient également la métaclasse des postes, MetaPoste.

"""

postes = {}

class MetaPoste(type):

    """Métaclasse des postes disponibles pour un membre d'équipage.

    Elle ajoute le poste dans le dictionnaire 'postes' si il possède
    un nom.

    """

    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        type.__init__(cls, nom, bases, contenu)
        if cls.nom:
            postes[cls.nom] = cls()

class Poste(metaclass=MetaPoste):

    """Classe définissant un poste occupé par un membre d'équipage.

    Les attributs d'un poste sont :
        nom -- le nom du poste
        autorite -- un entier définissant l'autorité du poste
        nom_parent -- le nom du poste parent

    """

    nom = ""
    points = 0
    def __init__(self):
        """Constructeur du poste."""
        self.autorite = 0
        self.nom_parent = ""

    @property
    def parent(self):
        """Retourne le poste parent si existe ou None sinon."""
        return postes.get(self.nom_parent)

    def __repr__(self):
        return "<poste {}>".format(repr(self.nom))

    def __str__(self):
        return self.nom

from . import capitaine
from . import second
from . import maitre_equipage
from . import officier
from . import matelot
from . import artilleur
from . import voilier
from . import charpentier
from . import vigie
from . import rameur
from . import chirurgien
from . import maitre_cuisinier
