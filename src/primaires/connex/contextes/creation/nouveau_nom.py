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
RE_NOM_VALIDE = re.compile(r"^[A-Za-z0-9]+$", re.I)

class NouveauNom(Contexte):
    """Premier contexte appelé à la création d'un compte.
    On demande simplement au client d'entrer un nom de compte valide.
    Plusieurs sorties possibles :
    *   Le client entre un nom de compte existant (les noms de compte
        ne sont pas sensibles à la casse)
    *   Le client entre un nom de compte invalide
    Dans ces deux cas on boucle sur le contexte.
    *   Le client entre un nom de compte valide
    Là, on redirige vers 'connex:creation:changer_enodage'.
    
    """
    nom = "connex:creation:entrer_nom"
    
    def __init__(self, poss):
        """Constructeur du contexte"""
        Contexte.__init__(self, poss)
        self.opts.sup_accents = True
        self.opts.rci_ctx_prec = "connex:connexion:entrer_nom"
    
    def get_prompt(self):
        """Message de prompt"""
        return "Votre nom de compte : "
    
    def accueil(self):
        """Message d'accueil"""
        return \
            "\n|tit|------= Création d'un compte =------|ff|\n" \
            "Bienvenue dans notre monde !\n" \
            "Entrez un |cmd|nom|ff| pour créer un compte, ou |cmd|/|ff| pour " \
			"revenir à l'écran précédent.\n" \
            "Ce |cmd|nom|ff| vous sera demandé à chaque connexion, ne " \
            "l'oubliez pas !"
    
    def interpreter(self, msg):
        """Méthode appelée quand un message est réceptionné"""
        cfg_connex = type(self).importeur.anaconf.get_config("connex")
        noms_interdits = list(cfg_connex.noms_interdits)
        noms_interdits.append(cfg_connex.chaine_nouveau)
        min = cfg_connex.taille_min
        max = cfg_connex.taille_max
        
        # On passe le message en minuscules
        msg = msg.lower()
        if msg in noms_interdits:
            self.poss.envoyer("|err|Ce nom de compte est interdit. " \
                    "Choisissez-en un autre.|ff|")
        elif msg in type(self).importeur.connex.nom_comptes:
            self.poss.envoyer("|err|Ce nom de compte est déjà réservé.|ff|")
        elif len(msg) < min or len(msg) > max:
            self.poss.envoyer("|err|Le nom doit faire entre {0} et {1} " \
                            "caractères de longueur.|ff|".format(min, max))
        elif RE_NOM_VALIDE.search(msg) is None:
            self.poss.envoyer("|err|Les caractères spéciaux ne sont pas " \
                            "autorisés.|ff|")
        else:
            # On crée le compte correspondant
            compte = type(self).importeur.connex.ajouter_compte(msg)
            self.poss.emetteur = compte
            self.migrer_contexte("connex:creation:changer_encodage")
