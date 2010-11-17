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

## Constantes
ENCODAGES = [
    'Utf-8',
    'Latin-1',
    'cp850',
    'cp1252',
]

class ChangerEncodage(Contexte):
    """Contexte de changement d'encodage.
    On affiche au client plusieurs possibilités d'encodage.
    Il est censé afficher celui qu'il voit correctement.
    On part du principe que l'encodage de sortie est le même que l'encodage
    d'entrée. Ainsi, une fois que le client a choisi son encodage, on le
    répercute sur l'encodage du client.
    
    """
    def __init__(self):
        """Constructeur du contexte"""
        Contexte.__init__(self, "connex:creation:changer_encodage")
        self.opts.ncod = False # On devra passer à 'envoyer' une chaîne de bytes
    
    def get_prompt(self, emt):
        """Message de prompt"""
        # Comme l'option ncod est activée, le préfixe est affiché en dur
        return b""
    
    def accueil(self, emt):
        """Message d'accueil"""
        ret = b"\n------= Choix de l'encodage =-------\n"
        ret += b"Le parametrage de l'encodage est necessaire pour " \
            b"permettre une optimisation\n" \
            b"de l'affichage dans votre client, et ainsi un meilleur " \
            b"confort de jeu.\n" \
            b"Choisissez donc un encodage qui s'affiche correctement chez vous.\n" \
            b"Pour ce faire, entrez le numero correspondant dans la " \
            b"liste ci-dessous :\n"
        test = "Caractères accentués en ".encode('Utf-8').decode()
        for i, encodage in enumerate(ENCODAGES):
            ret += b"\n  " + str(i+1).encode() + b" - " + \
                    test.encode(encodage) + encodage.encode()
        ret += b"\n\n"
        return ret
    
    def deconnecter(self, emt):
        """En cas de décnonexion du joueur, on supprime son compte"""
        type(self).importeur.connex.supprimer_compte(emt.emetteur)
    
    def interpreter(self, emt, msg):
        """Méthode appelée quand un message est réceptionné"""
        # On essaye d'abord de convertir le choix de l'utilisateur
        try:
            choix = int(msg)
            if choix < 1 or choix > len(ENCODAGES):
                raise ValueError
        except ValueError:
            self.envoyer(emt, b"Le nombre entre n'est pas valide.")
        else:
            emt.emetteur.encodage = ENCODAGES[choix - 1]
            self.migrer_contexte(emt, "connex:creation:choisir_pass")
