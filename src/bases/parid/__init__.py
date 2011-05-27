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


"""Ce fichier définit la classe parid, le gestionnaire des IDs sur Vancia.

Une instance de cette classe est créée à la fin du fichier.
Cette instance est passée comme gestionnaire aux objets 'ObjetID'. Dès qu'un
nouvel objet ObjetID est créé, on l'ajoute dans son groupe dans l'objet parid.

Cela permet de garder une trace des objets avec une ID. Notez cependant
que cette trace n'est effective que lors d'une session. Elle permet, par
exemple, à un module qui se décharge et se recharge de récupérer ses objets
manipulés sans avoir besoin de les récupérer depuis les fichiers. Toutefois,
d'une session à l'autre, les objets sont censés être enregistrer dans des
fichiers et récupérés de cette façon.

Mode d'emploi :
*   On importe l'instance 'parid' :
    >>> from bases.parid import parid
*   Cette instance est passée comme gestionnaire des objets ID :
    Dès qu'un objetID est créé, on l'ajoute dans son groupe dans parid. Cela
    est également vrai lors de la récupération d'un ObjetID (méthode
    __setstate__)
*   On peut également demander à 'parid' de stocker des groupes fictifs :
    Ce terme recouvre des objets qui ne sont pas destinés à être enregistrer
    (c'est-à-dire dont la durée de vie n'excède pas une session) mais qui
    doivent être conservé temporérement lors du rechargement d'un module.

Exemple :
    Le module primaire connex manipule des instances de connexion.
    Ces instances n'ont pas à être conservées d'une session à l'autre.
    Par contre, si le module se décharge puis se recharge (pour, par exemple
    apporter des modifications, corriger des bugs, ...), les instances
    de connexion doivent être récupérées.
    Dans ce cas, on demande à 'parid' de stocker un groupe fictif contenant
    les instances de connexion. Ce groupe doit être passé sous la forme d'un
    dictionnaire.
    >>> parid['nom du groupe'] = module.mon_groupe # mon_groupe = {id:objet}
    >>> module.recharger()
    >>> module.mon_groupe = parid['nom du groupe']

"""

import os

from bases.logs import man_logs

CONSTRUIT, CHARGE = 0, 1

class Parid:
    
    """Cette classe est un gestionnaire des objets ID avant tout.
    Elle garde une trace de tous les objets dérivés de 'ObjetID' créés ou
    récupérés depuis des fichiers.
    
    Elle permet également de conserver d'autres objets dans des groupes
    fictifs (voir plus haut).
    
    Dans la hiérarchie du module, les groupes fictifs ou d'identification
    sont stockés à la même enseigne, dans le même dictionnaire.
    Les noms identifiant les groupes fictifs doivent être différents des
    groupes d'identification.
    
    """
    
    def __init__(self):
        """Constructeur du gestionnaire"""
        self.groupes = {} # {nom_groupe:dico_objets}
        self.statut = CONSTRUIT
    
    def __contains__(self, nom_groupe):
        """nom_groupe se trouve ou non dans self.groupes"""
        return nom_groupe in self.groupes
    
    def __getitem__(self, nom_groupe):
        """Retourne le __getitem__ de l'attribut 'groupe'"""
        return self.groupes[nom_groupe]
    
    def __setitem__(self, nom_groupe, objets):
        """On appelle le '__setitem__' de 'self.groupe'.
            nom_groupe - nom du groupe (str)
            objets - groupe sous la forme d'un dictionnaire
        
        Le dictionnaire des objets doit être sous la forme {id:objet}.
        
        """
        self.groupes[nom_groupe] = objets
    
    def get_objet(self, id):
        """Retourne l'objet correspondant à l'ID ou None."""
        nom = id.groupe
        objet = None
        try:
            groupe = self[nom]
        except KeyError:
            groupe = None
        
        if groupe:
            try:
                objet = groupe[id.id]
            except KeyError:
                pass
        
        return objet
    
    @property
    def construit(self):
        """Retourne True si le statut du parid est construit"""
        return self.statut is CONSTRUIT
    
    def se_construit(self):
        """Change son statut en construit"""
        self.statut = CONSTRUIT
    
    def se_charge(self):
        """Change son statut en charge"""
        self.statut = CHARGE

# Création de l'instance
parid = Parid()
