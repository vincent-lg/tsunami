# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant la méta-classe et la classe abstraite de contrôle."""

from abstraits.obase import BaseObj, MetaBaseObj

controles = {}

class MetaControle(MetaBaseObj):

    """Métaclasse des contrôles.

    Elle ajoute le contrôle dans le dictionnaire 'controles' si il possède
    une clé.

    """

    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        MetaBaseObj.__init__(cls, nom, bases, contenu)
        if cls.cle:
            controles[cls.cle] = cls

class Controle(BaseObj, metaclass=MetaControle):

    """Classe représentant un contrôle.

    Un contrôle est une classe intermédiaire entre un objectif et une
    volonté. Un contrôle permet de spécifier une action continue
    paramétrable. Par exemple, un contrôle permet de paramétrer la
    vitesse du navire. Si un équipage possède ce contrôle actif,
    le commandant (le capitaine ou second PNJ) va décomposer ce contrôle
    en ordres après avoir déterminé combien de voiles, en fonction du
    vent, doivent être hissées, ainsi que combien de rames doivent être
    tenues et à quelle vitesse. Cependant, un contrôle n'est pas
    simpelment une volonté enveloppant d'autres volontés : le contrôle
    reste actif jusqu'au moment où il sera remplacé. Admettons que le
    vent change de direction et que la vitesse se modifie, le contrôle
    doit faire en sorte que la vitesse soit rétablie à celle spécifiée.

    Contrairement aux objectifs, volontés et ordres, un contrôle est
    actif ou inactif sur un navire en fonction de son type. On ne peut
    avoir deux contrôles actifs en même temps sur le même navire
    précisant que le navire doit aller à 1 noeud et à 2 noeuds. Par
    contre, on peut avoir deux contrôles actifs sur le même navire, l'un
    de type 'vitesse' précisant que le navire doit aller à 1,7 noeuds
    et l'autre de type 'direction' précisant que le navire doit maintenir
    ce cap.

    """

    cle = None
    logger = type(importeur).man_logs.get_logger("ordres")
    def __init__(self, equipage, *args):
        BaseObj.__init__(self)
        self.equipage = equipage
        self.arguments = args

    def __getnewargs__(self):
        arguments = (None, ) + getattr(self, "arguments", ())
        return arguments

    def __repr__(self):
        return "<Contrôle {}:{} {}>".format(self.cle_navire, self.cle,
                self.arguments)

    @property
    def navire(self):
        return self.equipage and self.equipage.navire or None

    @property
    def cle_navire(self):
        navire = self.navire
        return navire and navire.cle or "inconnu"

    @property
    def commandant(self):
        """Retourne le commdnant (PNJ) du navire."""
        commandants = self.equipage.get_matelots_au_poste("commandant",
                libre=False)
        if commandants:
            return commandants[0]

        return None

    def decomposer(self):
        """Décompose le contrôle en volontés.

        C'est la méthode la plus importante et celle qui risque de contenir
        le plus de code. Elle décompose réellement le contrôle en volontés
        (plier 2 voiles, ramer lentement, par exemple).

        """
        raise NotImplementedError
