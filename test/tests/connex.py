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

from tests import EchecTest, test

#Nom du test qui sera afficher en console
nom = "Test des créations de compte et des connexions"

class AfficherMOTD(test):
    
    nom = "AfficherMOTD"
    
    def test(self):
        self.cl = client.Client(self.smtp)
        message = self.cl.connecter()
        try:
            message.index(b"Bienvenue sur")
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide",self.cl.com)
        try:
            message.index(b"Votre compte")
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide",self.cl.com)

class EntrerNom(test):
    
    nom = "EntrerNom"
    
    def sendNom(self,nom):
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        return self.cl.envoyer(nom.encode())
    
    def test(self):
        message = self.sendNom("nouveau")
        try:
            message.index(b"Votre nom de compte")
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide",self.cl.com)
        
        message = self.sendNom("test")
        try:
            message.index(b"Ce compte n'existe pas.")
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide",self.cl.com)

class EntrerPass(test):
    
    nom = "EntrerPass"
    
    def test(self):
        
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        try:
            self.cl.creer_compte("nicolas", "123456", "nicolas@orange.fr")
        except EchecTest as inst:
            raise EchecTest("Impossible de crée le compte : " + str(inst), \
                self.cl.com)
        
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        message = self.cl.envoyer(b"nicolas")
        try:
            message.index(b"")#TODO
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide", self.cl.com)

class NouveauNom(test):
    
    nom = "NouveauNom"
    nom_valide = ["Lea","Bastien","JeanneFrancoise","tictac42","Nitrate"]
    nom_invalide = ["nouveau","kassie","Kassie","Al","Léa", \
        "MichelFrancois325","JeannineHuguette","Jean-Marc","François"]
    
    def mettre_nom(self,nom):
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        self.cl.envoyer(b"nouveau")
        return self.cl.envoyer(nom.encode())
        
    def test(self):
        message = self.mettre_nom("/")
        try:
            message.index(b"Votre compte")
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide, pour revenir en arrière", self.cl.com)
        
        for nom in self.nom_valide:
            message = self.mettre_nom(nom)
            try:
                message.index(b"Choix de l'encodage")
            except ValueError:
                raise EchecTest("Le nom {0} n'a pas été accepté".format(nom), \
                    self.cl.com)
        
        for nom in self.nom_invalide:
            message = self.mettre_nom(nom)
            try:
                message.index(b"Votre nom de compte :")
            except ValueError:
                raise EchecTest("Le nom {0} a été accepté".format(nom), \
                    self.cl.com)
        
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        self.cl.envoyer(b"nouveau")
        try:
            self.cl.creer_compte("Marie", "Blabla", "marie@orange.fr")
        except EchecTest as detail:
            raise EchecTest("Impossible de crée le compte : " + str(detail), \
                self.cl.com)
        message = self.mettre_nom("Marie")
        try:
            message.index(b"Votre nom de compte :")
        except ValueError:
            raise EchecTest("Un nom de compte a été accepté deux fois", \
                self.cl.com)

class ChangeEncodage(test):
    
    nom = "ChangeEncodage"
    
    def mettre_encodage(self,encodage):
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        self.cl.envoyer(b"nouveau")
        self.cl.envoyer(b"Titus")
        return self.cl.envoyer(encodage.encode())
    
    def test(self):
        message = self.mettre_encodage("0")
        try:
            message.index(b"Entrez le numero correspondant")
        except ValueError:
            raise EchecTest("0 accepté comme encopage", self.cl.com)
        
        message = self.mettre_encodage("1")
        try:
            message.index("prétexte".encode('Utf-8'))
        except ValueError:
            raise EchecTest("Erreur lors du choix de l'encodage 1", self.cl.com)
        
        message = self.mettre_encodage("2")
        try:
            message.index("prétexte".encode('Latin-1'))
        except ValueError:
            raise EchecTest("Erreur lors du choix de l'encodage 2", self.cl.com)
        
        message = self.mettre_encodage("3")
        try:
            message.index("prétexte".encode('cp850'))
        except ValueError:
            raise EchecTest("Erreur lors du choix de l'encodage 3", self.cl.com)
        
        message = self.mettre_encodage("4")
        try:
            message.index("prétexte".encode('cp1252'))
        except ValueError:
            raise EchecTest("Erreur lors du choix de l'encodage 4", self.cl.com)
        
        message = self.mettre_encodage("5")
        try:
            message.index(b"Entrez le numero correspondant")
        except ValueError:
            raise EchecTest("5 accepté comme encodage", self.cl.com)

