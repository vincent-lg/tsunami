# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant le contexte éditeur EdtCle"""

from primaires.interpreteur.editeur import Editeur

class EdtCle(Editeur):
    
    """Classe définissant le contexte éditeur 'cle'.
    
    Ce contexte permet de rechercher un prototype d'objet depuis sa clé.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None, types=None):
        """Constructeur de l'éditeur.
        
        Le paramètre types doit être une chaîne ou une liste de types
        qui peuvent être sélectionnés. Si ce paramètre est None, tous les
        types sont considérés comme pouvant être sélectionnés.
        
        """
        Editeur.__init__(self, pere, objet, attribut)
        if types is None:
            self.types = ()
        elif isinstance(types, str):
            self.types = (types, )
        else:
            self.types = tuple(types)
        self.ajouter_option("d", self.opt_supprimer)
    
    def opt_supprimer(self, arguments):
        """Supprime la clé (réinitialise l'attribut à None)."""
        setattr(self.objet, self.attribut, None)
        self.actualiser()
    
    def accueil(self):
        """Message d'accueil"""
        objet = getattr(self.objet, self.attribut)
        if objet:
            nom = objet.nom_singulier
            cle = objet.cle
        else:
            nom = "inconnu"
            cle = "|att|non précisée|ff|"
        
        ret = self.aide_courte + "\n\n"
        ret += "options :\n"
        ret += " - |cmd|/d|ff| : réinitialise l'objet entré\n\n"
        ret += "Objet actuel : " + nom + " (" + cle + ")"
        return ret
    
    def interpreter(self, msg):
        """Interprétation du message."""
        cle = msg.strip().lower()
        try:
            objet = importeur.objet.prototypes[cle]
        except KeyError:
            self.pere.envoyer("|err|Clé d'objet inconnue '{}'.|ff|".format(
                    cle))
        else:
            if self.types:
                val = False
                for nom_type in self.types:
                    if objet.est_de_type(nom_type):
                        val = True
                        break
                
                if not val:
                    self.pere.envoyer("|err|L'objet '{}' n'est pas du " \
                            "bon type. Types attendus : ".format(cle) + \
                            ", ".join(self.types) + "|ff|")
                    return
            
            setattr(self.objet, self.attribut, objet)
            self.actualiser()
