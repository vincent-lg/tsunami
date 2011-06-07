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
        BaseObj.__init__(self)
        self.nom = nom
        self.auteur = auteur
        self.clr = "|cyc|"
        self.resume = "canal de communication"
        self.description = Description()
        self.moderateurs = ListeID()
        self.immerges = ListeID()
        self.connectes = ListeID()
        self.liste_noire = ListeID()
    
    def __getnewargs__(self):
        return ("", None)
    
    def __str__(self):
        """Renvoie le canal sous la forme 'canal : résumé - X connecté(s)'"""
        res = self.nom + "|ff| : " + self.resume
        nb_connectes = 0
        for connecte in self.connectes:
            if connecte in type(self).importeur.connex.joueurs_connectes:
                nb_connectes += 1
        res += " (|rgc|" + str(nb_connectes) + "|ff|)"
        return res
    
    @property
    def infos(self):
        """Renvoie l'aide du canal"""
        return str(self)
    
    def rejoindre_ou_quitter(self, joueur, aff=True):
        """Connecte ou déconnecte un joueur et le signale aux connectés"""
        if not joueur in self.connectes:
            if joueur in self.liste_noire:
                joueur << "|err|Vous êtes sur la liste noire de ce canal.|ff|"
            else:
                self.connectes.append(joueur)
                for connecte in self.connectes:
                    if connecte in type(self).importeur.connex.joueurs_connectes:
                        if connecte is not joueur:
                            if connecte in self.immerges:
                                res = self.clr + "<" + joueur.nom
                                res += " rejoint le canal.>|ff|"
                                connecte << res
                            else:
                                res = self.clr + "[" + self.nom + "] "
                                res += joueur.nom + " rejoint le canal.|ff|"
                                connecte << res
        else:
            self.connectes.remove(joueur)
            if aff is True:
                for connecte in self.connectes:
                    if connecte in type(self).importeur.connex.joueurs_connectes:
                        if connecte in self.immerges:
                            res = self.clr + "<" + joueur.nom
                            res += " quitte le canal.>|ff|"
                            connecte << res
                        else:
                            res = self.clr + "[" + self.nom + "] " + joueur.nom
                            res += " quitte le canal.|ff|"
                            connecte << res
    
    def immerger_ou_sortir(self, joueur, aff=True):
        """Immerge un joueur et le signale aux immergés"""
        if not joueur in self.immerges:
            self.immerges.append(joueur)
            contexte = Immersion(joueur.instance_connexion)
            contexte.canal = type(self).importeur.communication.canaux[self.nom]
            joueur.contexte_actuel.migrer_contexte(contexte)
            for immerge in self.immerges:
                if immerge in type(self).importeur.connex.joueurs_connectes:
                    if immerge is not joueur:
                        res = self.clr + "<" + joueur.nom + " s'immerge.>|ff|"
                        immerge << res
        else:
            self.immerges.remove(joueur)
            joueur.contextes.retirer()
            if aff is True:
                for immerge in self.immerges:
                    if immerge in type(self).importeur.connex.joueurs_connectes:
                        res = self.clr + "<" + joueur.nom
                        res += " sort d'immersion.>|ff|"
                        immerge << res
    
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
            if connecte in type(self).importeur.connex.joueurs_connectes:
                if connecte in self.immerges:
                    connecte << self.clr + "<" + joueur.nom + " a été éjecté.>|ff|"
                else:
                    res = self.clr + "[" + self.nom + "] " + joueur.nom
                    res += " a été éjecté.|ff|"
                    connecte << res
        joueur << "|rgc|Vous avez été éjecté du canal {}.|ff|".format(self.nom)
    
    def bannir(self, joueur):
        """Bannit un joueur du canal (méthode de modération)"""
        if joueur in self.liste_noire:
            if joueur in self.immerges:
                self.immerger_ou_sortir(joueur, False)
            self.rejoindre_ou_quitter(joueur, False)
            self.liste_noire.append(joueur)
            for connecte in self.connectes:
                if connecte in type(self).importeur.connex.joueurs_connectes:
                    if connecte in self.immerges:
                        res = self.clr + "<" + joueur.nom + " a été banni.>|ff|"
                        connecte << res
                    else:
                        res = self.clr + "[" + self.nom + "] " + joueur.nom
                        res += " a été banni.|ff|"
                        connecte << res
            joueur << "|rgc|Vous avez été banni du canal {}.|ff|".format(
                    self.nom)
        else:
            self.liste_noir.remove(joueur)
            joueur << "|rgc|Vous n'êtes plus sur la liste noire du canal " \
                    "{}.|ff|".format(self.nom)
    
    def promouvoir_ou_dechoir(self, joueur):
        """Promeut ou déchoit un joueur du statut de modérateur"""
        if not joueur in self.moderateurs:
            for connecte in self.connectes:
                if (connecte in self.moderateurs or connecte is self.auteur) and \
                        connecte in type(self).importeur.connex.joueurs_connectes:
                    if connecte in self.immerges:
                        connecte << self.clr + "<{} a été promu " \
                                "modérateur.>|ff|".format(joueur.nom)
                    else:
                        connecte << self.clr + "[" + self.nom + "] {} a été " \
                                "promu modérateur.|ff|".format(joueur.nom)
            self.moderateurs.append(joueur)
            if joueur in type(self).importeur.connex.joueurs_connectes:
                if joueur in self.immerges:
                    joueur << self.clr + "<Vous avez été promu modérateur.>|ff|"
                else:
                    joueur << self.clr + "[" + self.nom + "] Vous avez " \
                            "été promu modérateur.|ff|"
        else:
            self.moderateurs.remove(joueur)
            if joueur in type(self).importeur.connex.joueurs_connectes:
                if joueur in self.immerges:
                    res = self.clr + "<Vous avez été déchu du rang de " \
                            "modérateur.>|ff|"
                    joueur << res
                else:
                    joueur << self.clr + "[" + self.nom + "] Vous avez " \
                            "été déchu du rang de modérateur.|ff|"
            for connecte in self.connectes:
                if (connecte in self.moderateurs or connecte is self.auteur) and \
                        connecte in type(self).importeur.connex.joueurs_connectes:
                    if connecte in self.immerges:
                        connecte << self.clr + "<{} a été déchu du statut de " \
                                "modérateur.>|ff|".format(joueur.nom)
                    else:
                        connecte << self.clr + "[" + self.nom + "] {} a été " \
                                "déchu du statut de modérateur.|ff|".format(
                                joueur.nom)
    
    def envoyer(self, joueur, message):
        """Envoie un message au canal"""
        type(self).importeur.communication. \
                dernier_canaux[joueur.nom] = self.nom
        ex_moi = self.clr + "[" + self.nom + "] Vous dites : "
        ex_moi += message + "|ff|"
        ex_autre = self.clr + "[" + self.nom + "] " + joueur.nom
        ex_autre += " dit : " + message + "|ff|"
        im = self.clr + "<" + joueur.nom + "> " + message + "|ff|"
        if joueur in self.immerges:
            joueur << im
        else:
            joueur << ex_moi
        
        for connecte in self.connectes:
            if connecte is not joueur:
                if connecte in type(self).importeur.connex.joueurs_connectes:
                    if connecte in self.immerges:
                        connecte << im
                    else:
                        connecte << ex_autre
    
    def nettoyer(self):
        """Nettoie le canal en supprimant les None des ListeID."""
        self.moderateurs.supprimer_none()
        self.immerges.supprimer_none()
        self.connectes.supprimer_none()
        self.liste_noire.supprimer_none()

