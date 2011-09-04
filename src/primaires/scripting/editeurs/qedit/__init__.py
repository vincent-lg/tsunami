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


"""Package contenant les éditeurs qedit (éditeurs de quête).

Ce fichier en particulier contient l'éditeur racine de qedit.

"""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .presentation import EdtPresentation
from primaires.format.fonctions import supprimer_accents, contient
from primaires.scripting.quete.quete import Quete, RE_QUETE_VALIDE

class EdtQedit(Editeur):
    
    """Classe définissant l'éditeur de quête 'qedit'.
    
    """
    
    nom = "qedit"
    
    def __init__(self, personnage, objet=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Editeur.__init__(self, instance_connexion, objet)
        self.personnage = personnage
    
    def __getnewargs__(self):
        return (None, None)
    
    def accueil(self):
        """Message d'accueil de l'éditeur.
        
        On affiche les quêtes existantes.
        
        """
        quetes = type(self).importeur.scripting.quetes.values()
        msg = "Editeur de quête :\n\n" \
            "Ci-dessous se trouve la liste des quêtes existantes.\n" \
            "Entrez simplement |ent|sa clé|ff| pour l'éditer ou pour " \
            "en créer une nouvelle.\n" \
            "Tapez |cmd|q|ff| pour quitter cet éditeur.\n\n" \
            "Quêtes disponibles :\n  "
        str_quetes = [str(q) for q in quetes]
        if not str_quetes:
            str_quetes = ["Aucune quête n'existe encore."]
        
        str_quetes = "\n  ".join(str_quetes)
        msg += str_quetes
        return msg
    
    def interpreter(self, msg):
        """Interprétation du message"""
        msg = msg.lower()
        print(msg, RE_QUETE_VALIDE.search(msg))
        if msg == "q":
            self.pere.joueur.contextes.retirer()
            self.pere.envoyer("Fermeture de l'éditeur de quêtes.")
        elif RE_QUETE_VALIDE.search(msg) is None:
            self.pere << "|err|Cette clé de quête est invalide.|ff|"
        else:
            if msg in type(self).importeur.scripting.quetes.keys():
                quete = type(self).importeur.scripting.quetes[msg]
            else:
                quete = Quete(msg, self.personnage)
                type(self).importeur.scripting.quetes[msg] = quete
            
            enveloppe = EnveloppeObjet(EdtPresentation, quete, "")
            contexte = enveloppe.construire(self.personnage)
            
            self.migrer_contexte(contexte)
