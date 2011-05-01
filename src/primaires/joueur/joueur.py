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


"""Fichier contenant la classe Joueur, détaillée plus bas."""

from abstraits.id import ObjetID
from primaires.perso.personnage import Personnage

class Joueur(Personnage):
    """Classe représentant un joueur, c'est-à-dire un personnage connecté
    grâce à un client, à différencier des NPCs qui sont des personnages
    virtuels, animés par l'univers.
    
    """
    groupe = "joueurs"
    sous_rep = "joueurs"
    
    def __init__(self):
        """Constructeur du joueur"""
        Personnage.__init__(self)
        self.groupe = "administrateur"
        self.compte = None
        self.instance_connexion = None
        self.connecte = False
        self.garder_connecte = False
        self.afk = ""
    
    def __getstate__(self):
        retour = self.__dict__.copy()
        retour["instance_connexion"] = None
        return retour
    
    def _get_encodage(self):
        """Retourne l'encodage du compte"""
        return self.compte.encodage
    
    encodage = property(_get_encodage)
    
    def est_connecte(self):
        """Retourne la valeur de self.connecte"""
        return self.connecte
    
    def retablir_contextes(self):
        contexte = type(self).importeur.interpreteur.contextes[
                "personnage:connexion:mode_connecte"](self.instance_connexion)
        self.contextes.vider()
        self.contexte_actuel = contexte
        self.enregistrer()
    
    def pre_connecter(self):
        """Méthode appelée pour préparer la connexion.
        ATTENTION : on parle ici de la connexion du joueur. Elle
        n'intervient pas à la connexion du client mais quand un joueur
        entre dans l'univers.
        En ce sens, le terme de connexion est à prendre dans le sens de
        lien avec l'univers, non pas dans le sens réseau.
        
        """
        for contexte in self.contextes:
            contexte.pere = self.instance_connexion
        
        if len(self.contextes) == 0:
            contexte = type(self).importeur.interpreteur.contextes[
                    "personnage:connexion:mode_connecte"](
                    self.instance_connexion)
            self.contexte_actuel = contexte
        
        serveur = type(self).importeur.serveur
        if self.salle is None:
            # On recherche la salle
            cle = type(self).importeur.salle.salle_retour
            salle = type(self).importeur.salle[cle]
            self.salle = salle
        
        # On verrouille la déconnexion
        # Autrement dit, on déconnecte simplement les instances
        # conflictuelles, pas les joueurs derrière
        self.garder_connecte = True
        for connecte in type(self).importeur.connex.instances.values():
            joueur_connecte = connecte.joueur
            if joueur_connecte and \
                    connecte is not self.instance_connexion and \
                    joueur_connecte is self:
                connecte.envoyer("|att|Un autre client demande à utiliser " \
                    "ce personnage.\nVous allez être déconnecté.|ff|")
                connecte.deconnecter("un autre client se connecte sur " \
                        "ce personnage")
        
        serveur.verifier_deconnexions()
        self.garder_connecte = False
        self.connecte = True
        salle = self.salle
        if salle:
            salle.ajouter_personnage(self)
        
        self << self.contexte_actuel.accueil()
    
    def pre_deconnecter(self):
        """Cette méthode prépare la déconnexion du joueur.
        Là encore, elle est à dissocier de la déconnexion du client.
        Si un client se déconnecte, le joueur n'est pas forcément
        déconnecté. De même, le joueur peut être déconnecté (c'est-à-dire
        retiré de l'univers) mais son client peut être maintenu.
        
        """
        self.connecte = False
        salle = self.salle
        if salle:
            salle.retirer_personnage(self)
        type(self).importeur.communication. \
                conversations.vider_conversations_pour(self)
    
    def envoyer(self, msg):
        """On redirige sur l'envoie de l'instance de connexion."""
        self.instance_connexion.envoyer(msg)

# On ajoute le groupe à ObjetID
ObjetID.ajouter_groupe(Joueur)
