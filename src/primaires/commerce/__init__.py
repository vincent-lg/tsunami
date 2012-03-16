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


"""Fichier contenant le module primaire commerce."""

from abstraits.module import *
from . import masques
from . import commandes
from . import types

class Module(BaseModule):
    
    """Cette classe contient les informations du module primaire commerce.
    
    Ce module gère le commerce, c'est-à-dire les transactions, les magasins,
    les monnaies.
    
    Note : on peut étendre ce module en proposant de nouveaux objets pouvant être vendus. Pour cela, il faut :
    1.  Lors de la configuration du module contenant les nouveaux
        objets, on doit signaler au module ocmmerce qu'un nouveau type
        d'objet sera susceptible d'être vendu. Pour cela, il faut ajouter
        une entrée dans le dictionnaire types_services avec en clé le
        nom du nouvel objet et en valeur, un dictionnaire permettant
        de trouver l'objet grâce à sa clé. Pour des exemples, regardez
        le module primaires objet
    2.  La classe produisant des objets pouvant être vendus en magasin
        doit posséder :
        A.  Un attribut de classe type_achat (str)
        B.  Une propriété ou un attribut d'objet valeur (float)
        C.  à voir
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "commerce", "primaire")
        self.commandes = []
        self.types_services = {}
    
    def ajouter_commandes(self):
        """Ajout des commandes"""
        self.commandes = [
            commandes.acheter.CmdAcheter(),
            commandes.lister.CmdLister(),
            commandes.vendre.CmdVendre(),
        ]
        
        for cmd in self.commandes:
            importeur.interpreteur.ajouter_commande(cmd)
