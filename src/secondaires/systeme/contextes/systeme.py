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


"""Fichier contenant le contexte 'systeme'"""

import sys
import traceback

from primaires.format.constantes import ponctuations_finales

from primaires.interpreteur.contexte import Contexte

class Systeme(Contexte):
    
    """Contexte permettant d'entrer du code Python.
    
    """
    
    nom = "systeme:python_console"
    
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.prompt_prf = ""
        self.opts.prompt_clr = ""
        self.espace = {}
    
    def __getstate__(self):
        attrs = Contexte.__getstate__(self)
        attrs["espace"] = {}
        return attrs
    
    def get_prompt(self):
        """Retourne le prompt"""
        return ">>> "
    
    def accueil(self):
        """Message d'accueil du contexte"""
        res = "|tit|Console Python|ff|\n\n" \
            "Vous pouvez entrer ici du code Python et voir le résultat " \
            "des instructions\nque vous entrez.\n" \
            "Vous pouvez utilisez la variable |cmd|importeur|ff| " \
            "qui contient, comme\nson nom l'indique, l'importeur et par " \
            "extension, une bonne partie de Kassie.\n" \
            "|att|Tapez |ff||cmd|/q|ff||att| pour quitter.|ff|\n\n" \
            "|tit|Python {}|ff|\n\n".format(sys.version)
        
        return res
    
    def interpreter(self, msg):
        """Méthode d'interprétation du contexte"""
        self.espace["importeur"] = type(self).importeur
        if msg.startswith("/"):
            msg = msg[1:]
            if msg == "q":
                self.pere.joueur.contextes.retirer()
                self.pere << "Fermeture de la console Python."
            else:
                self.pere << "|err|Option inconnue.|ff|"
        else:
            # Exécution du code
            sys.stdin = self.pere
            sys.stdout = self.pere
            nb_msg = self.pere.nb_msg
            try:
                exec(msg, self.espace)
            except Exception:
                self.pere << traceback.format_exc()
            else:
                if self.pere.nb_msg == nb_msg:
                    self.pere.envoyer("")
            finally:
                sys.stdin = sys.__stdin__
                sys.stdout = sys.__stdout__
