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


"""Fichier contenant la classe Matelot, détaillée plus bas."""

from abstraits.id import ObjetID

class Matelot(ObjetID):
    
    """Un matelot est un PNJ particulier membre d'un équipage d'un navire.
    
    Si la classe représentant un Matelot n'est pas directement héritée de PNJ,
    c'est surtout pour permettre la transition à la volée d'un PNJ à un
    matelot et inversement. Si un Matelot est hérité de PNJ, alors un
    PNJ doit être déclaré dès le départ comme un Matelot et ne pourra
    plus être modifié par la suite.
    
    Le matelot possède plus spécifiquement :
        un poste de prédilection
        une confiance éprouvée envers le capitaine
    
    Les autres informations sont propres au PNJ et sont accessibles
    directement. La méthode __getattr__ a été construit sur le même
    modèle que celle des objets ou des éléments de navire : si
    l'information n'est pas trouvée dans l'objet, on cherche dans le PNJ.
    
    """
    
    groupe = "matelots"
    sous_rep = "navigation.matelots"
    def __init__(self, personnage):
        """Constructeur du matelot."""
        self.personnage = personnage
        self.nom_poste = "matelot"
        self.confiance = 0
    
    def __getnewargs__(self):
        return (None, )
    
    def __getattr__(self, nom_attr):
        """On cherche l'attribut dans le personnage."""
        return getattr(self.personnage, nom_attr)

ObjetID.ajouter_groupe(Matelot)