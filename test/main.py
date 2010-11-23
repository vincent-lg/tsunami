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
import client
import kassie

import os.path
import shutil
import time
import traceback
import sys

import tests

#TODO Faire des dépendances de test et un tri automatique
#TODO Mieux gérer l'effacement du dossier kassie
#TODO Mieux gérer les exceptions dans les tests(affichage et tout)
#TODO vérifier les conventions de nommage des variables et classes

rep_kassie="./kassie"

if os.path.exists(rep_kassie):
    print("Effacer " + rep_kassie)
    exit()

serveur = kassie.kassie(rep_kassie)
serveur.change("email","nom_hote","localhost")

liste_tests = {}
for testeur in tests.testeurs:
    __import__("tests." + testeur)
    testeur = getattr(tests,testeur)
    liste_tests[testeur] = []
    for obj in dir(testeur):
        obj = getattr(testeur,obj)
        if (type(obj)==type) and issubclass(obj, tests.test):
            liste_tests[testeur].append(obj)

align = 50

for testeur in liste_tests.keys():
    print(testeur.nom + " : ")
    echec = 0
    for test in liste_tests[testeur]:
        serveur.start()
        sm = smtp.smtp()
        instance = test(sm)
        msg = "\t- {0} :".format(instance.nom)
        msg += " " * (align-len(msg))
        print(msg, end="")
        try:
            instance.test()
            print("\033[32mRéussi\033[0m")
        except Exception as inst:
            print("\033[31mEchoué\033[0m")
            _, _, trace = sys.exc_info()
            traceback.print_tb(trace)
            print(inst)
            echec += 1
        serveur.stop()
        sm.close()
    if (echec==0):
        print("\033[32mTous les tests ont été réussis\033[0m")
    else:
        print("\033[31m{0} tests ont échoué\033[0m".format(echec))

