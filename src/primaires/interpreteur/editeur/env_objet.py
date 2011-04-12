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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit la classe 'envelope_objet' détaillée lus bas."""

from abstraits.obase import BaseObj

class EnvelopeObjet(BaseObj):
    
    """Cette classe définit une envelope contenant :
    -   l'éditeur (une zone de texte uniligne, multi-ligne, une lsite...)
    -   l'édité : l'objet qui doit êre édité
    -   l'attribut : l'attribut qui doit être modifié
    
    On peut trouver en plus quelques informations permettant de construire
    l'éditeur :
    -   l'aide courte : un message d'aide courte, affiché directement
        dans l'accueil
    -   aide longue : un message plus long affiché quand on demande de
        l'aide sur l'éditeur
    
    """
    
    def __init__(self, editeur, edite, attribut):
        """Constructeur de l'envelope"""
        BaseObj.__init__(self)
        self.editeur = editeur
        self.objet = edite
        self.attribut = attribut
        self.parent = None
        self.prompt = ""
        self.apercu = ""
        self.aide_courte = ""
        self.aide_longue = ""
    
    def __getinitargs__(self):
        return (None, None, None)
    
    def construire(self,pere):
        """Retourne l'éditeur construit"""
        editeur = self.editeur(pere, self.objet, self.attribut)
        if self.parent:
            editeur.opts.rci_ctx_prec = self.parent
        editeur.prompt = self.prompt
        editeur.aide_courte = self.aide_courte
        editeur.aide_longue = self.aide_longue
        return editeur
    
    def get_apercu(self):
        """Retourne l'aperçu"""
        return self.apercu.format(objet = self.objet)
    
