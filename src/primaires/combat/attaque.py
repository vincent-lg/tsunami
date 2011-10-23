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


"""Fichier contenant la classe Attaque, détaillée plus bas.

Il contient également les autres classes héritées d'Attaque :
    Attaque
    Coup

"""

from abstraits.obase import BaseObj

class Attaque(BaseObj):
    
    """Classe représentant une attaque."""
    
    def __init__(self, personnage, cle):
        """Constructeur de l'attaque."""
        BaseObj.__init__(self)
        self.personnage = personnage
        self.cle = cle
        self.msg_tentative = {
            "moi": "",
            "contre": "",
            "autres": "",
        }
        self.msg_reussite = {
            "moi": "",
            "contre": "",
            "autres": "",
        }
        self._construire()
    
    def envoyer_msg_tentative(self, moi, contre, membre):
        """Envoie les messages en cas de tentative."""
        moi.envoyer_lisser(self.msg_tentative["moi"], moi=moi, contre=contre,
                membre=membre)
        contre.envoyer_lisser(self.msg_tentative["contre"],  moi=moi,
                contre=contre, membre=membre)
        moi.salle.envoyer_lisser(self.msg_tentative["autres"],  moi=moi,
                contre=contre, membre=membre)
    
    def envoyer_msg_reussite(self, moi, contre, membre, degats):
        """Envoie les messages en cas de réussite."""
        moi.envoyer_lisser(self.msg_reussite["moi"], moi=moi, contre=contre,
                membre=membre, degats=degats)
        contre.envoyer_lisser(self.msg_reussite["contre"],  moi=moi,
                contre=contre, membre=membre, degats=degats)
        moi.salle.envoyer_lisser(self.msg_reussite["autres"],  moi=moi,
                contre=contre, membre=membre, degats)

class Coup(Attaque):
    
    """Classe représentant un coup."""
    
    def __init__(self, personnage, cle):
        """Constructeur du coup."""
        Attaque.__init__(self, personnage, cle)
        self.msg_tentative["moi"] = \
                "Vous tentez d'atteindre {contre} à {membre}."
        self.msg_tentative["contre"] = \
                "{moi} tente de vous atteindre à {membre}."
        self.msg_tentative["autres"] = \
                "{moi} tente d'atteindre {contre} à {membre}."
