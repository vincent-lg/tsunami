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
from bases.collections.liste_id import ListeID
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
    _version = 2
    def __init__(self, cle=""):
        """Constructeur d'un type"""
        ObjetID.__init__(self)
        self.cle = cle
        self.no = 0 # nombre d'objets créés sur ce prototype
        self.nom_singulier = "un objet indéfini"
        self.etat_singulier = "est posé là"
        self.nom_pluriel = "objets indéfinis"
        self.etat_pluriel = "sont posés là"
        self.description = Description(parent=self)
        self.objets = ListeID()
    
    def __getnewargs__(self):
        return ()
    
    def __str__(self):
        return self.cle
    
    def get_nom(self, nombre):
        """Retourne le nom complet en fonction du nombre.
        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel
        
        """
        if nombre <= 0:
            raise valueError("la focntion get_nom_pluriel a été appelée " \
                    "avec un  nombre négatif ou nul.")
        elif nombre == 1:
            return self.nom_singulier
        else:
            return str(nombre) + " " + self.nom_pluriel
    
    def get_nom_etat(self, nombre):
        """Retourne le nom et l'état en fonction du nombre."""
        nom = self.get_nom(nombre)
        if nombre == 1:
            return nom + " " + self.etat_singulier
        else:
            return nom + " " + self.etat_pluriel
    
    # Actions sur les objets
    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        salle = personnage.salle
        moi = "Vous regardez {} :".format(self.nom_singulier)
        autre = "{} regarde {}.".format(personnage.nom, self.nom_singulier)
        description = str(self.description)
        if not description:
            description = "Il n'y a rien de bien intéressant à voir."
        
        moi += "\n\n" + description
        salle.envoyer(autre, (personnage, ))
        return moi

ObjetID.ajouter_groupe(BaseType)
