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


"""Ce fichier contient la classe ObjetNonUnique, détaillée plus bas."""

from abstraits.obase import BaseObj
from .objet import Objet

class ObjetNonUnique(BaseObj):
    
    """Enveloppe d'un objet non unique.
    
    Un objet non unique est une enveloppe d'un prototype et d'un nombre.
    Par exemple, l'objet non unique piece_or est construit d'après son
    prototype et un nombre variable, en fonction du nombre d'objets dans
    le conteneur. Si il y a 5 pièces d'or sur le sol, alors dans le
    conteneur de la salle on trouvera un objet non unique pointant
    sur le prototype piece_or et avec 5 en nombre.
    
    """
    
    def __init__(self, prototype, nombre=1):
        """Constructeur de l'objet."""
        BaseObj.__init__(self)
        self.prototype = prototype
        self.nombre = nombre
        self.identifiant = ""
    
    def __getnewargs__(self):
        return (None, )
    
    __getattr__ = Objet.__getattr__
