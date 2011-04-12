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

# Message de validation
msg_validation = \
    "Votre demande de création de compte a bien été enregistrée.\n" \
    "Pour valider ce compte, vous devez entrer le code ci-dessous dans " \
    "votre client.\n\n" \
    "Votre code de validation : {code}\n\n" \
    "Note : si vous avez été déconnecté du jeu dans l'intervalle, " \
    "reconnectez-vous. En entrant le nom de votre compte nouvellement créé " \
    "puis votre mot de passe, vous serez automatiquement redirigé vers " \
    "l'étape de validation où le code vous sera demandé pour valider le " \
    "compte et pouvoir, enfin, commencer à jouer."

from random import randrange

def generer_code():
    """Fonction chargée de générer un code aléatoire
    Elle retourne le code sous la forme d'une chaîne.
    
    """
    caracteres = "0123456789" # caractères constituant le code
    taille = 6 # taille du code de validation
    code = ""
    for i in range(taille):
        code += caracteres[randrange(len(caracteres))]
    
    print("Code:", code)
    return code


class Validation(Contexte):
    """Contexte de validation.
    On envoie un mail au client contenant un code pour valider son compte.
    Si le client entre trois fois de suite un code héroné, on renvoie un
    nouveau code.
    
    """
    nom = "connex:creation:validation"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.rci_ctx_prec = "connex:creation:entrer_email"
    
    def entrer(self):
        """Méthode appelée quand emt entre dans le contexte"""
        if not self.pere.compte.code_validation:
            # Le message de validation n'a pas été envoyé
            # Génération du code de validation
            code = generer_code()
            self.pere.compte.code_validation = code
            destinateur = "info"
            destinataire = self.pere.compte.adresse_email
            sujet = "Validation de votre compte - {0}".format( \
                    self.pere.compte.nom.capitalize())
            corps = msg_validation.format(code = code)
            type(self).importeur.email.envoyer(destinateur, destinataire, \
                    sujet, corps)
    
    def get_prompt(self):
        """Message de prompt"""
        return "Code de validation : "
    
    def accueil(self):
        """Message d'accueil"""
        return \
            "\n|tit|------= Validation du compte =------|ff|\n" \
            "Un message automatique vient d'être envoyé à l'adresse :\n" \
            "- {0} -\n" \
            "Il contient un code de validation que vous devez recopier ici.\n" \
            "|att|Ce code permet de valider votre compte, il est donc " \
            "indispensable.|ff|".format(self.pere.compte.adresse_email)
    
    def interpreter(self, msg):
        """Interpréteur du contexte"""
        if msg == self.pere.compte.code_validation:
            self.pere.compte.valide = True
            self.pere.compte.code_validation = ""
            self.pere.compte.tentatives_validation = 0
            self.pere.envoyer( \
                "\n|att|Félicitations, votre compte a bien été validé !|ff|\n\n" \
                "Vous pouvez maintenant commencer à créer un personnage...")
            self.migrer_contexte("connex:connexion:choix_personnages")
        else:
            self.pere.compte.tentatives_validation += 1
            if self.pere.compte.tentatives_validation == 3:
                # Génération d'un nouveau code de validation
                code = generer_code()
                self.pere.compte.code_validation = code
                destinateur = "info"
                destinataire = self.pere.compte.adresse_email
                sujet = "Validation de votre compte - {0}".format( \
                        self.pere.compte.nom.capitalize())
                corps = msg_validation.format(code = code)
                type(self).importeur.email.envoyer(destinateur, destinataire, \
                    sujet, corps)
                self.pere.compte.tentatives_validation = 0
                self.pere.envoyer( \
                    "|err|Vous avez entré trois codes de validation erronés " \
                    "de suite ;\n" \
                    "un nouveau code de validation vient de vous être " \
                    "envoyé.|ff|")
            else:
                self.pere.envoyer("|err|Votre code de validation est " \
                    "incorrect.|ff|")
