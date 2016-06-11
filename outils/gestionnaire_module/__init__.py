# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 DAVY Guillaume
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

import time, sys

from .divers import *
import gestionnaire_module.base
import gestionnaire_module.classe
import gestionnaire_module.commande
import gestionnaire_module.masque
import gestionnaire_module.contexte
import gestionnaire_module.editeur

REPSRC = "src/"

if len(sys.argv) < 5:
    print("Pas assez d'argument, la syntaxe est :\n")
    print("gestionnaire_module module type NOM Prénom\n")
    print("(type = p ou s, p pour primaire, s pour secondaire)")
    sys.exit(1)

module = sys.argv[1].lower()
typeMod = sys.argv[2]
copyright = time.strftime("%Y ") + sys.argv[3] + " " + sys.argv[4]
entete = ENTETE.format(copyright=copyright)

if typeMod == "p":
    typeMod = "primaire"
elif typeMod == "s":
    typeMod = "secondaire"
else:
    print("pas assez d'argument : manager module p/s NOM Prénom")
    sys.exit(1)

rep = REPSRC + typeMod + "s/" + module + "/"

base.init(rep, entete, typeMod, module)

while True:
    cmd = input("Veuillez entrer une commande (help pour de l'aide, quit " \
        "pour quitter) :\n-> ")
    
    cmd = cmd.split()
    if len(cmd) < 1:
        continue
    
    if cmd[0] == "help":
        print("Les différentes commandes possibles sont :")
        print("\t- quit : pour quitter")
        print("\t- classe nom [oui] : crée une classe et éventuellement " \
            "un conteneur associé si oui est précisé")
        print("\t- commande nom_fr nom_en categorie schema : crée une commande")
        print("\t- masque nom [nom_complet] : créé un masque")
        print("\t- editeur nom : créé un éditeur")
        print("\t- contexte nom : créé un contexte")
    elif cmd[0] == "quitter":
        sys.exit(0)
    elif cmd[0] == "classe":
        classe.ajouter(rep, entete, cmd)
    elif cmd[0] == "commande":
        commande.ajouter(rep, module, typeMod, entete, cmd)
    elif cmd[0] == "masque":
        masque.ajouter(rep, module, typeMod, entete, cmd)
    elif cmd[0] == "contexte":
        contexte.ajouter(rep, module, typeMod, entete, cmd)
    elif cmd[0] == "editeur":
        editeur.ajouter(rep, module, typeMod, entete, cmd)
    else:
        print("Commande inconnue")
