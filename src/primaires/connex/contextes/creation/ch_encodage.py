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
# pereIBILITY OF SUCH DAMAGE.


from primaires.interpreteur.contexte import Contexte

## Constantes
ENCODAGES = [
    'Utf-8',
    'Latin-1',
    'cp850',
    'cp1252',
]

class ChangerEncodage(Contexte):
    """Contexte de changement d'encodage.
    On affiche au client plusieurs pereibilités d'encodage.
    Il est censé afficher celui qu'il voit correctement.
    On part du principe que l'encodage de sortie est le même que l'encodage
    d'entrée. Ainsi, une fois que le client a choisi son encodage, on le
    répercute sur l'encodage du client.
    
    """
    nom = "connex:creation:changer_encodage"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
    
    def get_prompt(self):
        """Message de prompt"""
        return b"Entrez le numero correspondant dans la liste ci-dessus :\n"
    
    def accueil(self):
        """Message d'accueil"""
        ret = b"\n|tit|------= Choix de l'encodage =-------|ff|\n"
        ret += b"Le parametrage de l'encodage est necessaire pour " \
            b"permettre une optimisation\n" \
            b"de l'affichage dans votre client, et ainsi un meilleur " \
            b"confort de jeu.\n" \
            b"Choisissez donc un |ent|encodage|ff| qui s'affiche " \
            b"correctement a votre ecran.\n" \
            b"|att|NB : si plusieurs encodages sont disponibles, choisissez " \
            b"le premier d'entre eux.|ff|\n"
        test = "Caractères accentués en "
        for i, encodage in enumerate(ENCODAGES):
            ret += b"\n  " + str(i+1).encode() + b" - " + \
                    test.encode(encodage) + encodage.encode()
        return ret

    def deconnecter(self):
        """En cas de décnonexion du client, on supprime son compte"""
        type(self).importeur.connex.supprimer_compte(self.pere.compte)
    
    def interpreter(self, msg):
        """Méthode appelée quand un message est réceptionné"""
        # On essaye d'abord de convertir le choix de l'utilisateur
        try:
            choix = int(msg)
            if choix < 1 or choix > len(ENCODAGES):
                raise ValueError
        except ValueError:
            self.pere.envoyer(b"Le nombre entre n'est pas valide.")
        else:
            self.pere.compte.encodage = ENCODAGES[choix - 1]
            self.migrer_contexte("connex:creation:choisir_pass")
