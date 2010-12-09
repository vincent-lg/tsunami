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

import smtp
import kassie
import tests

import os.path
import shutil

#TODO Faire des dépendances de test et un tri automatique
#TODO Remplacer le sed dans Kassie par un regex

#Répertoire qui contiendra les logs, la configuration et la sauvegarde
rep_kassie = os.getcwd() + os.sep + "kassie" + os.sep

#Répertoire qui contiendra les répertoires contenant les erreurs
rep_echec = os.getcwd() + os.sep + "echec" + os.sep

#Vérifie que le répertoire n'existe pas pour pas effacer
#des logs peuvent être important
if os.path.exists(rep_kassie):
    print("Effacer " + rep_kassie)
    exit()

#Vérifie que le répertoire n'existe pas pour pas effacer
#des fichiers qui peuvent être important
if os.path.exists(rep_echec):
    print("Effacer " + rep_echec)
    exit()

#Nombre de caractère pour l'alignement des résultats des tests
align = 35

#Contient la liste des tests qui seront effectué, groupé par module
liste_tests = {}

#Création de Kassie et configuration
serveur = kassie.Kassie(rep_kassie)

#Configuration de Kassie
serveur.change("email","nom_hote","localhost")

#Récupère tous les tests
for testeur in tests.testeurs:
    __import__("tests." + testeur)
    testeur = getattr(tests,testeur)
    liste_tests[testeur] = []
    #Parcourt les objets de chaque module pour extraire
    #les classes dérivants de tests.test
    for obj in dir(testeur):
        obj = getattr(testeur,obj)
        if (type(obj)==type) and issubclass(obj, tests.test):
            liste_tests[testeur].append(obj)

#Effectue tous les tests
for testeur in liste_tests.keys():
    print(testeur.nom + " : ")
    echec = 0
    for test in liste_tests[testeur]:
        #Lancement serveurs
        serveur.start()
        sm = smtp.Smtp()
        instance = test(sm)
        msg = "    - {0} :".format(instance.nom)
        msg += " " * (align-len(msg))
        print(msg, end="")
        try:
            #Lance le test
            instance.test()
            print("\033[32mRéussi\033[0m")
        except tests.EchecTest as detail:
            serveur.stop()
            repertoire = rep_echec + testeur.nom + os.sep + test.nom + os.sep
            os.makedirs(repertoire)
            shutil.copytree(rep_kassie,repertoire + "kassie")
            os.mkdir(repertoire + "/mail")
            index = 0
            for mail in sm.msgs_all:
                f = open(repertoire + "/mail/" + str(index),'w')
                f.write(mail.decode())
                f.close()
            f = open(repertoire + "communication.txt",'w')
            f.write(detail.com)
            f.close()
            f = open(repertoire + "serveur_retour.txt",'w')
            out,debug = serveur.get_retours()
            f.write(str(out))
            f.close()
            f = open(repertoire + "serveur_debug.txt",'w')
            f.write(str(debug))
            f.close()
            print("\033[31mEchoué\033[0m")
            print("        \033[34m"+str(detail)+"\033[0m")
            echec += 1
        #Arrète les serveurs
        sm.close()
        serveur.stop()
    if (echec==0):
        print("\033[32mTous les tests ont été réussis\033[0m")
    else:
        print("\033[31m{0} tests ont échoué\033[0m".format(echec))

shutil.rmtree(rep_kassie)
