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


"""Fichier contenant la classe Evenement détaillée plus bas."""

from abstraits.obase import *

class Evenement(BaseObj):
    
    """Classe contenant un évènement de scripting.
    
    Un évènement est appelé dans une certaine situation. Un cas classique,
    par exemple, est un script définit dans un PNJ. Un évènement pourrait
    être appelé quand le PNJ est attaqué.
    
    Les évènements peuvent contenir des sous-évènements.
    
    Au niveau de la structure, un évènement contient :
    *   un dictionnaire de variables qui doivent IMPERATIVEMENT être
        TOUTES RENSEIGNEES quand on l'appelle
    *   une suite d'instructions de différents types
    *   un dictionnaire pouvant contenir des sous-évènements
    *   l'appelant de l'évènement (le parent du script)
    
    En outre, l'évènement garde en mémoire le script dont il est issu,
    qu'il soit sous-évènement ou non.
    
    Le constructeur d'èn évènement prend en paramètre :
        script -- le script qui possède l'évènement
        nom -- le nom de l'évènement
        parent -- si c'est un sous-évènement, l'évènement parent (optionnel)
    
    """
    
    def __init__(self, sscript, nom, parent=None):
        """Constructeur d'èn évènement"""
        BaseObj.__init__(self)
        self.script = script
        self.appelant = None
        if self.script:
            self.appelant = self.script.parent
        self.nom = nom
        self.parent = parent
        self.variables = {}
        self.__instructions = []
        self.__evenements = {}
        self.construire()
    
    def __getnewargs__(self):
        return (None, "")
