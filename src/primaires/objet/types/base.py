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


"""Ce fichier contient la classe BaseType, détaillée plus bas."""

from abstraits.id import ObjetID
from primaires.format.description import Description
from . import MetaType

class BaseType(ObjetID, metaclass=MetaType):
    
    """Classe abstraite représentant le type de base d'un objet.
    Si des données doivent être communes à tous les types d'objet
    (un objet a un nom, une description, quelque soit son type) c'est dans
    cette classe qu'elles apparaissent.
    
    """
    
    groupe = "prototypes_objets"
    sous_rep = "objets/prototypes"
    nom_type = "" # à redéfinir
    _nom = "base_type_objet"
    _version = 1
    def __init__(self, identifiant=""):
        """Constructeur d'un type"""
        ObjetID.__init__(self)
        self.identifiant = identifiant
        self.nom_singulier = ""
        self.etat_singulier = ""
        self.nom_pluriel = ""
        self.etat_pluriel = ""
        self.description = Description(parent=self)
    
    def __getinitargs__(self):
        return ()

ObjetID.ajouter_groupe(BaseType)
