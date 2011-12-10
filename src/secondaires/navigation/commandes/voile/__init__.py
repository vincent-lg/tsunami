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


"""Package contenant la commande 'voile'."""

from primaires.interpreteur.commande.commande import Commande
from .border import PrmBorder
from .choquer import PrmChoquer
from .empanner import PrmEmpanner
from .hisser import PrmHisser
from .plier import PrmPlier

class CmdVoile(Commande):
    
    """Commande 'voile'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "voile", "sail")

        self.aide_courte = "manipulation de la voile"
        self.aide_longue = \
            "Cette commande permet de manipuler une voile se trouvant " \
            "dans la même pièce que vous. Vous pouvez lahisser, la " \
            "plier et l'orienter."
    
    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmBorder())
        self.ajouter_parametre(PrmChoquer())
        self.ajouter_parametre(PrmEmpanner())
        self.ajouter_parametre(PrmHisser())
        self.ajouter_parametre(PrmPlier())
