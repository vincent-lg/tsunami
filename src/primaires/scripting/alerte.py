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


"""Fichier contenant la classe alerte détailée plus bas."""

from datetime import datetime

from abstraits.obase import BaseObj

class Alerte(BaseObj):
    
    """Classe définissant une alerte scripting.
    
    Une alerte est levée en cas d'erreur lors de l'exécution d'un script.
    Les alertes sont visibles par un groupe d'immortels. L'alerte
    contient les informations utiles à la correction du bug.
    
    """
    
    def __init__(self, objet, evenement, test, no_ligne, ligne, message,
            traceback):
        """Cration d'une alerte.
        
        Les paramètres attendus sont :
            objet -- l'objet scripté
            evenement - le nom de l'évènement exécuté
            test -- le nom du test
            no_ligne -- le numéro à laquel s'est produit l'erreur
            ligne -- la ligne de script elle-même
            message -- le message d'erreur
            traceback -- le traceback complet de l'exception levée.
        
        """
        BaseObj.__init__(self)
        self.no = len(type(self).importeur.scripting.alertes) + 1
        self.objet = repr(objet)
        self.date = datetime.now()
        if objet:
            self.type = type(objet).nom_scripting
        else:
            self.type = "inconnu"
        self.evenement = evenement
        self.test = test
        self.no_ligne = no_ligne
        self.ligne = ligne
        self.message = message
        self.traceback = traceback
    
    def __getnewargs__(self):
        return (None, "", "", "", "", "", "")
