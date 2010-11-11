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


from primaires.interpreteur.contexte import Contexte

import re

## Constantes
# Regex
RE_NOM_VALIDE = re.compile(r"^[A-Za-z0-9]{3,15}$", re.I)

class NouveauNom(Contexte):
    """Premier contexte appelé à la création d'un compte.
    On demande simplement au client d'entrer un nom de compte valide.
    Plusieurs sorties possibles :
    *   Le client entre un nom de compte existant(les noms de compte
        ne sont pas sensibles à la casse)
    *   Le client entre un nom de compte valide :
        Dans ce cas, on redirige vers 'connex:creation:entrer_ncod'
    *   Le client entre un nom de compte invalide
    
    """
    def __init__(self):
        """Constructeur du contexte"""
        Contexte.__init__(self, "connex:creation:entrer_nom")
        self.opts.emt_ncod = False
        self.opts.sup_accents = True
    
    def get_prompt(self, emt):
        """Message de prompt"""
        return "Nouveau nom de compte : "
    
    def accueil(self, emt):
        """Message d'accueil"""
        return \
            "\n\n" \
            "    Entrez le nom de votre nouveau compte.\n" \
            "    Ce nom vous sera demandé à chaque connexion.\n" \
            "    Les caractères spéciaux ne sont pas autorisés dans ce nom.\n" \
            "    Les noms de compte ne sont pas sensibles à la casse."
    
    def interpreter(self, emt, msg):
        """Méthode appelée quand un message est réceptionné"""
        # On passe le message en minuscule
        msg = msg.lower()
        if msg in type(self).importeur.connex.nom_comptes:
            self.envoyer(emt, "Ce nom de compte est déjà réservé.")
        elif RE_NOM_VALIDE.search(msg):
            # On crée le compte correspondant
            compte = type(self).importeur.connex.ajouter_compte(msg)
            emt.emetteur = compte
            self.migrer_contexte(emt, "connex:creation:changer_encodage")
        else:
            self.envoyer(emt, "nom invalide")