class ChoisirPass(test):
    
    nom = "ChoisirPass"
    mdp_valide = ["123456","Bastien","tictac42","{"*8,"}"*8,"/"*8, \
        "["*8,"]"*8,"("*8,")"*8,"+"*8,"="*8,"$"*8,"_"*8,"*"*8,"@"*8,"^"*8, \
        "\""*8,"'"*8,"`"*8,"£"*8,"#"*8,"-"*8]
    mdp_invalide = ["totor","oubli","flané32","\\"*8]
    
    def mettre_mdp(self,mdp):
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        self.cl.envoyer(b"nouveau")
        self.cl.envoyer(b"potter")
        self.cl.envoyer(b"1")
        return self.cl.envoyer(mdp.encode())
        
    def test(self):
        message = self.mettre_mdp("/")
        try:
            message.index(b"Choix de l'encodage")
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide, pour revenir en arrière", self.cl.com)
        
        for mdp in self.mdp_valide:
            message = self.mettre_mdp(mdp)
            try:
                message.index(b"Confirmez le mot de passe :")
            except ValueError:
                raise EchecTest("Le mot de passe : {0} n'a pas été " \
                    "accepté".format(mdp), self.cl.com)
        
        for mdp in self.mdp_invalide:
            message = self.mettre_mdp(mdp)
            try:
                message.index(b"Votre mot de passe :")
            except ValueError:
                raise EchecTest("Le mot de passe : {0} a " \
                    "été accepté".format(mdp), self.cl.com)

class ConfirmerPass(test):
    
    nom = "ConfirmerPass"
    
    def mettre_mdp(self,mdp):
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        self.cl.envoyer(b"nouveau")
        self.cl.envoyer(mdp.encode())
        self.cl.envoyer(b"1")
        return self.cl.envoyer(mdp.encode())
        
    def test(self):
        self.mettre_mdp("test22")
        message = self.cl.envoyer(b"/")
        try:
            message.index(b"Votre mot de passe :")
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide, pour revenir en arrière", self.cl.com)
        
        self.mettre_mdp("test42")
        message = self.cl.envoyer(b"test42")
        try:
            message.index(b"Votre adresse mail :")
        except ValueError:
            raise EchecTest("Un mot de passe n'a pas été confirmé", self.cl.com)
        
        self.mettre_mdp("test21")
        message = self.cl.envoyer(b"test42")
        try:
            message.index(b"Confirmez le mot de passe :")
        except ValueError:
            raise EchecTest("Un mot de passe a été confirmé")

import asyncore
import time

class EntrerEmail(test):
    
    nom = "EntrerEmail"
    nom_compte = 100000
    mail_valide = ["test@test.com", "bruno@maitredumonde.fr", \
        "blabla@un.grand.nom.de.domaine.fr","test@test.info"]
    mail_invalide = ["essaye","essaye@encore","blabla@aa.a","test@fr", \
        "test@test.francais","français@test.fr","test@français.fr"]
    
    def mettre_mail(self,email):
        self.nom_compte += 1
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        self.cl.envoyer(b"nouveau")
        self.cl.envoyer(str(self.nom_compte).encode())
        self.cl.envoyer(b"1")
        self.cl.envoyer(str(self.nom_compte).encode())
        self.cl.envoyer(str(self.nom_compte).encode())
        return self.cl.envoyer(email.encode())
        
    def test(self):
        message = self.mettre_mail("/")
        try:
            message.index(b"Votre adresse mail")
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide, en essayent de revenir en arrière", self.cl.com)
        
        
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        try:
            self.cl.creer_compte("bruno", "maitredumonde", "bruno@mdm.com")
        except EchecTest as detail:
            raise EchecTest("Impossible de crée le compte : " + str(detail), \
                self.cl.com)
        
        message = self.mettre_mail("bruno@mdm.com")
        try:
            message.index(b"Votre adresse mail")
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide, en essayent de revenir en arrière", self.cl.com)
        
        for mail in self.mail_valide:
            message = self.mettre_mail(mail)
            try:
                message.index(b"Code de validation :")
            except ValueError:
                raise EchecTest("Le mail : {0} n'a pas été " \
                    "accepté".format(mail), self.cl.com)
        
        for mail in self.mailmail_invalide:
            message = self.mettre_mail(mail)
            try:
                message.index(b"Votre mot de passe :")
            except ValueError:
                raise EchecTest("Le mail : {0} a été accepté".format(mail), \
                    self.cl.com)

