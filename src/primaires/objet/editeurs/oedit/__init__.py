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


"""Package contenant l'éditeur 'oedit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .presentation import EdtPresentation
from primaires.objet.types import types
from primaires.format.fonctions import supprimer_accents, contient

class EdtOedit(Editeur):
    
    """Classe définissant l'éditeur d'objet 'oedit'.
    
    """
    
    nom = "oedit"
    
    def __init__(self, personnage, prototype):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Editeur.__init__(self, instance_connexion, prototype)
        self.personnage = personnage
        self.identifiant = ""
    
    def __getnewargs__(self):
        return (None, None)
    
    def accueil(self):
        """Message d'accueil de l'éditeur.
        On affiche les types disponibles.
        
        """
        identifiant = self.identifiant
        noms_types = tuple(types.keys())
        return "|tit|Création du prototype {}|ff|\n\n".format(identifiant) + \
                "Entrez |cmd|le type d'objet|ff| que vous souhaitez créer " \
                "ou |cmd|a|ff| pour annuler.\n" \
                "Le type choisi ne pourra pas être modifié par la suite, " \
                "soyez prudent.\n\n" \
                "Liste des types existants : |cmd|" + "|ff|, |cmd|".join(
                noms_types) + "|ff|"
    
    def get_prompt(self):
        return "->"
    
    def interpreter(self, msg):
        """Interprétation du message"""
        msg = msg.lower()
        if msg == "a":
            self.pere.joueur.contextes.retirer()
            self.pere.envoyer("Opération annulée.")
        else:
            type_choisi = ""
            for nom in types.keys():
                if contient(nom, msg):
                    type_choisi = nom
            
            if not type_choisi:
                self.pere << "|err|Ce type est inconnu.|ff|"
            else:
                self.objet = type(self).importeur.objet.creer_prototype(
                        self.identifiant, type_choisi)
                enveloppe = EnveloppeObjet(EdtPresentation, self.objet, "")
                contexte = enveloppe.construire(self.personnage)
                
                self.migrer_contexte(contexte)
