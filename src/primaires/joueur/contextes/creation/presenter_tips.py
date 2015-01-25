# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant le contexte "personnage:creation:presenter_tips."""

from primaires.interpreteur.contexte import Contexte

class PresenterTips(Contexte):

    """Contexte présentant simplement les tips."""

    nom = "personnage:creation:presenter_tips"

    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)

    def accueil(self):
        """Message d'accueil du contexte"""
        return \
            "\n|tit|-------= Suivez les tips =-------|ff|\n" \
            "Votre nouveau personnage a bien été créé !\nVous allez " \
            "à présent arriver dans un lieu propre aux nouveaux\njoueurs. " \
            "Vous y découvrirez les commandes les plus courantes et\n" \
            "la façon d'obtenir de l'aide en jeu. Toutes ces informations " \
            "vous\nseront données sous la forme de \"tips\", des " \
            "messages |att|colorés|ff|\nqui apparaîtront après l'entrée " \
            "de commandes, dès votre arrivée dans\nla zone pour " \
            "débutants. Surveillez l'apparition de ces messages,\n" \
            "car ils vous donneront des explications concrètes sur " \
            "les commandes\nà utiliser."

    def get_prompt(self):
        """Message de prompt"""
        return "Appuyez sur la touche ENTRÉE pour entrer en jeu."

    def interpreter(self, msg):
        """Méthode d'interprétation"""
        importeur.joueur.migrer_ctx_creation(self)