class Validation(test):
    
    nom = "Validation"
    nom_compte = 100000
    
    def ask_validation(self):
        self.nom_compte += 1
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        self.cl.envoyer(b"nouveau")
        self.cl.envoyer(str(self.nom_compte).encode())
        self.cl.envoyer(b"1")
        self.cl.envoyer(str(self.nom_compte).encode())
        self.cl.envoyer(str(self.nom_compte).encode())
        
        return self.cl.envoyer((str(self.nom_compte) + "@free.fr").encode())
        
    def test(self):
        self.ask_validation()
        message = self.cl.envoyer(b"/")
        try:
            message.index(b"Votre adresse mail :")
        except ValueError:
            raise EchecTest("Réponse attendu de la part de Kassie " \
                "invalide, pour revenir en arrière", self.cl.com)
        
        self.ask_validation()
        adresse = (str(self.nom_compte) + "@free.fr").encode()
        mail = self.smtp.attendre_message_de(1,adresse)
        if mail == None:
            raise EchecTest("Mail de validation non reçue",self.cl.com)
        code = self.cl.extraire_code(mail)
        message = self.cl.envoyer(str(code).encode())
        try:
            message.index(b"Choix du personnage")
        except ValueError:
            raise EchecTest("Validation classique impossible", self.cl.com)
        
        self.ask_validation()
        adresse = (str(self.nom_compte) + "@free.fr").encode()
        mail = self.smtp.attendre_message_de(1,adresse)
        if mail == None:
            raise EchecTest("Mail de validation non reçue",self.cl.com)
        self.cl = client.Client(self.smtp)
        self.cl.connecter(str(self.nom_compte),str(self.nom_compte))
        code = self.cl.extraire_code(mail)
        message = self.cl.envoyer(str(code).encode())
        try:
            message.index(b"Choix du personnage")
        except ValueError:
            raise EchecTest("Validation après reconnexion impossible", \
                self.cl.com)
        
        self.ask_validation()
        adresse = (str(self.nom_compte) + "@free.fr").encode()
        mail = self.smtp.attendre_message_de(1,adresse)
        if mail == None:
            raise EchecTest("Mail de validation non reçue",self.cl.com)
        code = self.cl.extraire_code(mail)
        message = self.cl.envoyer("")
        message = self.cl.envoyer("")
        message = self.cl.envoyer("")
        mail = self.smtp.attendre_message_de(1,adresse)
        if mail == None:
            raise EchecTest("Mail de validation non reçue",self.cl.com)
        code = self.cl.extraire_code(mail)
        message = self.cl.envoyer(str(code).encode())
        try:
            message.index(b"Choix du personnage")
        except ValueError:
            raise EchecTest("Validation après 3 tentatives impossible", \
                self.cl.com)
        

class Connexion(test):
    
    nom = "Connexion"
    
    nom_compte = ["Bastien","JeanneFrancoise","tictac42","Nitrate"]
    mdp = ["123456","Bastien","tictac42"]
    email = ["test@test.com"]
    
    rand_nom = 100000
    
    def testCompte(self, nom, mdp, mail):
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        self.cl.creer_compte(nom,mdp,mail)
        self.cl = client.Client(self.smtp)
        self.cl.connecter()
        self.cl.connexion(nom, mdp)
    
    def test(self):
        for nom in self.nom_compte:
            self.testCompte(nom, nom, nom + "@free.fr")
        for mdp in self.mdp:
            self.rand_nom += 1
            self.testCompte(str(self.rand_nom), mdp, \
                str(self.rand_nom) + "@free.fr")
        for mail in self.email:
            self.rand_nom += 1
            self.testCompte(str(self.rand_nom), str(self.rand_nom), mail)
            
