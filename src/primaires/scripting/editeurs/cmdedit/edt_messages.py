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


"""Fichier contenant le contexte éditeur EdtMessages."""

from primaires.interpreteur.editeur import Editeur

class EdtMessages(Editeur):
    
    """Classe définissant le contexte éditeur 'messages'.
    
    Ce contexte permet d'éditer les messages de la commande.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("?", self.opt_aide)
        self.ajouter_option("err", self.opt_erreur)
        self.ajouter_option("att", self.opt_attente)
    
    def accueil(self):
        """Retourne le message d'accueil."""
        commande = self.objet
        return \
            "Cet éditeur vous permet de configurer les différents " \
            "messages de la\n " \
            "commande. Chaque message est configurable " \
            "par une différente option.\n" \
            "Si vous voulez effacer le message correspondant, " \
            "entrez l'option sans argument.\n\n" \
            "Si vous voulez avoir de l'aide sur les différents messages,\n" \
            "entrez |cmd|/?|ff| pour afficher l'aide.\n\n" \
            "Options disponibles :\n\n" \
            "  |cmd|/err (message)|ff| : configure le message d'erreur\n" \
            "  |cmd|/att (message)|ff| : configure le message d'attente\n\n" \
            "Messages actuels :\n" \
            "  Erreur : |bc|" + commande.message_erreur + "|ff|\n" \
            "  Attente : |bc|" + commande.message_attente + "|ff|"
    
    def opt_erreur(self, arguments):
        """Change le message d'erreur de la commande dynamique.
        
        Syntaxe :
            /err (message)
        
        """
        message = arguments.capitalize()
        commande = self.objet
        if message and message[-1] not in ".!?":
            message += "."
        
        commande.message_erreur = message
        self.actualiser()
    
    def opt_attente(self, arguments):
        """Change le message d'attente de la commande dynamique.
        
        Syntaxe :
            /att (message)
        
        """
        message = arguments.capitalize()
        commande = self.objet
        if message and message[-1] not in ".!?":
            message += "."
        
        commande.message_attente = message
        self.actualiser()
    
    def opt_aide(self, arguments):
        """affiche l'aide."""
        self.pere.envoyer( \
            "Message d'erreur :\n\n" \
            "    Ce message est envoyé quand l'objet désigné " \
            "par le joueur lors de\n" \
            "    l'appel de la commande n'est pas scriptable " \
            "ou ne contient pas\n" \
            "    l'évènement correspondant à la commande. " \
            "Par exemple, le joueur\n" \
            "    essaye de pousser un détail de la salle qui n'a " \
            "pas été scripté\n" \
            "    pour ce faire.\n\n" \
            "Message d'attente :\n\n" \
            "    Ce message est envoyé au joueur seulement " \
            "si la commande est configurée\n" \
            "    pour s'exécuter avec de la latence. Dans ce cas, " \
            "le message d'attente\n" \
            "    est envoyé quand le joueur exécute la commande, " \
            "avant que le script\n" \
            "    ne soit envoyé (après la latence).")

