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


"""Fichier contenant la classe Etape détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.format.description import Description

class Etape(BaseObj):
    
    """Classe définissant une étape simple dans la quête.
    
    Une étape simple est liée à une suite d'instructions. Une suite d'étapes
    simple peut constituer une quête mais il est tout à fait possible d'y
    intégrer des étapes plus complexes, comme des embranchements ou des
    sous-quêtes. Ces deux autres étapes plus complexes ne sont pas traitées ici.
    
    """
    
    def __init__(self, quete):
        """Constructeur de l'étape."""
        BaseObj.__init__(self)
        self.quete = quete
        self.titre = "non renseigné"
        self.description = Description(self)
        self.objet = None
        self.evenement = ""
        self.no_test = -1
    
    def __getnewargs__(self):
        return (None, )
    
    @property
    def reliee(self):
        """Retourne True si l'étape est reliée."""
        return self.objet is not None and self.evenement and self.no_test >= 0
    
    @property
    def test(self):
        """Retourne le test connecté."""
        return getattr(self.objet, "script").evenements[self.evenement].tests[
                self.no_test]
