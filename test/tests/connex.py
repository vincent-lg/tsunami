# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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

import client

import tests

nom = "Test des créations de compte et des connexions"

"""
EntrerPass
ChoisirPersonnage

ChangerEncodage
ChoisirPass
ConfirmerPass
EntrerEmail
Validation
"""

class AfficherMOTD(tests.test):
    
    nom = "AfficherMOTD"
    
    def test(self):
        cl = client.client(self.smtp)
        message = cl.connect()
        message.index(b"Bienvenue sur")


class EntrerNom(tests.test):
    
    nom = "EntrerNom"
    
    def test(self):
        cl = client.client(self.smtp)
        message = cl.connect()
        message.index(b"Votre compte")
        message = cl.envoyer(b"nouveau")
        message.index(b"Creation d'un compte")
        
        cl = client.client(self.smtp)
        cl.connect()
        message = cl.envoyer(b"test")
        message.index(b"Ce compte n'existe pas.")


class EntrerPass(tests.test):
    
    nom = "EntrerPass"
    
    def test(self):
        
        cl = client.client(self.smtp)
        cl.connect()
        cl.creer_compte("nicolas", "123456", "nicolas@orange.fr")
        
        cl = client.client(self.smtp)
        cl.connect()
        message = cl.envoyer(b"nicolas")
        message.index(b"")

class nouveau_nom(tests.test):
    
    nom = "nouveau_nom"
    nom_valide = ["Lea","Bastien"]
    nom_invalide = ["nouveau","Al","Léa"]
    
    def mettre_nom(self,nom):
        cl = client.client(self.smtp)
        cl.connect()
        cl.envoyer(b"nouveau")
        return cl.envoyer(nom.encode())
        
    def test(self):
        cl = client.client(self.smtp)
        cl.connect()
        message = cl.envoyer(b"nouveau")
        message.index(b"Creation d'un compte")
        
        message = self.mettre_nom("/")
        message.index(b"Votre compte")
        
        for nom in self.nom_valide:
            try:
                message = self.mettre_nom(nom)
                message.index(b"Choix de l'encodage")
            except Exception as inst:
                raise(Exception("Erreur nom de compte : {0} : {1} ({2})".format(nom,inst,message)))
        
        for nom in self.nom_invalide:
            try:
                message = self.mettre_nom(nom)
                message.index(b"Votre nom de compte :")
            except Exception as inst:
                raise(Exception("Erreur nom de compte : {0} : {1} ({2})".format(nom,inst,message)))

class nouveau_compte(tests.test):
    nom = "Créer un nouveau compte"
    
    def test(self):
        cl = client.client(self.smtp)
        cl.connect()
        return cl.creer_compte("arthur", "123456", "arthur@free.fr")

class connexion(tests.test):
    nom = "Connexion"
    
    def test(self):
        cl = client.client(self.smtp)
        cl.connect()
        cl.creer_compte("jean", "azerty", "jean@alice.fr")
        cl = client.client(self.smtp)
        cl.connect()
        return cl.connexion("jean", "azerty")
