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


"""Fichier contenant l'action dire."""

from primaires.scripting.action import Action
from primaires.scripting.utile.fonctions import *

class ClasseAction(Action):
    
    """Dit quelque chose.
    
    C'est l'action standard pour envoyer un message dans l'univers."""
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.dire_personnage, "Personnage", "str")
        cls.ajouter_types(cls.dire_salle, "Salle", "str")
    
    @staticmethod
    def dire_personnage(personnage, message):
        """Envoie un message au personnage."""
        personnage.envoyer(message, **variables)
    
    @staticmethod
    def dire_salle(salle, message):
        """Envoie un message aux personnages présents dans la salle.
        A noter que tous les personnages contenus dans des variables de
        ce script, s'il y en a, sont exclus de la liste et ne reçoivent
        donc pas ce message.
        
        """
        f_variables = get_variables(variables, message)
        salle.envoyer(message, **f_variables)
