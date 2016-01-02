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


"""Fichier contenant la classe Message, détaillée plus bas."""

from primaires.format.fonctions import *

class Message:
    """Classe définissant un message.
    Ce message est créé depuis une chaîne de caractères.
    Certains codes présents dans cette chaîne permettent d'ajouter quelques
    informations de formattage (des sauts de ligne, de la couleur...).
    
    Il suffit ensuite de demander à convertir ce message en une nouvelle
    chaîne (on peut utiliser pour ce faire la fonction 'str()').
    
    """
    def __init__(self, msg_chn, config):
        """On passe en paramètre du constructeur le message comme une
        chaîne de caractère, et l'objet de configuration (voir config.py).
        
        """        
        # Opérations sur la chaîne
        msg_chn = convertir_nl(msg_chn)
        msg_chn = ajouter_couleurs(msg_chn, config)
        msg_chn = remplacer_sp_cars(msg_chn)
        
        # On l'enregistre en tant qu'attribut
        self.chaine = msg_chn
    
    def __str__(self):
        """Retourne msg_chn"""
        return self.msg_chn
