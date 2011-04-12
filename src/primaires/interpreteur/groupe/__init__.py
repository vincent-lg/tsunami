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


"""Ce fichier définit un conteneur de groupe. Il doit n'y voir qu'un conteneur
de groupes et c'est de ce fait à la fois une classe singleton implicite
dérivée de Unique.

"""

from abstraits.unique import Unique
from primaires.interpreteur.groupe.groupe import Groupe

class ConteneurGroupes(Unique):
    
    """Classe conteneur des groupes.
    Elle peut être soit créée directement par le système si le fichier
    n'existe pas, soit récupérée depuis son fichier de sauvegarde.
    
    """
    
    def __init__(self):
        """Constructeur du conteneur."""
        Unique.__init__(self, "groupes", "groupes")
        self._groupes = {} # nom_groupe:groupe
        
        # Dictionnaire associant une adresse de commande à un groupe
        self.commandes = {}
    
    def __getinitargs__(self):
        return ()
    
    def __contains__(self, nom_groupe):
        """Retourne True si le groupe est dans le dictionnaire, False sinon"""
        return nom_groupe in self._groupes.keys()
    
    def __getitem__(self, nom_groupe):
        """Retourne le groupe avec le nom spécifié"""
        return self._groupes[nom_groupe]
    
    def __len__(self):
        """Retourne le nombre de groupes"""
        return len(self._groupes)
    
    def ajouter_groupe(self, nom_groupe):
        """Méthode appelée pour ajouter un groupe.
        L'objet Groupe est créé "à la volée" et est retourné par la méthode si
        l'on désire le manipuler directement.
        
        """
        groupe = Groupe(self, nom_groupe)
        self._groupes[nom_groupe] = groupe
        self.enregistrer()
        return groupe
    
    def supprimer_groupe(self, nom_groupe):
        """Supprime le groupe nom_groupe"""
        del self._groupes[nom_groupe]
        self.enregistrer()
    
    def ajouter_commande(self, commande):
        """Ajout de 'commande' dans son groupe"""
        if not commande.adresse in self.commandes.keys():
            groupe = self[commande.groupe]
            self.commandes[commande.adresse] = groupe
            self.enregistrer()
    
    def supprimer_commande(self, commande):
        """On supprime la commande 'commande'.
        
        """
        del self.commandes[commande.adresse]
        self.enregistrer()
    
    def changer_groupe_commande(self, chemin, nom_groupe):
        """Change le groupe d'une commande.
        
        """
        nouveau_groupe = self[nom_groupe]
        self.commandes[chemin] = nouveau_groupe
        self.enregistrer()
    
    def personnage_a_le_droit(self, personnage, commande):
        """Le personnage a-t-il le droit d'appeler 'commande' ?"""
        if personnage.groupe in self:
            groupe_png = self[personnage.groupe]
        else:
            groupe_png = self["npc"] # droits minimums
        
        groupe_cmd = self.commandes[commande.adresse]
        
        return self.explorer_groupes_inclus(groupe_png, groupe_cmd.nom)
    
    def explorer_groupes_inclus(self, groupe_base, cherche):
        """Explore les groupes inclus de 'groupe_base', récursivement.
        Si le groupe groupe_base ou l'un des groupes inclus a pour nom
        'cherche', retourne True, False sinon.
        
        """
        trouve = False
        if cherche == groupe_base.nom:
            trouve = True
        else:
            for nom_groupe in groupe_base.groupes_inclus:
                if nom_groupe == cherche:
                    trouve = True
                    break
                
                r_groupe = self[nom_groupe]
                trouve = self.explorer_groupes_inclus(r_groupe, cherche)
                if trouve:
                    break
        
        return trouve
