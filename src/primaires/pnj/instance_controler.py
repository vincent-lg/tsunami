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


"""Fichier contenant la classe InstanceControlelr, détaillée plus bas."""

from primaires.connex.instance_connexion import InstanceConnexion

class InstanceControler(InstanceConnexion):
    
    """Instance de connexion virtuelle pour les PNJ contrôlés."""
    
    def __init__(self, joueur, pnj):
        InstanceConnexion.__init__(self, None)
        self.t_joueur = joueur
        self.pnj = pnj
        self.joueur = pnj
    
    def __getnewargs__(self):
        return (None, None)
    
    @property
    def encodage(self):
        encodage = "Utf-8"
        if not hasattr(self, "t_joueur") or self.t_joueur is None:
            return encodage
        if self.t_joueur.compte:
            return self.t_joueur.compte.encodage
        return encodage
    
    def envoyer(self, msg, nl=2):
        """Redéfinition de la méthode envoyer."""
        self.nb_msg += 1
        msg = self.formater_message(msg)
        if hasattr(self, "t_joueur") and self.t_joueur and \
                self.t_joueur.instance_connexion:
            self.t_joueur.instance_connexion.file_attente.append((nl, msg))
