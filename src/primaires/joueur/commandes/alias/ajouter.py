# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'ajouter' de la commande 'alias'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmAjouter(Parametre):
    
    """Commande 'alias ajouter'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "ajouter", "add")
        self.schema = "<message>"
        self.aide_courte = "ajoute ou remplace un alias"
        self.aide_longue = \
            "Cette commande permet d'ajouter ou remplacer un alias. " \
            "La syntaxe est simple : vous devez préciser en " \
            "paramètre le nom de l'alias, suivi d'un espace et de " \
            "sa signification. Par exemple |cmd|%alias% %alias:ajouter%|ff| " \
            "|cmd|l look|ff| ajoutera l'alias |cmd|l|ff| qui vaudra " \
            "|cmd|look|ff|. Si l'alias existe déjà, il sera remplacé."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        message = dic_masques["message"].message
        message = message.split(" ")
        if len(message) < 2:
            personnage << "|err|Syntaxe invalide. Référez-vous à l'aide.|ff|"
            return
        
        comm = message[0].lower()
        signification = " ".join(message[1:])
        personnage.alias[comm] = signification
        personnage << "L'alias |cmd|{}|ff| vaut à présent |cmd|{}|ff|.".format(
                comm, signification)
