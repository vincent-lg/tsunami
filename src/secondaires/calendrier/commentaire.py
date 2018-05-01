# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 AYDIN Ali-Kémal
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

"""Fichier décrivant la classe Commentaire, détaillée plus bas."""

import datetime

from abstraits.obase import BaseObj
from primaires.format.date import get_date

class Commentaire(BaseObj):

    """Classe décrivant un commentaire
    
    Un commentaire est défini par son contenu, son auteur,
    sa date de publication et l'évènement associé.
    
    Une fois posté, un commentaire ne doit plus être modifié.
    
    """
    
    def __init__(self, evt, auteur, msg):
        """Constructeur d'un commentaire"""
        BaseObj.__init__(self)
        self.evenement = evt
        self.auteur = auteur
        self.contenu = msg
        self.date = datetime.date.today()   
    
    def __getnewargs__(self):
        return (None, None, "")
    
    def __str__(self):
        return "{}\n  par {} le {}".format(
                self.contenu, self.auteur.nom, self.str_date)
    
    @property
    def str_date(self):
        """Retourne la date en format français."""
        return get_date(self.date.timetuple())
