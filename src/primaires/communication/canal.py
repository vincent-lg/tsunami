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


"""Ce fichier contient la classe Canaldétaillée plus bas."""

from abstraits.obase import BaseObj
from bases.collections.liste_id import ListeID
from primaires.format.description import Description
from primaires.communication.contextes import Immersion

class Canal(BaseObj):
    
    """Classe définissant un canal.
    
    """
    
    def __init__(self, nom, auteur):
        """Constructeur du canal"""
        self.nom = nom
        self.auteur = auteur
        self.couleur = "|cyc|"
        self.resume = "canal de communication"
        self.description = Description()
        self.moderateurs = ListeID()
        self.immerges = ListeID()
        self.connectes = ListeID()
    
    def __getinitargs__(self):
        return ("", None)
    
    def __str__(self):
        """Renvoie le canal sous la forme 'canal : résumé - X connectés'"""
        res = self.nom + " : " + self.resume
        nb_connectes = len(self.connectes)
        if nb_connectes == 1:
            connectes = "1 joueur connecté"
        else:
            connectes = str(nb_connectes) + " joueurs connectés"
        res += " - " + connectes
        return res
    
    def connecter(self, personnage):
        """Connecte ou déconnecte personnage et le signale aux immergés"""
        if not personnage in self.connectes:
            self.connectes.append(personnage)
            for immerge in self.immerges:
                immerge << "<" + personnage.nom + " rejoint le canal.>"
        else:
            self.connectes.remove(personnage)
            for immerge in self.immerges:
                immerge << "<" + personnage.nom + " quitte le canal.>"
    
    def immerger(self, personnage):
        """Immerge un personnage et le signale aux immergés"""
        if not personnage in self.immerges:
            self.immerges.append(personnage)
            contexte = Immersion(personnage.instance_connexion)
            contexte.canal = self
            personnage.contexte_actuel.migrer_contexte(contexte)
            for immerge in self.immerges:
                if immerge is not personnage:
                    immerge << "<" + personnage.nom + " s'immerge.>"
        else:
            self.immerges.remove(personnage)
            personnage.contextes.retirer()
            for immerge in self.immerges:
                if immerge is not personnage:
                    immerge << "<" + personnage.nom + " sort d'immersion.>"
    
    def envoyer(self, personnage, message):
        """Envoie le message au canal"""
        type(self).importeur.communication. \
                dernier_canaux[personnage.nom] = self.nom
        ex_moi = self.couleur + "[" + self.nom + "] Vous dites : "
        ex_moi += message + "|ff|"
        ex_autre = self.couleur + "[" + self.nom + "] " + personnage.nom
        ex_autre += " dit : " + message + "|ff|"
        im_moi = im_autre = "<" + personnage.nom + "> " + message
        if personnage in self.immerges:
            personnage << im_moi
        else:
            personnage << ex_moi
        
        for connecte in self.connectes:
            if connecte is not personnage:
                if connecte in type(self).importeur.connex.joueurs_connectes:
                    if connecte in self.immerges:
                        connecte << im_autre
                    else:
                        connecte << ex_autre
