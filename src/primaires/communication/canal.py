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
        self.liste_noire = ListeID()
    
    def __getinitargs__(self):
        return ("", None)
    
    def __str__(self):
        """Renvoie le canal sous la forme 'canal : résumé - X connecté(s)'"""
        res = "|cmd|" + self.nom + "|ff| : " + self.resume
        nb_connectes = len(self.connectes)
        if nb_connectes == 1:
            connectes = "(1 joueur connecté)"
        else:
            connectes = "(" + str(nb_connectes) + " joueurs connectés)"
        res += connectes
        return res
    
    @property
    def aide(self):
        """Renvoie l'aide du canal"""
        res = str(self)
    
    def rejoindre_ou_quitter(self, joueur, aff=True):
        """Connecte ou déconnecte un joueur et le signale aux connectés"""
        if not joueur in self.connectes:
            self.connectes.append(joueur)
            for connecte in self.connectes:
                if connecte is not joueur:
                    if connecte in self.immerges:
                        connecte << "<" + joueur.nom + " rejoint le canal.>"
                    else:
                        res = self.couleur + "[" + self.nom + "] " + joueur.nom
                        res += " rejoint le canal.|ff|"
                        connecte << res
        else:
            self.connectes.remove(joueur)
            if aff is True:
                for connecte in self.connectes:
                    if connecte in self.immerges:
                        connecte << "<" + joueur.nom + " quitte le canal.>"
                    else:
                        res = self.couleur + "[" + self.nom + "] " + joueur.nom
                        res += " quitte le canal.|ff|"
                        connecte << res
    
    def immerger_ou_sortir(self, joueur, aff=True):
        """Immerge un joueur et le signale aux immergés"""
        if not joueur in self.immerges:
            self.immerges.append(joueur)
            contexte = Immersion(joueur.instance_connexion)
            contexte.canal = type(self).importeur.communication.canaux[self.nom]
            joueur.contexte_actuel.migrer_contexte(contexte)
            if aff is True:
                for immerge in self.immerges:
                    if immerge is not joueur:
                        immerge << "<" + joueur.nom + " s'immerge.>"
        else:
            self.immerges.remove(joueur)
            joueur.contextes.retirer()
            if aff is True:
                for immerge in self.immerges:
                    immerge << "<" + joueur.nom + " sort d'immersion.>"
    
    def dissoudre(self):
        """Détruis le canal et déconnecte tous les joueurs"""
        for joueur in self.connectes:
            if joueur in self.immerges:
                self.immerger_ou_sortir(joueur, False)
            self.rejoindre_ou_quitter(joueur, False)
            joueur << "|err|Le canal {} a été dissous.|ff|".format(self.nom)
        del type(self).importeur.communication.canaux[self.nom]
    
    def ejecter(self, joueur):
        """Ejecte un joueur du canal (méthode de modération)"""
        if joueur in self.immerges:
            self.immerger_ou_sortir(joueur, False)
        self.rejoindre_ou_quitter(joueur, False)
        for connecte in self.connectes:
            if connecte in self.immerges:
                connecte << "<" + joueur.nom + " a été éjecté.>"
            else:
                res = self.couleur + "[" + self.nom + "] " + joueur.nom
                res += " a été éjecté.|ff|"
                connecte << res
        joueur << "|rgc|Vous avez été éjecté du canal {}.|ff|".format(self.nom)
    
    def bannir(self, joueur):
        """Bannit un joueur du canal (méthode de modération)"""
        if joueur in self.immerges:
            self.immerger_ou_sortir(joueur, False)
        self.rejoindre_ou_quitter(joueur, False)
        self.liste_noire.append(joueur)
        for connecte in self.connectes:
            if connecte in self.immerges:
                connecte << "<" + joueur.nom + " a été banni.>"
            else:
                res = self.couleur + "[" + self.nom + "] " + joueur.nom
                res += " a été banni.|ff|"
                connecte << res
        joueur << "|rgc|Vous avez été banni du canal {}.|ff|".format(self.nom)
    
    def promouvoir_ou_dechoir(self, joueur):
        """Promeut ou déchoit un joueur du statut de modérateur"""
        if not joueur in self.moderateurs:
            self.moderateurs.append(joueur)
            if joueur in type(self).importeur.connex.joueurs_connectes:
                if joueur in self.immerges:
                    joueur << "<Vous avez été promu modérateur.>"
                else:
                    joueur << self.couleur + "[" + self.nom + "] Vous avez " \
                            "été promu modérateur.|ff|"
        else:
            self.moderateurs.remove(joueur)
            if joueur in type(self).importeur.connex.joueurs_connectes:
                if joueur in self.immerges:
                    joueur << "<Vous avez été déchu du rang de modérateur.>"
                else:
                    joueur << self.couleur + "[" + self.nom + "] Vous avez " \
                            "été déchu du rang de modérateur.|ff|"
    
    def envoyer(self, joueur, message):
        """Envoie un message au canal"""
        type(self).importeur.communication. \
                dernier_canaux[joueur.nom] = self.nom
        ex_moi = self.couleur + "[" + self.nom + "] Vous dites : "
        ex_moi += message + "|ff|"
        ex_autre = self.couleur + "[" + self.nom + "] " + joueur.nom
        ex_autre += " dit : " + message + "|ff|"
        im_moi = im_autre = "<" + joueur.nom + "> " + message
        if joueur in self.immerges:
            joueur << im_moi
        else:
            joueur << ex_moi
        
        for connecte in self.connectes:
            if connecte is not joueur:
                if connecte in type(self).importeur.connex.joueurs_connectes:
                    if connecte in self.immerges:
                        connecte << im_autre
                    else:
                        connecte << ex_autre
