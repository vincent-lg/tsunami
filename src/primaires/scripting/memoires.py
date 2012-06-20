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


"""Fichier contenant la classe Instruction, détaillée plus bas ; et
l'exception ErreurExecution.

"""

from collections import OrderedDict

from abstraits.obase import BaseObj, MetaBaseObj
from .exceptions import ErreurScripting

class Memoires(BaseObj):
    
    """Classe enveloppe définissant les mémoires du scripting.
    
    Les mémoires peuvent être liées à un PNJ, une salle, un objet, l'univers...
    Elles sont manipulées en scripting par l'action ecrire_memoire, et les
    fonctions memoire_existe et memoire.
    
    """
    
    enregistrer = True
    
    def __init__(self, parent=None):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self._memoires = {}
    
    def __getnewargs__(self):
        return ()
    
    def __getitem__(self, cle):
        return self._memoires[cle]
    
    def __setitem__(self, cle, valeur):
        self._memoires[cle] = valeur
    
    def __contains__(self, valeur):
        return valeur in self._memoires
