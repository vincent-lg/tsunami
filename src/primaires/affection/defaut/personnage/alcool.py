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


"""Ce module contient la classe Alcool, détaillée plus bas."""

from random import choice, randint, random

from primaires.affection.personnage import AffectionPersonnage

class Alcool(AffectionPersonnage):
    
    """Affection définissant l'alcool dans un personnage."""
    
    def __init__(self):
        AffectionPersonnage.__init__(self, "alcool")
        self.visible = True
    
    def __getnewargs__(self):
        return ()
    
    def dec_duree(self, affection, duree=1):
        """Manipule l'affection concrète quand la durée se décrémente.
        
        Cette fonction est appelée pour modifier une affection concrète
        (avec durée, force et s'appliquant à un affecté) quand la
        durée est censée se décrémenter. Ici, l'alcool reste la même.
        
        """
        affection.duree -= duree
    
    def message(self, affection):
        """Retourne le message du personnage affecté par l'alcool."""
        messages = (
            (1, "Une fine rougeur colorie les joues de {perso}"),
            (5, "Une légère rougeur colorie le front et le cou de {perso}"),
            (10, "Une rougeur assez vive colorie le visage de {perso}"),
            (20, "{perso} a le nez bien rouge et titube légèrement"),
            (40, "{perso} a le visage rouge brique et titube à chaque " \
                    "mouvement"),
        )
        
        for t_force, message in messages:
            if affection.force <= t_force:
                return message
        
        return messages[-1][0]
    
    def moduler(self, affection, duree, force):
        """Module, c'est-à-dire ici ajoute simplement les forces et durées."""
        affection.duree += duree
        affection.force += force
        if affection.force > 50:
            affection.force = 50
    
    def message_detruire(self, affection):
        """Destruction de l'affection du personnage."""
        affection.affecte.envoyer("Vous retrouvez votre clarté d'esprit, " \
                "très lentement.", prompt=False)
    
    def deformer_message(self, affection, message):
        """Déforme le message en fonction de l'alcool."""
        expressions = {
            "v": "b",
            "vr": "nr",
            "f": "v",
            "v": "f",
            "t": "d",
            "d": "t",
            "b": "p",
            "p": "b",
            "ca": "ga",
            "co": "go",
            "cu": "gu",
            "cou": "gou",
            "s": "z",
            "ce": "ze",
            "cé": "zé",
            "ci": "zi",
            "ç": "z",
        }
        
        for expression, remplacement in expressions.items():
            t_min = 0
            pos = []
            while t_min >= 0:
                t_min = message.find(expression, t_min)
                if t_min >= 0:
                    pos.append(t_min)
                    t_min += 1
                else:
                    break
            
            t_pos = []
            for position in pos:
                if affection.force / 50 >= random():
                    t_pos.append(position)
            
            for pos in t_pos:
                message = message[:pos] + remplacement + message[pos + \
                        len(expression):]
        
        mots = message.split(" ")
        t_mots = list(mots)
        exclammations = ("ufff...", "hic !", "blurg !", "hum...")
        if affection.force >= 25:
            exclammations += ("houla...", "argh !", "ah !", "ah...", "argh !")
        if affection.force >= 40:
            exclammations += ("youpi !", )
        for i, mot in enumerate(t_mots):
            if affection.force / 150 >= random():
                retour = randint(0, 3)
                if i < 3:
                    continue
                
                a_mots = t_mots[i - retour:i + 1]
                a_mots = " " + " ".join(a_mots)
                
                mots[i] = mot + "... " + choice(exclammations) + a_mots
        
        return " ".join(mots)
