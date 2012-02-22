# -*-coding:Utf-8 -*
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


"""Fichier contenant la classe Dictionnaire détaillée plus bas."""

import copy

from collections import OrderedDict

class Dictionnaire:

    """Classe représentant un dictionnaire, très semblable aux builtins.

    La grande différence est que ce dictionnaire est susceptible de contenir,
    en clé ou valeur, des objets prévus pour être enregistrés.
    Ces objets contiennent simplement un attribut e_existe qui doit
    être à True. Si il est à False, l'objet est ignoré (c'est-à-dire
    supprimé du dictionnaire).

    A chaque action sur le dictionnaire, on le nettoie.

    """

    def __init__(self, *args, **kw_args):
        """Constructeur du dictionnaire."""
        self.a_nettoyer = True
        self.dictionnaire = dict(*args, **kw_args)
        self.e_existe = True

    def __getattr__(self, attr):
        """L'attribut en question est probablement une méthode.

        Dans tous les cas, on nettoie la dictionnaire avant de retourner
        l'objet concerné que l'on cherche dans dictionnaire.

        """
        net = False
        if object.__getattribute__(self, "dictionnaire"):
            try:
                coll = object.__getattribute__(self, "dictionnaire")
                a_nettoyer = object.__getattribute__(self, "a_nettoyer")
                if a_nettoyer:
                    net = True
            except AttributeError:
                pass
        if net:
            self.nettoyer()
        return getattr(self.dictionnaire, attr)

    def __getitem__(self, item):
        self.nettoyer()
        return self.dictionnaire[item]

    def __setitem__(self, item, valeur):
        self.dictionnaire[item] = valeur

    def __delitem__(self, item):
        del self.dictionnaire[item]

    def __repr__(self):
        self.nettoyer()
        return repr(self.dictionnaire)

    def __str__(self):
        self.nettoyer()
        return str(self.dictionnaire)

    def __iter__(self):
        self.nettoyer()
        return iter(self.dictionnaire)

    def __len__(self):
        self.nettoyer()
        return len(self.dictionnaire)

    def nettoyer(self):
        """Nettoie le dictionnaire."""
        dictionnaire = {}
        for cle, valeur in self.dictionnaire.items():
            # Traitement de la clé
            if hasattr(cle, "e_existe") and not cle.e_existe:
                continue
            # Traitement de la valeur
            if hasattr(valeur, "e_existe") and not valeur.e_existe:
                continue
            dictionnaire[cle] = valeur
        
        self.dictionnaire.clear()
        self.dictionnaire.update(dictionnaire)

class DictionnaireOrdonne:

    """Classe représentant un dictionnaire ordonné.

    La grande différence est que ce dictionnaire est susceptible de contenir,
    en clé ou valeur, des objets prévus pour être enregistrés.
    Ces objets contiennent simplement un attribut e_existe qui doit
    être à True. Si il est à False, l'objet est ignoré (c'est-à-dire
    supprimé du dictionnaire).

    A chaque action sur le dictionnaire, on le nettoie.

    """

    def __init__(self, *args, **kw_args):
        """Constructeur du dictionnaire."""
        self.dictionnaire = OrderedDict(*args, **kw_args)
        self.e_existe = True

    def __getattr__(self, attr):
        """L'attribut en question est probablement une méthode.

        Dans tous les cas, on nettoie la dictionnaire avant de retourner
        l'objet concerné que l'on cherche dans dictionnaire.

        """
        if object.__getattribute__(self, "dictionnaire"):
            self.nettoyer()
        return getattr(self.dictionnaire, attr)

    def __getitem__(self, item):
        self.nettoyer()
        return self.dictionnaire[item]

    def __setitem__(self, item, valeur):
        self.dictionnaire[item] = valeur

    def __delitem__(self, item):
        del self.dictionnaire[item]

    def __repr__(self):
        self.nettoyer()
        return repr(self.dictionnaire)

    def __str__(self):
        self.nettoyer()
        return str(self.dictionnaire)

    def __iter__(self):
        self.nettoyer()
        return iter(self.dictionnaire)

    def __len__(self):
        self.nettoyer()
        return len(self.dictionnaire)

    def __deepcopy__(self, memo):
        """Méthode surchargée pour permettre la copie de ce dictionnaire."""
        dictionnaire = copy.deepcopy(object.__getattribute__(self,
                "dictionnaire"), memo)
        return dictionnaire
    
    def nettoyer(self):
        """Nettoie le dictionnaire."""
        dictionnaire = OrderedDict()
        for cle, valeur in self.dictionnaire.items():
            # Traitement de la clé
            if hasattr(cle, "e_existe") and not cle.e_existe:
                continue
            # Traitement de la valeur
            if hasattr(valeur, "e_existe") and not valeur.e_existe:
                continue
            dictionnaire[cle] = valeur
        
        self.dictionnaire.clear()
        self.dictionnaire.update(dictionnaire)
