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


"""Fichier contenant la classe Confirmation, détaillée plus bas.

"""

from . import Contexte

class Confirmation(Contexte):
    
    """Contexte générique de confirmation.
    Ce contexte permet de créer facilement un système de confirmation
    pour n'importe quelle commande ou éditeur. Il suffit de lui passer
    un objet et une fonction de callback suivie de la liste de ses arguments.
    Elle sera appelée si le joueur confirme.
    
    """
    
    def __init__(self, pere, objet, callback, arguments=[]):
        Contexte.__init__(self, pere)
        self.opts.prompt_prf = ""
        self.opts.prompt_clr = ""
        self.objet = objet
        self.callback = callback
        self.arguments = arguments
    
    def __getnewargs__(self):
        return (None, None, None)
    
    def __getstate__(self):
        """On nettoie les options"""
        dico_attr = Contexte.__getstate__(self)
        dico_attr["callback"] = dico_attr["callback"].__name__
        return dico_attr
    
    def __setstate__(self, dico_attr):
        """Récupération de l'éditeur"""
        Contexte.__setstate__(self, dico_attr)
        fonction = getattr(self.objet, self.callback)
        self.callback = fonction
    
    def get_prompt(self):
        """Prompt du contexte"""
        return "-> "
    
    def accueil(self):
        """Accueil du contexte"""
        return \
            "|att|Etes-vous sûr ? Entrez |ff||ent|oui|ff||att| pour " \
            "confirmer.|ff|"
    
    def interpreter(self, msg):
        """Interprétation du contexte"""
        fonction = self.callback
        args = self.arguments
        if msg.lower() == "oui":
            fonction(*args)
            self.fermer()
            self.pere.joueur << "Vous avez bien confirmé."
        else:
            self.fermer()
            self.pere.joueur << "Vous avez bien annulé."
