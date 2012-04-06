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


"""Ce fichier définit le contexte-éditeur 'entier'."""

from . import Editeur

class Entier(Editeur):
    
    """Contexte-éditeur entier.
    
    Ce contexte sert à modifier des attributs de type 'int'.
    
    """
    
    nom = "editeur:base:entier"
    
    def __init__(self, pere, objet=None, attribut=None, inf=0, sup=None,
            signe=""):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.limite_inf = inf
        self.limite_sup = sup
        self.signe = signe
    
    def accueil(self):
        """Retourne l'aide courte"""
        valeur = str(getattr(self.objet, self.attribut)) + self.signe
        return self.aide_courte.format(objet=self.objet, valeur=valeur)
    
    def interpreter(self, msg):
        """Interprétation du contexte"""
        try:
            msg = int(msg)
            if self.limite_inf is not None:
                assert msg >= self.limite_inf
            if self.limite_sup is not None:
                assert msg <= self.limite_sup
        except ValueError:
            self.pere << "|err|Précisez un nombre valide.|ff|"
        except AssertionError:
            sup = "supérieur à {}".format(self.limite_inf) if self.limite_inf \
                    is not None else ""
            inf = "inférieur à {}".format(self.limite_sup) if self.limite_sup \
                    is not None else ""
            et = " et " if sup and inf else ""
            err = "|err|Le nombre entré doit être {sup}{et}{inf}.|ff|".format(
                    su=sup, et=et, nf=inf)
            self.pere << err
        else:
            setattr(self.objet, self.attribut, msg)
            self.actualiser()
