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


"""Ce fichier définit la classe Fonction, détaillée plus bas."""

class Fonction:
    """Cette classe définit une fonction possédant une liste
    de paramètres, que l'on peut ainsi appeler à tout moment.

    """
    def __init__(self, fonction, *args, **kwargs):
        """Créée  un objet Fonction gardant la fonction et les paramètres
        à appeler. Pour exécuter cette fonction, on utilise la méthode d'objet
        exec().

        A noter que la méthode exec() peut prendre des paramètres
        supplémentaires. Ils seront ajoutés à la liste des paramètres
        précisés lors de la construction de l'objet.

        """
        self.fonction = fonction
        self.args = args # sous la forme d'un tuple
        self.kwargs = kwargs # sous la forme d'un dictionnaire

    def executer(self, *args_sup, **kwargs_sup):
        """Cette méthode permet d'exécuter la fonction contenue dans
        self.fonction en lui passant en paramètre :
        - les paramètres contenus dans self.args et self.kwargs
        - les paramètres contenus dans args_sup et kwargs_sup

        """
        if self.fonction is not None:
            args = self.args + args_sup
            self.kwargs.update(kwargs_sup)
            kwargs = self.kwargs
            self.fonction(*args, **kwargs)
