# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Ce package contient les différents types d'objet, sous la forme
d'une classe par fichier, héritée de BaseType (voir base.py).

"""

from abstraits.obase import MetaBaseObj

types = {} # types d'objet {nom:classe}

class MetaType(MetaBaseObj):
    
    """Métaclasse des types d'objet.
    
    Elle ajoute le type de l'objet dans le dictionnaire 'types' si il possède
    un nom.
    
    """
    
    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        MetaBaseObj.__init__(cls, nom, bases, contenu)
        cls.types = {}
        if cls.nom_type:
            types[cls.nom_type] = cls
            
            # On l'ajoute dans la classe-mère
            base = bases and bases[0] or None
            if base:
                base.types[cls.nom_type] = cls

from .bijou import Bijou
from .cible import Cible
from .clef import Clef
from .conteneur import Conteneur
from .conteneur_potion import ConteneurPotion
from .conteneur_nourriture import ConteneurNourriture
from .flechette import Flechette
from .indefini import *
from .livre import Livre
from .potion import Potion
from .nourriture import Nourriture
from .pierre_feu import PierreFeu
from .vetement import Vetement

# Nourriture
from .viande import *
from .legume import *
from .fruit import *
from .gateau import *

from .assiette import Assiette
from .bol import Bol

# Vêtements
from .cape import Cape
from .ceinture import Ceinture
from .chapeau import Chapeau
from .chaussette import Chaussette
from .chaussure import Chaussure
from .chemise import Chemise
from .ceinture import Ceinture
from .gant import Gant
from .jupe import Jupe
from .pantalon import Pantalon
from .robe import Robe
from .tunique import Tunique
from .veste import Veste

# Bijoux
from .bague import Bague
from .boucle_oreille import BoucleOreille
from .bracelet import Bracelet
from .collier import Collier

# Cadavre
from .cadavre import Cadavre

# Matériau
from .matiere import Matiere
from .fourrure import Fourrure

from .boule_neige import BouleNeige
